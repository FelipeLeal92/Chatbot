from enum import Enum
from app.core.redis import redis_client
import json

class ConversationStage(str, Enum):
    ENTRY = "ENTRY"
    DISCOVERY = "DISCOVERY"
    DIAGNOSIS = "DIAGNOSIS"
    QUALIFICATION = "QUALIFICATION"
    SOLUTION_DIRECTION = "SOLUTION_DIRECTION"
    HANDOFF = "HANDOFF"
    CLOSE = "CLOSE"

def default_state():
    return {
        "stage": ConversationStage.ENTRY.value,
        "collected_data": {},
        "lead_score": 0
    }

def init_conversation_state():
    return {
        "stage": ConversationStage.ENTRY,
        "collected_data": {},
        "lead_score": 0
    }


async def get_state(session_id: str) -> dict:
    key = f"conversation:{session_id}"
    data = await redis_client.get(key)
    return json.loads(data) if data else default_state()


async def save_state(session_id: str, state: dict):
    key = f"conversation:{session_id}"
    await redis_client.set(key, json.dumps(state), ex=3600)


def next_stage(stage: str) -> str:
    flow = list(ConversationStage)
    idx = [s.value for s in flow].index(stage)
    return flow[idx + 1].value if idx + 1 < len(flow) else ConversationStage.CLOSE.value

