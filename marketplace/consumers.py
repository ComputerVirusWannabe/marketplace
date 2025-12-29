# Description: Chat Consumer, connected to on Chat Page
# Source: Adapted from Django Channels documentation tutorial
#   (channels.readthedocs.io/en/stable/tutorial/part_1.html)
# Notes: Used the Websockets communication from this tutorial and added queries to create chats.
# Now uses nicknames in chat unless no nicknames are provided.
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, CustomUser, Chat, UserChat, Notification
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data["message"]
        user_id = data["user_id"]

        # Fetch user + chat
        user = await sync_to_async(CustomUser.objects.get)(id=user_id)
        chat = await sync_to_async(Chat.objects.get)(id=self.room_name)

        # Determine display name (nickname preferred)
        user_display_name = user.nickname if user.nickname else user.first_name

        # Save message in DB
        await sync_to_async(Message.objects.create)(author=user, content=message, chat=chat)

        # Send notification to other user
        userchats = await sync_to_async(lambda: list(
            UserChat.objects
            .select_related("user")
            .filter(chat=chat)
        ))()

        for userchat in userchats:
            if (userchat.user.id != user.id):
                print(userchat.user.nickname)
                latest_notification = await sync_to_async(lambda:  
                    Notification.objects.filter(user = userchat.user).order_by('-created_at').first()
                )()
                
                #  Only send one new message notification in sequence
                if (latest_notification == None):
                    await sync_to_async(Notification.objects.create)(
                            user=userchat.user,
                            type='new_message',
                            related_id=self.room_name,
                            message=f"New messages in '{chat.name}'."
                            )
                elif (not (latest_notification.type == 'new_message' 
                    and latest_notification.related_id == int(self.room_name))
                    or (latest_notification.type == 'new_message' 
                    and latest_notification.related_id == int(self.room_name)
                    and latest_notification.is_read)
                    ):
                    print("Notification sent")
                    await sync_to_async(Notification.objects.create)(
                            user=userchat.user,
                            type='new_message',
                            related_id=self.room_name,
                            message=f"New messages in '{chat.name}'."
                            )

        # Send to WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
                "user_display_name": user_display_name
            }
        )
        print("Message sent")

    # Receive message broadcasted from group
    async def chat_message(self, event):
        print("Message received")

        message = event["message"]
        user_display_name = event["user_display_name"]

        # Send JSON to browser
        await self.send(text_data=json.dumps({
            "message": message,
            "user_display_name": user_display_name
        }))