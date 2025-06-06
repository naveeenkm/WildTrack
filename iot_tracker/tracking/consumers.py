import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from tracking.models import Alert
from django.utils import timezone
from datetime import timedelta

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # This method is called when a WebSocket connection is about to be established.
        self.room_group_name = "general_alerts"  # Static room name

        # Join the alerts room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

        # Start polling the alert count
        await self.poll_alert_count()

    async def disconnect(self, close_code):
        # This method is called when the WebSocket is disconnected
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Periodically poll the alert count and send updates to the WebSocket
    async def poll_alert_count(self):
        while True:
            # Calculate the start and end of yesterday
            yesterday_start = timezone.now() - timedelta(days=1)
            yesterday_end = yesterday_start.replace(hour=23, minute=59, second=59, microsecond=999999)

            # Fetch the alert count for yesterday
            alert_count = Alert.objects.filter(
                created_at__gte=yesterday_start, created_at__lte=yesterday_end
            ).count()

            # Send the alert count back to the WebSocket
            await self.send(text_data=json.dumps({
                'alert_count': alert_count  # Sending the count to the client
            }))
            
            # Sleep for a specified period before checking again
            await asyncio.sleep(5)  # Poll every 5 seconds (adjust as needed)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", None)  # Extract the message from the client, if any
        
        # Handle the received data if needed. For example, log or process it.
        if message:
            print(f"Received message: {message}")
        
        # Optionally, you can also update the alert count here if needed
        # await self.send_alert_count()

    # Method to send the latest alert count (can be used when a new alert is created or deleted)
    async def send_alert_count(self):
        # Calculate the start and end of yesterday
        yesterday_start = timezone.now() - timedelta(days=1)
        yesterday_end = yesterday_start.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Fetch the alert count for yesterday
        alert_count = Alert.objects.filter(
            created_at__gte=yesterday_start, created_at__lte=yesterday_end
        ).count()

        # Send the alert count back to the WebSocket
        await self.send(text_data=json.dumps({
            'alert_count': alert_count  # Sending the count to the client
        }))



# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class AlertConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.send(text_data=json.dumps({'message': 'WebSocket connected'}))

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         await self.send(text_data=json.dumps({'message': f"Echo: {data.get('message', '')}"}))













# consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from tracking.models import Alert  # Replace with your model

# class AlertConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_group_name = "alerts_room"
        
#         # Join the group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def send_update(self, event):
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             "message": event["message"]
#         }))

# # Signal to send data when the database is updated
# @receiver(post_save, sender=Alert)
# def database_update_signal(sender, instance, **kwargs):
#     async_to_sync(channel_layer.group_send)(
#         "alerts_room",
#         {
#             "type": "send_update",
#             "message": "Database updated"
#         }
#     )
