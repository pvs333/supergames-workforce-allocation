# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Supergames environment implementation."""

import copy
from typing import List
from uuid import uuid4
import random
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import SupergamesAction, SupergamesObservation
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from models import SupergamesAction, SupergamesObservation, WorkItem

try:
    from ..tasks import TASKS
    from ..simulator import simulateSprint
except ImportError:
    from tasks import TASKS
    from simulator import simulateSprint


class SupergamesEnvironment(Environment):
    """Environment for staffing and sprint allocation across Supergames tasks."""

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self.stateData = State(episode_id=str(uuid4()), step_count=0)
        # task data
        self.taskId = 1
        self.games = []
        self.workQueue = []
        self.staffPool = None
        self.totalSteps = 0
        self.goal = ""
        # tracking
        self.completedItems: List[WorkItem] = []
        self.cumulativeRevenue = 0.0
        self.crisisResolved = False
        self.done = True
        self.initialWorkQueue = []
        self.initialStaffPool = None
        self.estimatedOptimalRevenue = 1.0
        self.pendingCrisisItems = []
        self.crisisStep = 0

    def buildObservation(self, reward: float | None = None) -> SupergamesObservation:
        return SupergamesObservation(
            taskID=self.taskId,
            currentStep=self.stateData.step_count,
            totalSteps=self.totalSteps,
            games=copy.deepcopy(self.games),
            workQueue=copy.deepcopy(self.workQueue),
            staffPool=copy.deepcopy(self.staffPool),
            crisis=any(item.crisis for item in self.workQueue),            
            goal=self.goal,
            done=self.done,
            reward=reward,
            metadata={
                "completedItems": list(self.completedItems),
                "cumulativeRevenue": round(self.cumulativeRevenue, 2),
            },
        )

    def computeReward(self, sprintRevenue: float) -> float:
        if not self.done:
            averageOptimal = self.estimatedOptimalRevenue / self.totalSteps
            return round(min(1.0, max(0.0, sprintRevenue / averageOptimal)), 4)

        grader = TASKS[self.taskId]["grade"]
        if self.taskId == 1:
            agentImpact = sum(item.revenueImpact for item in self.completedItems)
            return float(grader(agentImpact, self.initialWorkQueue, self.initialStaffPool))
        if self.taskId in (2, 3):
            return float(grader(self.cumulativeRevenue, self.estimatedOptimalRevenue))
        return float(grader(self.cumulativeRevenue, self.estimatedOptimalRevenue, self.crisisResolved))

    def reset(self, task_id: int = 1, seed: int = 42) -> SupergamesObservation:
        if task_id not in TASKS:
            raise ValueError(f"Unknown task_id: {task_id}")

        self.stateData = State(episode_id=str(uuid4()), step_count=0)
        self.taskId = task_id

        games, workQueue, staffPool, totalSteps, goal = TASKS[task_id]["generate"](seed)
        self.games = copy.deepcopy(games)
        self.workQueue = copy.deepcopy(workQueue)
        self.staffPool = copy.deepcopy(staffPool)
        self.totalSteps = totalSteps
        self.goal = goal

        # For task 4, crisis work should only become available starting sprint 2.
        self.pendingCrisisItems = []
        if self.taskId == 4:
            self.pendingCrisisItems = [item for item in self.workQueue if item.crisis]
            self.workQueue = [item for item in self.workQueue if not item.crisis]
            rng = random.Random(seed)
            self.crisisStep = rng.randint(2, 3)

        self.completedItems = []
        self.cumulativeRevenue = 0.0
        self.crisisResolved = False
        self.done = False
        self.initialWorkQueue = copy.deepcopy(self.workQueue)
        self.initialStaffPool = copy.deepcopy(self.staffPool)

        # Coarse upper bound for multi-sprint normalization.
        baseRevenue = sum(game.monthlyRevenue for game in self.games) * self.totalSteps
        impactBound = 0.0
        for item in self.workQueue + self.pendingCrisisItems:
            activeSprints = max(0, self.totalSteps - item.impactDelay)
            impactBound += item.revenueImpact * (activeSprints / max(1, self.totalSteps))
        self.estimatedOptimalRevenue = max(1.0, round(baseRevenue + impactBound, 2))

        return self.buildObservation(reward=0.0)

    def step(self, action: SupergamesAction) -> SupergamesObservation:
        if self.done:
            return self.buildObservation(reward=self.computeReward(0.0))

        self.stateData.step_count += 1

        if self.taskId == 4 and self.stateData.step_count == self.crisisStep and self.pendingCrisisItems:
            self.workQueue.extend(self.pendingCrisisItems)
            self.pendingCrisisItems = []

        (
            self.games,
            self.workQueue,
            completedItems,
            sprintRevenue,
            message,
        ) = simulateSprint(
            self.games,
            self.workQueue,
            self.staffPool,
            action,
            self.stateData.step_count,
        )

        self.cumulativeRevenue += sprintRevenue
        self.completedItems.extend(completedItems)

        if self.taskId == 4 and any(item.crisis for item in completedItems):
            self.crisisResolved = True

        self.done = self.stateData.step_count >= self.totalSteps
        reward = self.computeReward(sprintRevenue)

        obs = self.buildObservation(reward=reward)
        obs.metadata.update(
            {
                "stepRevenue": round(sprintRevenue, 2),
                "message": message,
            }
        )
        return obs

    @property
    def state(self) -> State:
        return self.stateData
