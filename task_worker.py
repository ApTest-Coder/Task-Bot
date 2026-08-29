# Per-user task state, lifecycle, and global task controls.

class TaskWorker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.task_enabled = False
        self.active_task = False

    def can_start_task(self, global_enabled=True):
        return global_enabled and self.task_enabled and not self.active_task
