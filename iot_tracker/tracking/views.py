
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from tracking.utils import check_and_send_alerts, check_and_send_deleted_alerts
from .models import Alert
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process and store the data, e.g., in a database
            print(data)  # Log the data for now
            return JsonResponse({"status": "Data received"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid data"}, status=400)
    return JsonResponse({"message": "Send POST request"}, status=405)

def dashboard(request):
    return render(request, 'dashboard.html')


from django.db.models import Count

def home(request):
    now = timezone.now()

    # Get the recent alerts excluding those with status 'animal'
    recent_alerts = Alert.objects.exclude(status='animal').order_by('-datetime')
    unique_board_count = Alert.objects.filter(status='animal').values('board_id').distinct().count()
    phone_number_count = PhoneNumber.objects.count()
   

    # Count of alerts
    alert_count = recent_alerts.count()

    # Define a mapping of board_id to animal names
    animal_mapping = {
        1: "Tiger",
        2: "Elephant",
        3: "Deer",
        4: "Lion",  # Add more mappings as needed
        5: "Bear",
        # Continue with your animal mappings
    }

    # Predefine angles for specific animals
    predefined_angles = {
        1: 45,  # Tiger
        2: 25,  # Elephant
        3: 135, # Deer
        4: 180, # Lion
        5: 225, # Bear
        # Add more board_id to angle mappings as needed
    }

    # Loop through recent_alerts and add the corresponding animal name to each alert
    for alert in recent_alerts:
        animal_name = animal_mapping.get(alert.board_id, "Unknown")  # Default to "Unknown" if no match
        alert.animal_name = animal_name  # Add the animal name to the alert object

    # Prepare the animal list with alert details
    animal_counts = (
        Alert.objects.exclude(status='animal')  # Exclude alerts with status 'animal'
        .values('board_id')
        .annotate(count=Count('board_id'))
    )
    unique_animal_counts = (
    Alert.objects.filter(status='animal')  # Include only alerts with status 'animal'
    .values('board_id')
    .annotate(count=Count('board_id'))
)


    # Prepare the animal list for alert count display
    animal_list = []
    for entry in animal_counts:
        board_id = entry['board_id']
        count = entry['count']
        animal_name = animal_mapping.get(board_id, "Unknown")
        angle = predefined_angles.get(board_id, 0)  # Default to 0 degrees if no predefined angle
        animal_list.append({'name': animal_name, 'count': count, 'angle': angle})
    unique_animal_list = []
    for entry in unique_animal_counts:
        board_id = entry['board_id']
        count = entry['count']
        animal_name = animal_mapping.get(board_id, "Unknown")
        angle = predefined_angles.get(board_id, 0)  # Default to 0 degrees if no predefined angle
        unique_animal_list.append({'name': animal_name, 'count': count, 'angle': angle})
    for alert in recent_alerts:
        alert.animal_name = animal_mapping.get(alert.board_id, "Unknown")
    # Pass the data to the template
    return render(request, 'home.html', {
        'alerts': recent_alerts,
        'alert_count': alert_count,
        'animal_list': json.dumps(animal_list),
        'unique_board_count': unique_board_count,
        'unique_animal_list':unique_animal_list,
        'phone_number_count':phone_number_count,
        'animal_mapping':animal_mapping
    })

    
@login_required


def alerts_view(request):
    # Get the current time (optional, depending on your needs)
    now = timezone.now()

    # Get the recent alerts excluding those with status 'animal'
    recent_alerts = Alert.objects.exclude(status='animal').order_by('-datetime')

    # Count of alerts
    alert_count = recent_alerts.count()

    # Define a mapping of board_id to animal names
    animal_mapping = {
        1: "Tiger",
        2: "Elephant",
        3: "Deer",
        4: "Lion",  # Add more mappings as needed
        5: "Bear",
        # Continue with your animal mappings
    }

    # Predefine angles for specific animals
    predefined_angles = {
        1: 45,  # Tiger
        2: 25,  # Elephant
        3: 135, # Deer
        4: 180, # Lion
        5: 225, # Bear
        # Add more board_id to angle mappings as needed
    }

    # Loop through recent_alerts and add the corresponding animal name to each alert
    for alert in recent_alerts:
        animal_name = animal_mapping.get(alert.board_id, "Unknown")  # Default to "Unknown" if no match
        alert.animal_name = animal_name  # Add the animal name to the alert object

    # Prepare the animal list with alert details
    animal_counts = (
        Alert.objects.exclude(status='animal')  # Exclude alerts with status 'animal'
        .values('board_id')
        .annotate(count=Count('board_id'))
    )

    # Prepare the animal list for alert count display
    animal_list = []
    for entry in animal_counts:
        board_id = entry['board_id']
        count = entry['count']
        animal_name = animal_mapping.get(board_id, "Unknown")
        angle = predefined_angles.get(board_id, 0)  # Default to 0 degrees if no predefined angle
        animal_list.append({'name': animal_name, 'count': count, 'angle': angle})

    # Pass the data to the template
    return render(request, 'alerts.html', {
        'alerts': recent_alerts,
        'alert_count': alert_count,
        'animal_list': json.dumps(animal_list)
    })



# ACTUALL SERVER ==>[BACKEND]
from django.http import JsonResponse
def get_alert_count(request):
    # Get the count of new alerts (e.g., filtered by a certain condition)
    check_and_send_alerts()
    check_and_send_deleted_alerts()
    count = Alert.objects.exclude(status='animal').all().count()
    return JsonResponse({'count': count})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('modalEmail')  # Get the email
        password = request.POST.get('modalPassword')  # Get the password

        user = authenticate(request, username=email, password=password)  # Use username or email based on your user model
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid email or password.')
    return redirect('home')  # Render the login template

# Signup view
def signup_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('home')

        # Create new user
        user = User.objects.create_user(username=email, password=password)
        user.first_name = name
        user.save()
        messages.success(request, "Account successfully created!, Please login..")
        # Log the user in after sign-up
        login(request, user)  
        return redirect('home')

    return render(request, 'signup.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        
        # Compose the email message
        subject = f"Contact Form Submission from {name}"
        message = f"Name: {name}\nEmail: {email}\nPhone: {phone}"
        from_email = email  # or use a no-reply email address
        
        try:
            send_mail(subject, message, from_email, ['kmnaveen1110@gmail.com'])
            messages.success(request, 'Your message has been sent successfully! Thank you for reaching out to us. We will catch you soon!')
            return redirect('home')  # Redirect back to the contact page
        except Exception as e:
            messages.error(request, {e})
            return redirect('home')

    return redirect('home')



# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Alert
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_alert(request, alert_id):
        """Delete an alert by its ID."""
    
        alert = get_object_or_404(Alert, id=alert_id)
        
        # Send the "You are safe now" message
       
        try:
            # Delete the alert
            alert.delete()

            # Return a success response
            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Return an error response if something goes wrong
            return JsonResponse({'status': 'error', 'message': str(e)})
        
        



from django.http import JsonResponse
from django.shortcuts import render
from .models import Alert

def add_animal(request):
    """View to add a new animal based on the board_id."""
    if request.method == 'POST' :
        board_id = request.POST.get('board_id')
        
        if not board_id:
            return JsonResponse({'status': 'error', 'message': 'Board ID is required.'})
        
        # Check if the animal already exists in the database
        animal_exists = Alert.objects.filter(board_id=board_id).exists()
        
        if animal_exists:
            return JsonResponse({'status': 'error', 'message': 'Animal with this board ID already exists.'})
        
        # Add new animal with status 'animal'
        new_animal = Alert.objects.create(
            board_id=board_id,
            distance=2,
            status='animal',  # Set status as 'animal'
              # Default value for new animal
        )
        
        # Return success with updated animal count
        unique_board_count = Alert.objects.values('board_id').annotate(board_count=Count('board_id')).count()
 # Update the animal count
        return JsonResponse({'status': 'success', 'new_animal_count': unique_board_count})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


    






from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PhoneNumber

def add_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Add +91 prefix
        full_number = f'+91{phone_number}'

        # Save to database
        if PhoneNumber.objects.filter(phone_number=full_number).exists():
            messages.warning(request, "This phone number is already in the database.")
        else:
            PhoneNumber.objects.create(phone_number=full_number)
            messages.success(request, "Phone number added successfully!")

        return redirect('home')  # Replace with your desired view



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PhoneNumber
from twilio.rest import Client

@csrf_exempt  # Use only if you are not using AJAX CSRF handling (for development)
def send_safe_message(request):
    if request.method == 'POST':
        # Send a "safe now" message to all phone numbers
        account_sid = 'ACd1c1e5e1b7488681d97a307a7e2a7fcf'
        auth_token = '36e84fa83a67478ba02437964504b246'
        client = Client(account_sid, auth_token)

        phone_numbers = PhoneNumber.objects.values_list('phone_number', flat=True)

        # Send the "You are safe now" message
        message = client.messages.create(
            from_='+16073676564',  # Your Twilio number
            body='You are safe now, the animal is back in the region.',
            to=phone_numbers
        )

        return JsonResponse({'status': 'success', 'message_sid': message.sid})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
