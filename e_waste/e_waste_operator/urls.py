from django.urls import path
from .views import *



app_name = 'e_waste_operator'

urlpatterns = [
     path('', homepage_operator, name='operator-homepage'), #Operator Homepage
     path('createacc/', operator_createacc, name='createacc'), #Pickup Status
     path('manageReq/', manageReq, name='manageReq'), #Manage Requests
     path("update_request_status/", update_request_status, name="update_request_status"), #Update Request Status
]