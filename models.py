# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Supergames Environment.

Pydantic data models for supergames workforce allocation
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from openenv.core.env_server.types import Action, Observation
from pydantic import BaseModel, Field

class GameTitle(str, Enum):
    MMO = "Super MMO"
    SHOOTER = "Super Shooter"
    STRAT = "Super Strategy"
    FIGHTER = "Super Fighter"

class WorkType(str, Enum):
    BUG = "bug"
    FEATURE = "feature"

class Severity(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    BLOCKER = 5

#pydantic models

class Game(BaseModel):
    # the game to be worked on
    id: str
    title: GameTitle
    branch: str
    monthlyRevenue: float
    revenuePotential: float
    activePlayers: int
    churnRate: float
    churnMult: float = 1.0
    desc: str = ""

class WorkItem(BaseModel):
    # the work item to be completed
    id: str
    gameId: str
    workType: WorkType
    title: str
    severity: Severity
    effort: int
    revenueImpact: float
    impactDelay: int
    churnReduction: float = 0.0
    crisis: bool = False
    lastSprintStaff: int = 0
    daysWorked: int = 0
    desc: str = ""

class StaffPool(BaseModel):
    # the available staff to work on items
    total: int                  #total staff available
    allocated: int = 0          #staff currently allocated current sprint, resets to 0 at end of each sprint
    
    @property
    def available(self) -> int:
        return self.total - self.allocated

class Assignment(BaseModel):
    workItemID: str
    staff: int = Field(..., ge=1)



class SupergamesAction(Action):
    """a list of assignments"""
    assignments: List[Assignment]

   # message: str = Field(..., description="Message to echo back")


class SupergamesObservation(Observation):
    """Observation from the Supergames environment"""
    taskID: int
    currentStep: int
    totalSteps: int
    games: List[Game]
    workQueue: List[WorkItem]
    staffPool: StaffPool
    crisis: bool = False
    goal: str = ""
    # echoed_message: str = Field(default="", description="The echoed message")
    # message_length: int = Field(default=0, description="Length of the echoed message")

class StepResult(BaseModel):
    observation: SupergamesObservation
    reward: float = Field(..., ge = 0.0, le=1.0)
    done: bool
    info: Optional[Dict[str, Any]] = None

class EnvironmentState(BaseModel):
    taskID: int
    step: int
    totalSteps: int
    games: List[Game]
    workQueue: List[WorkItem]
    staffPool: StaffPool
    completedItems: List[str]
    cumulativeRevenue: float
    crisis: bool = False
    done: bool
    seed: int