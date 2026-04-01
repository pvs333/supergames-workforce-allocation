from models import (
    Game, GameTitle, WorkItem, WorkType, 
    Severity, StaffPool
)
from itertools import combinations
from typing import List, Tuple
import random

DAYS_PER_SPRINT = 10  # each staff member contributes 10 days per sprint

def task1Generate(seed: int = 42):
    
    games = [
        Game(
            id="mmo",
            title=GameTitle.MMO,
            branch="Bangalore",
            monthlyRevenue=789600.0,
            revenuePotential=15670000.0,
            activePlayers=325000,
            churnRate=0.05,
        )
    ]

    workQueue = [
        WorkItem(
            id="b1",
            gameId="mmo",
            workType=WorkType.BUG,
            title="Chat system lag",
            severity=Severity.MEDIUM,
            effort=120,
            revenueImpact=30.00,
            impactDelay=1,
            churnReduction=0.0,
        ),
        WorkItem(
            id="b2",
            gameId="mmo",
            workType=WorkType.BUG,
            title="Game crashes on login",
            severity=Severity.BLOCKER,
            effort=300,
            revenueImpact=250.00,
            impactDelay=0,
            churnReduction=0.3,
        ),
        WorkItem(
            id="b3",
            gameId="mmo",
            workType=WorkType.BUG,
            title="Payment processing failure",
            severity=Severity.CRITICAL,
            effort=200,
            revenueImpact=180.00,
            impactDelay=1,
            churnReduction=0.2,
        ),
        WorkItem(
            id="b4",
            gameId="mmo",
            workType=WorkType.BUG,
            title="Character progression reset",
            severity=Severity.HIGH,
            effort=180,
            revenueImpact=90.00,
            impactDelay=0,
            churnReduction=0.1,
        ),
    ]

    staffPool = StaffPool(total=67)
    totalSteps = 1
    goal = "You are the engineering lead for Super MMO, Bangalore branch. You have 67 staff and 1 sprint. Assign staff to bugs to maximise revenue recovered this sprint."

    return games, workQueue, staffPool, totalSteps, goal

#task2

def task2Generate(seed: int = 42):
    games = [
        Game(
            id="mmo",
            title=GameTitle.MMO,
            branch="Mumbai",
            monthlyRevenue=1200000.0,
            revenuePotential=2500000.0,
            activePlayers=280000,
            churnRate=0.04,
        ),
        Game(
            id="shooter",
            title=GameTitle.SHOOTER,
            branch="Chennai",
            monthlyRevenue=800000.0,
            revenuePotential=1400000.0,
            activePlayers=150000,
            churnRate=0.05,
        ),
        Game(
            id="strat",
            title=GameTitle.STRAT,
            branch="Bangalore",
            monthlyRevenue=500000.0,
            revenuePotential=1800000.0,
            activePlayers=90000,
            churnRate=0.06,
        ),
        Game(
            id="fighter",
            title=GameTitle.FIGHTER,
            branch="Hyderabad",
            monthlyRevenue=300000.0,
            revenuePotential=900000.0,
            activePlayers=60000,
            churnRate=0.07,
        ),
    ]

    workQueue = [
        # Bugs
        WorkItem(
            id="b1", gameId="shooter", workType=WorkType.BUG,
            title="Anti-cheat false bans", severity=Severity.CRITICAL,
            effort=200, revenueImpact=180.0, impactDelay=0, churnReduction=0.2,
        ),
        WorkItem(
            id="b3", gameId="strat", workType=WorkType.BUG,
            title="Save file corruption", severity=Severity.CRITICAL,
            effort=160, revenueImpact=120.0, impactDelay=0, churnReduction=0.2,
        ),
        WorkItem(
            id="b4", gameId="fighter", workType=WorkType.BUG,
            title="Ranked mode desync", severity=Severity.HIGH,
            effort=120, revenueImpact=60.0, impactDelay=0, churnReduction=0.1,
        ),
        WorkItem(
            id="b5",
            gameId="mmo",
            workType=WorkType.BUG,
            title="Game crashes on login",
            severity=Severity.BLOCKER,
            effort=300,
            revenueImpact=250.00,
            impactDelay=0,
            churnReduction=0.3,
        ),
        WorkItem(
            id="b6",
            gameId="mmo",
            workType=WorkType.BUG,
            title="Payment processing failure",
            severity=Severity.CRITICAL,
            effort=200,
            revenueImpact=180.00,
            impactDelay=1,
            churnReduction=0.2,
        ),
        # Features
        WorkItem(
            id="f1", gameId="mmo", workType=WorkType.FEATURE,
            title="Season 8 content drop", severity=Severity.HIGH,
            effort=400, revenueImpact=280.0, impactDelay=1, churnReduction=0.0,
        ),
        WorkItem(
            id="f2", gameId="strat", workType=WorkType.FEATURE,
            title="Multiplayer co-op mode", severity=Severity.HIGH,
            effort=500, revenueImpact=220.0, impactDelay=2, churnReduction=0.0,
        ),
        WorkItem(
            id="f3", gameId="shooter", workType=WorkType.FEATURE,
            title="Ranked 2.0 system", severity=Severity.MEDIUM,
            effort=300, revenueImpact=150.0, impactDelay=1, churnReduction=0.0,
        ),
        WorkItem(
            id="f4", gameId="fighter", workType=WorkType.FEATURE,
            title="New DLC Fighters", severity=Severity.MEDIUM,
            effort=280, revenueImpact=100.0, impactDelay=1, churnReduction=0.0,
        ),
    ]

    staffPool = StaffPool(total=69)
    totalSteps = 3
    goal = (
        "You manage engineering across all 4 Super Games titles. "
        "You have 69 staff and 3 sprints. Allocate staff to bugs and features "
        "to maximise total revenue across all 3 sprints. "
        "Unresolved critical bugs increase churn each sprint. "
        "Features take longer but have higher long term payoff."
    )
    return games, workQueue, staffPool, totalSteps, goal


#task3

def task3Generate(seed: int = 42):
    games = [
        Game(
            id="mmo",
            title=GameTitle.MMO,
            branch="Mumbai",
            monthlyRevenue=1400000.0,
            revenuePotential=2800000.0,
            activePlayers=320000,
            churnRate=0.03,
        ),
        Game(
            id="shooter",
            title=GameTitle.SHOOTER,
            branch="Chennai",
            monthlyRevenue=900000.0,
            revenuePotential=1600000.0,
            activePlayers=180000,
            churnRate=0.04,
        ),
        Game(
            id="strat",
            title=GameTitle.STRAT,
            branch="Bangalore",
            monthlyRevenue=600000.0,
            revenuePotential=2200000.0,
            activePlayers=110000,
            churnRate=0.055,
        ),
        Game(
            id="fighter",
            title=GameTitle.FIGHTER,
            branch="Hyderabad",
            monthlyRevenue=350000.0,
            revenuePotential=1000000.0,
            activePlayers=70000,
            churnRate=0.065,
        ),
    ]

    workQueue = [
        WorkItem(
            id="b1", gameId="mmo", workType=WorkType.BUG,
            title="Data breach vulnerability", severity=Severity.BLOCKER,
            effort=350, revenueImpact=450.0, impactDelay=0, churnReduction=0.4,
        ),
        WorkItem(
            id="b2", gameId="shooter", workType=WorkType.BUG,
            title="Wall hack exploit", severity=Severity.BLOCKER,
            effort=280, revenueImpact=250.0, impactDelay=0, churnReduction=0.35,
        ),
        WorkItem(
            id="b3", gameId="strat", workType=WorkType.BUG,
            title="Progression wipe on update", severity=Severity.CRITICAL,
            effort=200, revenueImpact=130.0, impactDelay=0, churnReduction=0.2,
        ),
        WorkItem(
            id="b4", gameId="fighter", workType=WorkType.BUG,
            title="Online multiplayer crash", severity=Severity.HIGH,
            effort=150, revenueImpact=70.0, impactDelay=0, churnReduction=0.1,
        ),
        WorkItem(
            id="b5", gameId="mmo", workType=WorkType.BUG,
            title="Guild bank duplication glitch", severity=Severity.HIGH,
            effort=180, revenueImpact=80.0, impactDelay=0, churnReduction=0.08,
        ),
        WorkItem(
            id="f1", gameId="strat", workType=WorkType.FEATURE,
            title="Open world expansion", severity=Severity.BLOCKER,
            effort=800, revenueImpact=400.0, impactDelay=2, churnReduction=0.0,
        ),
        WorkItem(
            id="f2", gameId="mmo", workType=WorkType.FEATURE,
            title="PvP battleground revamp", severity=Severity.HIGH,
            effort=550, revenueImpact=300.0, impactDelay=1, churnReduction=0.0,
        ),
        WorkItem(
            id="f3", gameId="shooter", workType=WorkType.FEATURE,
            title="Battle pass Season 5", severity=Severity.HIGH,
            effort=320, revenueImpact=180.0, impactDelay=1, churnReduction=0.0,
        ),
        WorkItem(
            id="f4", gameId="fighter", workType=WorkType.FEATURE,
            title="World championship mode", severity=Severity.MEDIUM,
            effort=400, revenueImpact=110.0, impactDelay=2, churnReduction=0.0,
        ),
        WorkItem(
            id="f5", gameId="mmo", workType=WorkType.FEATURE,
            title="Crafting system overhaul", severity=Severity.MEDIUM,
            effort=280, revenueImpact=95.0, impactDelay=1, churnReduction=0.0,
        ),
    ]

    staffPool = StaffPool(total=143)
    totalSteps = 5
    goal = (
        "You are CTO of Super Games. Manage all 4 titles across all branches "
        "with 143 staff over 5 sprints. Unresolved blocker bugs cause compounding "
        "churn every sprint. Features take longer but unlock higher revenue. "
        "Maximise total revenue across all 5 sprints."
    )
    return games, workQueue, staffPool, totalSteps, goal


#task4

def task4Generate(seed: int = 42):
    rng = random.Random(seed)
    crisisStep = rng.randint(2,4)
    games = [
        Game(
            id="mmo",
            title=GameTitle.MMO,
            branch="Mumbai",
            monthlyRevenue=1400000.0,
            revenuePotential=2800000.0,
            activePlayers=320000,
            churnRate=0.03,
        ),
        Game(
            id="shooter",
            title=GameTitle.SHOOTER,
            branch="Chennai",
            monthlyRevenue=900000.0,
            revenuePotential=1600000.0,
            activePlayers=180000,
            churnRate=0.04,
        ),
        Game(
            id="strat",
            title=GameTitle.STRAT,
            branch="Bangalore",
            monthlyRevenue=600000.0,
            revenuePotential=2200000.0,
            activePlayers=110000,
            churnRate=0.055,
        ),
        Game(
            id="fighter",
            title=GameTitle.FIGHTER,
            branch="Hyderabad",
            monthlyRevenue=350000.0,
            revenuePotential=1000000.0,
            activePlayers=70000,
            churnRate=0.065,
        ),
    ]

    workQueue = [
        WorkItem(
            id="b1", gameId="mmo", workType=WorkType.BUG,
            title="Login server instability", severity=Severity.CRITICAL,
            effort=280, revenueImpact=160.0, impactDelay=0, churnReduction=0.15,
        ),
        WorkItem(
            id="b2", gameId="shooter", workType=WorkType.BUG,
            title="Matchmaking ELO corruption", severity=Severity.HIGH,
            effort=160, revenueImpact=90.0, impactDelay=0, churnReduction=0.1,
        ),
        WorkItem(
            id="f1", gameId="strat", workType=WorkType.FEATURE,
            title="New biome: Crystal Caves", severity=Severity.MEDIUM,
            effort=500, revenueImpact=150.0, impactDelay=1, churnReduction=0.0,
        ),
        WorkItem(
            id="f2", gameId="fighter", workType=WorkType.FEATURE,
            title="Online tournament bracket", severity=Severity.MEDIUM,
            effort=380, revenueImpact=100.0, impactDelay=1, churnReduction=0.0,
        ),
        # Crisis item — injected at step 2
        WorkItem(
            id="crisis-1", gameId="mmo", workType=WorkType.BUG,
            title="CRISIS: Player data exposed", severity=Severity.BLOCKER,
            effort=350, revenueImpact=600.0, impactDelay=0, churnReduction=0.5,
            crisis=True,
        ),
    ]

    staffPool = StaffPool(total=131)
    totalSteps = 5
    goal = (
        "A critical data exposure bug may emerge at any point during the episode. "
        "You have 131 staff and 5 sprints. Monitor the work queue carefully each sprint "
        "and prioritise any crisis items immediately when they appear."
    )
    return games, workQueue, staffPool, totalSteps, goal


#graders

def optimalRevenueSingleSprint(
    workQueue: List[WorkItem],
    staffPool: StaffPool,
) -> float:
    """
    Brute force optimal for Task 1 — tries every subset of work items
    and returns the highest achievable revenue in one sprint.
    Only feasible for small queues (≤ 8 items).
    """
    budget = staffPool.total * DAYS_PER_SPRINT
    best = 0.0

    for r in range(1, len(workQueue) + 1):
        for subset in combinations(workQueue, r):
            totalEffort = sum(item.effort for item in subset)
            if totalEffort > budget:
                continue
            revenue = sum(
                item.revenueImpact if item.impactDelay == 0
                else item.revenueImpact * 0.5 if item.impactDelay == 1
                else 0.0
                for item in subset
            )
            if revenue > best:
                best = revenue

    return best


def task1Grade(
    agentImpact: float,
    workQueue: List[WorkItem],
    staffPool: StaffPool,
) -> float:
    optimal = optimalRevenueSingleSprint(workQueue, staffPool)
    if optimal <= 0:
        return 1.0
    return round(min(1.0, max(0.0, agentImpact / optimal)), 4)


def task2Grade(agentTotalTevenue: float, optimalRevenue: float) -> float:
    if optimalRevenue <= 0:
        return 1.0
    return round(min(1.0, max(0.0, agentTotalTevenue / optimalRevenue)), 4)


def task3Grade(agentTotalRevenue: float, optimalRevenue: float) -> float:
    if optimalRevenue <= 0:
        return 1.0
    return round(min(1.0, max(0.0, agentTotalRevenue / optimalRevenue)), 4)


def task4Grade(
    agentTotalRevenue: float,
    optimalRevenue: float,
    crisisResolved: bool,
) -> float:
    if optimalRevenue <= 0:
        return 1.0
    baseScore = min(1.0, max(0.0, agentTotalRevenue / optimalRevenue))
    # hard penalty if crisis was never resolved
    if not crisisResolved:
        baseScore *= 0.25
    return round(baseScore, 4)


# final tasks list

TASKS = {
    1: {
        "generate": task1Generate,
        "grade":    task1Grade,
        "description": "Single game bug triage — maximise revenue in 1 sprint",
        "difficulty":  "easy",
    },
    2: {
        "generate": task2Generate,
        "grade":    task2Grade,
        "description": "Multi-game mixed queue — balance bugs vs features over 3 sprints",
        "difficulty":  "medium",
    },
    3: {
        "generate": task3Generate,
        "grade":    task3Grade,
        "description": "Full portfolio — cross-game churn, 5 sprint revenue maximisation",
        "difficulty":  "hard",
    },
    4: {
        "generate": task4Generate,
        "grade":    task4Grade,
        "description": "Crisis interrupt — emergency bug mid-episode, contain churn",
        "difficulty":  "hard",
    },
}