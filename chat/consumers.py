import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_group'
        self.scope["character_name"] = None  # Initialize character

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Connection established message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are connected'
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Character mapping
        characters = {
            '1': 'Jerry',
            '2': 'Tom',
            '3': 'Monkey.D.Garp',
            '4': 'GOL.D.ROGER',
            '5': 'Luffy',
            '6': 'Zoro',
            '7': 'Nami',
            '8': 'Sanji',
            '9': 'Usopp',
            '0': 'Oda',
        }

        # If the message is a digit, set/switch the character
        if message in characters:
            self.scope["character_name"] = characters[message]
            response = f"Code received: {message}, {self.scope['character_name']} is now online"
        else:
            # If no character selected yet, default to "Anonymous"
            character_name = self.scope.get("character_name", "Anonymous")
            response = f"{character_name}: {message}"

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': response
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))
