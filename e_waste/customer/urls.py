from django.urls import path
from .views import index, schedule_pickup, homepage_customer, pickup_status
#from .views import reward_points, recent_activity, profile

app_name = 'customer'

urlpatterns = [
    path('', homepage_customer, name='homepage-customer'), #Customer Homepage
    # path('homepage-customer/', homepage_customer, name='homepage-customer'), #Customer Homepage

    path('schedule_pickup/', schedule_pickup, name='schedule_pickup'), #Schedule Pickup
    # path('reward_points/', reward_points, name='reward_points'), #Reward Points (WAIT)
    path('pickup_status/', pickup_status, name='pickup_status'), #Pickup Status
    # path('recent_activity/', recent_activity, name='recent_activity'), #Recent Activity
    # path('profile/', profile, name='profile'), #Customer Profile

]