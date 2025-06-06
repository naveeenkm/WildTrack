from django.db import models
from twilio.rest import Client
# Create your models here.


animal_mapping = {
        1: "Tiger",
        2: "Elephant",
        3: "Deer",
        4: "Lion",  # Add more mappings as needed
        5: "Bear",
        # Continue with your animal mappings
    }

class Alert(models.Model):
    distance = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    board_id = models.IntegerField(default=0)
    # Removed `msg` field
    status = models.CharField(max_length=50, default="active") 
    is_processed = models.BooleanField(default=False)# Added new column

    def __str__(self):
        return f"Alert({self.id}, {self.status}, {self.distance}, {self.datetime})"
    
    
    
    def save(self,*args,**kwargs):
        if self.status=='active':
            # account_sid = 'ACd1c1e5e1b7488681d97a307a7e2a7fcf'
            account_sid = 'ACffa65e57cb5782a0a2351bcdac028d30'
            auth_token = '8c2a947ffaa3ef425b2d53e3c7b5a4cd'
            client = Client(account_sid, auth_token)
            phone_numbers = PhoneNumber.objects.values_list('phone_number', flat=True)
            animal_name = animal_mapping.get(self.board_id, "Unknown Animal")
            try:
                message = client.messages.create(
                  from_='+13612735675',
                  body=f'Its an Emergency...Alert!!! an {animal_name}  is out of region from forest please Be Alert. By  Wildtrack System ',
                  to=phone_numbers
                )

                print(message.sid)
            except Exception as e:
                pass
        return super().save(*args,**kwargs)
    
from django.core.validators import RegexValidator

class PhoneNumber(models.Model):
    phone_number = models.CharField(
        max_length=15,  # Accommodates international formats
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Regex for phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
        unique=True,  # Ensures no duplicate numbers
    )

    def __str__(self):
        return self.phone_number
    
    
class DeletedAlert(models.Model):
    board_id = models.IntegerField()
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DeletedAlert(board_id={self.board_id}, deleted_at={self.deleted_at})"


