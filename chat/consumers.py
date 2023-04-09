from channels.generic.websocket import AsyncWebsocketConsumer

COUNTER = 1


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("COnnected")
        self.sender = globals()["COUNTER"]
        globals()["COUNTER"] =  globals()["COUNTER"]+ 1
        await self.channel_layer.group_add("LELO", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        print("Data")
        await self.send(text_data="Hello Mam")
        await self.channel_layer.group_send("LELO", {"type": "chat_message", "message": text_data,
                                                     "sender": self.sender})

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        await self.send(text_data=f"Message from {sender}: {message}")

    async def disconnect(self, code):
        return await super().disconnect(code)


COUNTER = 1
