import asyncio
from enum import StrEnum

class State(StrEnum):
    IDLE = "idle"
    ACTIVE = "active"
    RECOVERY = "recovery"

class TaskWorker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = State.IDLE
        self.task_enabled = False
        self.lock = asyncio.Lock()

    def can_start_task(self, global_enabled=True):
        return global_enabled and self.task_enabled and self.state == State.IDLE

    async def enable(self):
        self.task_enabled = True

    async def disable(self):
        self.task_enabled = False

    async def reset(self):
        self.state = State.IDLE
