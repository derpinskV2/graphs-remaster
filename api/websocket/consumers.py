import logging

import orjson

from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class CSVDataConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        await self.accept()
        logger.warning("Connected")
        await self.send_json({"message": "Connected"})

    async def disconnect(self, close_code):
        logger.warning(f"Disconnected {close_code}")
        pass

    async def receive_json(self, text_data=None, bytes_data=None):
        message = text_data
        logger.warning(f"Received {message}")
        await self.send_json({"message": "asasdasdasdasdasdasdaf"})
        logger.warning("Received")

    async def send_json(self, content, close=False):
        await self.send(text_data=orjson.dumps(content).decode())
        logger.warning("Sent")
        if close:
            await self.close()
