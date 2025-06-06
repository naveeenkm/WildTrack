from twilio.rest import Client
from .models import PhoneNumber, Alert

# Animal mapping based on board_id
animal_mapping = {
    1: "Tiger",
    2: "Elephant",
    3: "Deer",
    4: "Lion",
    5: "Bear",
    # Add more mappings as needed
}

# def send_alert_message(board_id, animal_name):
#     """Function to send an alert message using Twilio."""
#     account_sid = 'ACd1c1e5e1b7488681d97a307a7e2a7fcf'
#     auth_token = '36e84fa83a67478ba02437964504b246'
#     client = Client(account_sid, auth_token)

#     # Get phone numbers to send the alert
#     phone_numbers = PhoneNumber.objects.values_list('phone_number', flat=True)

#     # Send message to all phone numbers
#     for number in phone_numbers:
#         message = client.messages.create(
#             from_='+16073676564',  # Your Twilio number
#             body=f'Alert!!! An {animal_name} (ID: {board_id}) is out of region from the forest. By Wildtrack System.',
#             to=number
#         )
#         print(f"Alert sent to {number}: {message.sid}")
        
def check_and_send_alerts():
    """Function to check for unprocessed alerts, send messages, and update 'is_processed'."""
    alerts = Alert.objects.filter(is_processed=False)  # Get all unprocessed alerts

    for alert in alerts:
        animal_name = animal_mapping.get(alert.board_id, "Unknown Animal")
        # send_alert_message(alert.board_id, animal_name)  # Send alert message
        alert.is_processed = True  # Mark as processed
        alert.save()  # Save the updated alert
        
from django.http import JsonResponse
from .models import DeletedAlert, PhoneNumber
from twilio.rest import Client
from django.shortcuts import get_object_or_404

# Define your animal mappings
animal_mapping = {
    1: "Tiger",
    2: "Elephant",
    3: "Deer",
    4: "Lion",
    5: "Bear",
    # Add more mappings as needed
}

def check_and_send_deleted_alerts():
    """Function to check for deleted alerts, send messages, and delete the alert."""
    
    # Fetch all deleted alerts from TrackingDeletedAlert table
    deleted_alerts = DeletedAlert.objects.all()  # Adjust the queryset as needed

    for deleted_alert in deleted_alerts:
        # Map board_id to animal name
        animal_name = animal_mapping.get(deleted_alert.board_id, "Unknown Animal")
        
        # Fetch phone numbers
        phone_numbers = PhoneNumber.objects.values_list('phone_number', flat=True)

        # Send the "You are safe now" message
        account_sid = 'ACffa65e57cb5782a0a2351bcdac028d30'
        auth_token = '8c2a947ffaa3ef425b2d53e3c7b5a4cd'
        client = Client(account_sid, auth_token)

        try:
            # Send the message
            message = client.messages.create(
                from_='+13612735675',  # Your Twilio number
                body=f'You are safe now, the {animal_name}  is back in the region. By Wildtrack System.',
                to=phone_numbers
            )

            # Log message SID for reference
            print(f"Alert sent to {phone_numbers}: {message.sid}")

            # Delete the deleted alert entry after sending the message
            deleted_alert.delete()

            # Return success response
            return JsonResponse({'status': 'success'})

        except Exception as e:
            # Return error response if something goes wrong
            return JsonResponse({'status': 'error', 'message': str(e)})


