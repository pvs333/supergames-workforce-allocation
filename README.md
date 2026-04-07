
---
title: SuperGames Workforce Allocation
emoji: 🎮
colorFrom: red
colorTo: yellow
sdk: docker
pinned: false
app_port: 8000
tags:
  - openenv
---

# Supergames — Workforce Allocation Environment

An OpenEnv-compliant reinforcement learning environment where an AI agent 
allocates engineering staff across a fictional game studio portfolio to 
maximise revenue.

## Environment Overview

Super Games is a fictional game studio with 4 titles:
- **Super MMO** — high revenue, large playerbase
- **Super Shooter** — competitive, churn-sensitive  
- **Super Strategy** — high potential, growing
- **Super Fighter** — smaller but loyal playerbase

Each sprint the agent assigns staff to bugs and features across these titles.
Unresolved critical bugs compound player churn every sprint. Features take 
longer but unlock higher revenue ceilings.

## Tasks

| Task | Difficulty | Description |
|------|-----------|-------------|
| 1 | Easy | Single game, 1 sprint — precise budget allocation across 4 bugs |
| 2 | Medium | 4 games, 3 sprints — balance bugs vs features |
| 3 | Hard | Full portfolio, 5 sprints — cross-game churn management |
| 4 | Hard | Crisis interrupt — emergency bug appears mid-episode |

## Observation Space

```json
{
  "taskID": 1,
  "currentStep": 0,
  "totalSteps": 1,
  "games": [
    {
      "id": "mmo",
      "title": "Super MMO",
      "branch": "Bangalore",
      "monthlyRevenue": 789600.0,
      "churnRate": 0.05,
      "churnMult": 1.0
    }
  ],
  "workQueue": [
    {
      "id": "b1",
      "workType": "bug",
      "severity": 5,
      "effort": 300,
      "revenueImpact": 250.0,
      "impactDelay": 0,
      "daysWorked": 0,
      "lastSprintStaff": 0,
      "crisis": false
    }
  ],
  "staffPool": {
    "permanent": 67,
    "contractors": 0,
    "allocated": 0
  },
  "crisis": false,
  "goal": "..."
}
```

## Action Space

```json
{
  "assignments": [
    {"workItemID": "b1", "staff": 30},
    {"workItemID": "b2", "staff": 20}
  ]
}
```

Rules:
- Total staff across all assignments cannot exceed `staffPool.available`
- Staff assigned per item must be ≥ 1
- Multiple items can be assigned in one sprint

## Reward

Per-step reward is normalized sprint revenue against estimated optimal:

```
reward = sprint_revenue / (estimated_optimal / total_steps)
```

Final episode score uses a task-specific grader:
- Tasks 1-3: `agent_revenue / optimal_revenue`
- Task 4: revenue ratio × crisis resolution multiplier (0.25 penalty if crisis unresolved)

All rewards are clamped to `[0.0, 1.0]`.

## Simulation

Each staff member contributes **10 staff-days** per sprint. A work item 
completes when `daysWorked >= effort`.

Revenue per sprint:
```
base = monthlyRevenue * (1 - churnRate * churnMult)
total = base + sum(revenueImpact of completed items)
```

Churn multiplier increases by `0.15` per unresolved CRITICAL/BLOCKER bug 
and decreases when bugs are fixed.

## Quick Start

```python
from supergames.server.environment import SupergamesEnvironment
from models import SupergamesAction, Assignment

env = SupergamesEnvironment()
obs = env.reset(task_id=1, seed=42)

action = SupergamesAction(assignments=[
    Assignment(workItemID="b1", staff=30),
    Assignment(workItemID="b4", staff=18),
])

result = env.step(action)
print(result.reward)
```

## Running Locally

```bash
# Install dependencies
pip install -e .

# Start server
python -m server.app

# Test health
curl http://localhost:8000/health
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/reset` | POST | Start new episode |
| `/step` | POST | Execute one sprint |
| `/state` | GET | Current environment state |
| `/docs` | GET | Interactive API docs |

## Inference

```bash
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=meta-llama/Llama-3.3-70B-Instruct
export HF_TOKEN=your_token_here
export ENV_BASE_URL=http://localhost:8000

python inference.py
```

## Baseline Results

Scores using `meta-llama/Llama-3.3-70B-Instruct`:

| Task | Score | Notes |
|------|-------|-------|
| 1 | 0.08 | Requires precise arithmetic — hardest for LLM |
| 2 | 0.94 | Greedy heuristic works well |
| 3 | 0.95 | Multi-sprint strategy near optimal |
| 4 | 0.95 | Crisis prioritisation learned correctly |

Task 1 being the hardest for LLM agents despite being "easy" reveals an 
interesting insight — single sprint budget optimisation requires precise 
numerical reasoning that LLMs struggle with, while multi-sprint strategic 
allocation rewards heuristic thinking that LLMs handle well.

## Project Structure

```
supergames/
├── models.py          # Pydantic domain models
├── simulator.py       # Revenue and churn simulation
├── tasks.py           # Task generators and graders
├── inference.py       # Baseline LLM agent
├── openenv.yaml       # OpenEnv manifest
├── pyproject.toml     # Project metadata
└── server/
    ├── app.py         # FastAPI server
    ├── environment.py # OpenEnv environment class
    └── Dockerfile     # Container definition
```