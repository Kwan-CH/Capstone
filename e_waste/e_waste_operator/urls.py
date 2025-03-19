from django.urls import path
from .views import *



app_name = 'operator'

urlpatterns = [
     path('', homepage_operator, name='homepage-operator'), #Operator Homepage
     path('create-driver-acc/', operator_create_acc_page, name='create_acc'),#Create Driver Account
     path('save_driver_account', save_driver_account, name='save_account'),
     path('manageReq/', manageReq, name='manageReq'), #Manage Requests
     path("update_request_status/", update_request_status, name="update_request_status"), #Update Request Status
     path('manageReq/', assign_driver, name='assign_driver')
]