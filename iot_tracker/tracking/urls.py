from django.urls import path

from tracking import consumers
from .views import add_animal, add_phone_number, alerts_view, contact_view, dashboard, delete_alert, get_alert_count, login_view, logout_view, receive_data, home, send_safe_message, signup_view

urlpatterns = [
    path('receive-data/', receive_data, name='receive-data'),
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard webpage
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('contact/', contact_view, name='contact'),
    path('alerts/', alerts_view, name='alerts'),
    path('ajax_count/', get_alert_count, name='get_alert_count'), 
    path('delete-alert/<int:alert_id>/', delete_alert, name='delete_alert'),
    path('add-phone-number/', add_phone_number, name='add_phone_number'),
    path('send_safe_message/', send_safe_message, name='send_safe_message'),
    path('add-animal/', add_animal, name='add_animal'),
    # path('ws/alerts/', consumers.AlertConsumer.as_asgi()),
]
