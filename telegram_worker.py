# Telegram session, authorization, and task-bot communication layer.

class TelegramWorker:
    def __init__(self, session=None):
        self.session = session

    async def start(self):
        pass

    async def stop(self):
        pass
