"""
Simulator for the Supergames Environment.
Given an action from the agent, simulates a sprint and returns the results.
"""
from typing import List, Tuple
import copy
from models import Game, WorkItem, WorkType, StaffPool, SupergamesAction

DAYS_PER_SPRINT = 10  # each staff member contributes 10 days per sprint


def applyAssignments(
    workQueue: List[WorkItem],
    action: SupergamesAction,
    staffPool: StaffPool,
) -> Tuple[List[WorkItem], str]:
    """
    Apply the agent's staff assignments to work items.
    Returns updated work queue and a message if something went wrong.
    """
    # check total staff requested doesn't exceed available
    totalRequested = sum(a.staff for a in action.assignments)
    if totalRequested > staffPool.available:
        return workQueue, f"Overallocation: requested {totalRequested}, only {staffPool.available} available"

    # build a quick lookup so we don't loop the whole queue for every assignment
    queueMap = {item.id: item for item in workQueue}

    for assignment in action.assignments:
        item = queueMap.get(assignment.workItemID)

        if item is None:
            return workQueue, f"Unknown work item: {assignment.workItemID}"

        # add progress to the item
        daysContributed = assignment.staff * DAYS_PER_SPRINT
        item.daysWorked += daysContributed
        item.lastSprintStaff = assignment.staff

    return list(queueMap.values()), "ok"


def getCompletedItems(workQueue: List[WorkItem]) -> Tuple[List[WorkItem], List[WorkItem]]:
    """
    Split the work queue into completed and remaining items.
    An item is complete when daysWorked >= effort.
    """
    completedItems = []
    remainingItems = []

    for item in workQueue:
        if item.daysWorked >= item.effort:
            completedItems.append(item)
        else:
            remainingItems.append(item)

    return completedItems, remainingItems


def updateChurn(
    games: List[Game],
    remainingQueue: List[WorkItem],
    completedItems: List[WorkItem],
) -> List[Game]:
    """
    Update churn multiplier for each game based on unresolved bugs.
    - Unresolved CRITICAL/BLOCKER bugs increase churnMult
    - Completing a bug reduces churnMult by its churnReduction value
    """
    games = copy.deepcopy(games)
    completedIds = {item.id for item in completedItems}

    for game in games:
        # count unresolved critical/blocker bugs for this game
        badBugs = [
            item for item in remainingQueue
            if item.gameId == game.id
            and item.workType == WorkType.BUG
            and item.severity == 4
            and item.id not in completedIds
        ]
        veryBadBugs = [
            item for item in remainingQueue
            if item.gameId == game.id
            and item.workType == WorkType.BUG
            and item.severity == 5
            and item.id not in completedIds
        ]
        # each unresolved bad bug adds 0.15 to churn multiplier
        game.churnMult = 1.0 + (len(badBugs) * 0.15) + (len(veryBadBugs) * 0.25)

        # completed bugs reduce churn
        for item in completedItems:
            if item.gameId == game.id and item.workType == WorkType.BUG:
                game.churnMult = max(1.0, game.churnMult - item.churnReduction)

    return games


def calculateRevenue(
    games: List[Game],
    completedItems: List[WorkItem],
    currentStep: int,
) -> float:
    """
    Calculate total portfolio revenue for this sprint.
    
    For each game:
      base = monthlyRevenue * (1 - churnRate * churnMult)
      + revenueImpact of completed items (adjusted for impactDelay)
    """
    total = 0.0

    for game in games:
        # base revenue shrinks if churn is high
        base = game.monthlyRevenue * (1.0 - game.churnRate * game.churnMult)

        # add revenue from completed items
        for item in completedItems:
            if item.gameId != game.id:
                continue
            if item.impactDelay == 0:
                total += item.revenueImpact
            elif item.impactDelay == 1:
                total += item.revenueImpact * 0.5  # half now, half next sprint
            # impactDelay == 2 means no impact yet this sprint

        total += base

    return round(total, 2)


def simulateSprint(
    games: List[Game],
    workQueue: List[WorkItem],
    staffPool: StaffPool,
    action: SupergamesAction,
    currentStep: int,
) -> Tuple[List[Game], List[WorkItem], List[WorkItem], float, str]:
    """
    Run one sprint of simulation.

    Returns:
        updatedGames     - games with updated churn multipliers
        remainingQueue   - work items not yet complete
        completedItems   - work items finished this sprint
        sprintRevenue    - total revenue earned this sprint
        message           - what happened (for observation)
    """
    # step 1 - apply assignments, update daysWorked
    workQueue, message = applyAssignments(workQueue, action, staffPool)
    if message != "ok":
        return games, workQueue, [], 0.0, message

    # step 2 - figure out what got completed
    completedItems, remainingItems = getCompletedItems(workQueue)

    # step 3 - update churn based on what's still unresolved
    updatedGames = updateChurn(games, remainingItems, completedItems)

    # step 4 - calculate revenue
    sprintRevenue = calculateRevenue(updatedGames, completedItems, currentStep)

    message = (
        f"Completed {len(completedItems)} items: "
        f"{', '.join(i.title for i in completedItems) or 'none'}. "
        f"Revenue: ${sprintRevenue}"
    )

    return updatedGames, remainingItems, completedItems, sprintRevenue, message