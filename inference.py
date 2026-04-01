"""
inference.py — Baseline agent for the Supergames environment.
Runs all 4 tasks using an LLM agent via OpenAI client.

Required env vars:
    API_BASE_URL   The API endpoint for the LLM
    MODEL_NAME     The model identifier
    HF_TOKEN       Your Hugging Face / API key
"""

import os
import json
import time
from openai import OpenAI
from server.environment import SupergamesEnvironment
from models import SupergamesAction, Assignment

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY      = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
MODEL_NAME   = os.getenv("MODEL_NAME")
TEMPERATURE  = 0.2
MAX_TOKENS   = 512

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

SYSTEM_PROMPT = """
You are an engineering manager at Super Games.
Your job is to allocate staff to bugs and features each sprint to maximise revenue.

You will receive the current state of the environment as text.
Respond with ONLY a valid JSON object in this exact format, no explanation:

{
  "assignments": [
    {"workItemID": "<id>", "staff": <int>},
    ...
  ]
}

Rules:
- Total staff across all assignments must not exceed staffPool total
- Prioritise crisis items immediately when they appear
- High severity bugs cause compounding churn if left unresolved
- Features take longer but have higher long term payoff
"""


def buildPrompt(obs) -> str:
    # your job — describe the observation to the LLM
    # hint: include goal, currentStep, totalSteps,
    # staffPool.available, and a summary of workQueue items
    lines = [
        "Current Supergames state:",
        f"Goal: {obs.goal}",
        f"Sprint: {obs.currentStep}/{obs.totalSteps}",
        f"Staff available: {obs.staffPool.available} (total={obs.staffPool.total})",
        f"Queue size: {len(obs.workQueue)}",
        
        "Work queue:",
    ]

    if not obs.workQueue:
        lines.append("- No items in queue")
    else:
        for item in obs.workQueue:
            lines.append(
                "- "
                f"id={item.id} "
                f"type={item.workType.value} "
                f"severity={int(item.severity)} "
                f"crisis={item.crisis} "
                f"effort={item.effort} "
                f"daysWorked={item.daysWorked} "
                f"revenueImpact={item.revenueImpact} "
                f"impactDelay={item.impactDelay}"
                f"daysWorked={item.daysWorked}/{item.effort} "
                f"lastSprintStaff={item.lastSprintStaff} "
            )

    lines.extend(
        [
            "",
            "Return ONLY JSON in the requested schema.",
            "Do not include markdown code fences.",
        ]
    )

    return "\n".join(lines)


def parseAction(response: str) -> SupergamesAction:
    # your job — parse the LLM's JSON response into a SupergamesAction
    # hint: use json.loads(), then build Assignment objects
    # if parsing fails, return a fallback action
    fallback = SupergamesAction(assignments=[])

    try:
        raw = response.strip()
        if not raw:
            return fallback

        # Handle markdown-wrapped JSON or extra text around the payload.
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            start = raw.find("{")
            end = raw.rfind("}")
            if start == -1 or end == -1 or end <= start:
                return fallback
            data = json.loads(raw[start : end + 1])

        assignments_data = data.get("assignments", []) if isinstance(data, dict) else []
        if not isinstance(assignments_data, list):
            return fallback

        assignments = []
        for item in assignments_data:
            if not isinstance(item, dict):
                continue

            work_item_id = item.get("workItemID")
            staff = item.get("staff")

            if not isinstance(work_item_id, str) or not work_item_id.strip():
                continue

            try:
                staff_int = int(staff)
            except (TypeError, ValueError):
                continue

            if staff_int < 1:
                continue

            assignments.append(Assignment(workItemID=work_item_id.strip(), staff=staff_int))

        return SupergamesAction(assignments=assignments)
    except Exception:
        return fallback


def runTask(taskId: int, seed: int = 42) -> float:
    env = SupergamesEnvironment()
    obs = env.reset(task_id=taskId, seed=seed)
    print(f"\nTask {taskId} | {obs.goal[:80]}...")

    while not obs.done:
        prompt = buildPrompt(obs)
        print(f"\n{'='*40}")
        print(f"TASK {taskId} | STEP {obs.currentStep + 1}/{obs.totalSteps}")
        print(f"{'='*40}")
        print(f"--- OBSERVATION ---\n{prompt}")
        
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )
            raw = response.choices[0].message.content or ""
            print(f"\n--- LLM RESPONSE ---\n{raw}")
        except Exception as e:
            print(f"  LLM error: {e}")
            raw = '{"assignments": []}'

        action = parseAction(raw)
        print(f"\n--- PARSED ACTION ---\n{action}")
        obs = env.step(action)
        print(f"  Step {obs.currentStep}/{obs.totalSteps} | reward: {obs.reward:.4f}")
        time.sleep(1)

    return obs.reward or 0.0


def main():
    print("Supergames Basic Inference")
    scores = []
    for taskId in range(1, 5):
        try:
            score = runTask(taskId)
            scores.append(score)
            print(f"Task {taskId} final score: {score:.4f}")
        except Exception as e:
            print(f"Task {taskId} failed: {e}")
            scores.append(0.0)

    print("\n=== RESULTS ===")
    for i, score in enumerate(scores, 1):
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        print(f"Task {i}: [{bar}] {score:.4f}")
    print(f"Mean: {sum(scores)/len(scores):.4f}")


if __name__ == "__main__":
    main()