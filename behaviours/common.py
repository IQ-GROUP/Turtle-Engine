# behaviours/common.py
import asyncio

class CommonBehaviour:
    def __init__(self, tick=0.016):
        self.tick = tick

    async def start(self):
        pass

    async def update(self):
        pass

    async def late_update(self):
        pass

    async def run(self):
        await self.start()
        while True:
            await self.update()
            await self.late_update()
            await asyncio.sleep(self.tick)
