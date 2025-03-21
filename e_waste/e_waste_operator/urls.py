from django.urls import path
from .views import *



app_name = 'operator'

urlpatterns = [
     path('', homepage_operator, name='homepage-operator'), #Operator Homepage
     path('create-driver-acc/', operator_create_acc_page, name='create_acc'),#Create Driver Account
     path('save_driver_account', save_driver_account, name='save_account'),
     path('manageReq/', manageReq, name='manageReq'), #Manage Requests
     path("update_request_status/", update_request_status, name="update_request_status"), #Update Request Status
     path('manageReq/', assign_driver, name='assign_driver'),
     path('reward_system/', reward_system, name='reward_system'), #Reward System
     path('add_reward/', add_reward, name='add_reward'), #Add Reward
     path('edit_reward/<str:voucherID>/', edit_reward, name='edit_reward'), #Add Reward
]