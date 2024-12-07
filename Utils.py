import json
import random
import math
from websockets import connect
import asyncio


class Utils:
    def __init__(self) -> None:
        pass

    def isJson(self, dataString):
        try:
            json.loads(dataString)
            return True
        except:
            return False

    def getRandom(self):
        return math.ceil(random.random() * 1000000)

    async def sendEvent(self, event: str):
        async with connect("ws://127.0.0.1:2760/events/") as websocket:
            await websocket.send(event)
