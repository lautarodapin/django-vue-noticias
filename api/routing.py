from channelsmultiplexer.demultiplexer import AsyncJsonWebsocketDemultiplexer
from chat.consumers import (UserConsumerObserver, RoomConsumer)
from todo.consumers import TodoConsumer
class EntryDeMultiplexer(AsyncJsonWebsocketDemultiplexer):
    applications = {
        "room": RoomConsumer.as_asgi(),
        "user": UserConsumerObserver.as_asgi(),
        "todo": TodoConsumer.as_asgi()
    }
    
    async def receive_json(self, content, **kwargs):
        print(content)
        return await super().receive_json(content, **kwargs)

    async def websocket_connect(self, message):
        print(message)
        return await super().websocket_connect(message) 