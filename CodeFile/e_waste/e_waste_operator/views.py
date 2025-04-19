from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from database.models import Driver, ScheduleRequest, Reason, Voucher, Operator
# CompletedRequest
from django.db.models import Q, Case, CharField, Value, When, F
from django.db.models.functions import Concat
from utilities.Email import emailAutomation
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from itertools import chain
from utilities.state_data import getState

import os
from dotenv import load_dotenv

load_dotenv()

states=getState.getState()

excluded_states = ['Kuala Lumpur', 'Putrajaya', 'Labuan']

#centralised all request.get.session()
def get_userID_from_session(request):
    return request.session.get('user_id')

def get_profile_picture(request):
    return Operator.objects.only('profile_picture').get(operatorID=get_userID_from_session(request))


def homepage_operator(request):
    return render(request, 'operator/operator-homepage.html', {'operator':get_profile_picture(request)})

def manageReq(request):
    requests = (
        ScheduleRequest.objects
        .annotate(
            address=Case(
                When(state__in=excluded_states,
                    then=Concat('street', Value(', '), 'postalCode', Value(', '), 'state', output_field=CharField())),
                default=Concat('street', Value(', '), 'postalCode', Value(', '), 'area', Value(', '), 'state', output_field=CharField()),
                output_field=CharField()
            )
        )
        .filter(~Q(status='Completed'), ~Q(status='Rejected'))
        .order_by('-requestID')
    )

    reasons = Reason.objects.all()

    paginator = Paginator(requests, 5)
    page = request.GET.get('page')
    requests = paginator.get_page(page)

    return render(request, 'operator/operator-manageReq.html',{
        'requests': requests,
        'reasons':reasons,
        'operator': get_profile_picture(request)
        })

def update_request_status(requestID):
    pickUpRequest = ScheduleRequest.objects.filter(requestID=requestID).first()
    pickUpRequest.status = "Approved"
    pickUpRequest.save()

def assign_driver_page(request):
    requestID = request.GET.get('requestID')
    requestInfo = (ScheduleRequest.objects
                   .annotate(address=Concat('street', Value(', '), 'postalCode',
                                            Value(', '), 'area', Value(', '), 'state', output_field=CharField()))
                   .filter(requestID= requestID).first())
    priority_driver = Driver.objects.filter(areaCovered=requestInfo.area)
    non_priority_driver = Driver.objects.filter(~Q(areaCovered=requestInfo.area))

    drivers = list(chain(priority_driver, non_priority_driver))

    return render(request, 'operator/assign-driver.html', {
        'drivers': drivers,
        'request':requestInfo,
        'operator': get_profile_picture(request)
    })

def assign_driver(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            requestID = data.get('requestID')
            driverID = data.get('driverID')
            if requestID and driverID:
                selectedRequest = (ScheduleRequest.objects
                                   .annotate(address=Concat('street', Value(', '), 'postalCode',
                                                            Value(', '), 'area', Value(', '), 'state',
                                                            output_field=CharField()))
                                   .filter(requestID=requestID).first())
                driver = Driver.objects.filter(driverID=driverID).first()
                operator = Operator.objects.filter(operatorID = get_userID_from_session(request)).first()
                selectedRequest.driver = driver
                selectedRequest.operator = operator
                selectedRequest.save()
                update_request_status(requestID)
                emailAutomation.sendEmail('driver_assignment', selectedRequest.customer.email,
                                         context={
                                             'driver':driver,
                                             'request':selectedRequest
                                         })
                return JsonResponse({'success': True, 'message': 'Driver assigned successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Something went wrong'}, status=400)
        except Exception as e:
            return JsonResponse({'success':False, 'message':f'{str(e)}'}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

def reject_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            requestID = data.get('selectedRequest')
            reasonID = data.get('selectedReason')
            if requestID and reasonID:
                selectedRequest = ScheduleRequest.objects.filter(requestID=requestID).first()
                reason = Reason.objects.filter(reasonID=reasonID).first()
                operator = Operator.objects.filter(operatorID=get_userID_from_session(request)).first()
                selectedRequest.rejectedReason = reason
                selectedRequest.status = 'Rejected'
                selectedRequest.operator = operator
                selectedRequest.save()
                return JsonResponse({'success': True})
                # return redirect('operator:manageReq')
            else:
                return JsonResponse({'success': False, 'message': 'Something went wrong'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'{str(e)}'}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

def operator_create_acc_page(request):
    return render(request, 'operator/operator-create_acc.html', {
        "states":states,
        "API_KEY": os.getenv('GET_STATE_AREA_API'),
        'operator': get_profile_picture(request)
    })

def save_driver_account(request):
    operator = get_profile_picture(request)
    if request.method == 'POST':
        name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        contact = request.POST['phone_number']
        stateCovered = request.POST.get('state_covered')
        areaCovered = request.POST.get('area_covered')
        carPlate = request.POST['car_plate']

        # Check if email already exists
        if Driver.objects.filter(email=email).exists():
            messages.error(request, "Email existed in the database already, please try a new one")
            return render(request, 'operator/operator-create_acc.html',{
                "formData": request.POST,
                "states":states,
                "API_KEY": os.getenv('GET_STATE_AREA_API'),
                'operator': operator
            })

        elif '@' not in email:
            messages.error(request, "Invalid email address")
            return render(request, 'operator/operator-create_acc.html',{
                "formData": request.POST,
                "states":states,
                "API_KEY": os.getenv('GET_STATE_AREA_API'),
                'operator': operator
            })

        elif len(password) < 8:
            messages.error(request, "Password is too short, minimum length is 8")
            return render(request, 'operator/operator-create_acc.html',{
                "formData": request.POST,
                "states":states,
                "API_KEY": os.getenv('GET_STATE_AREA_API'),
                'operator': operator
            })

        elif not contact.isdigit() or not contact.startswith("01") or len(contact) not in [10,11]:
            messages.error(request, "Please enter a valid phone number")
            return render(request, "operator/operator-create_acc.html", {
                "formData": request.POST,
                "states":states,
                "API_KEY": os.getenv('GET_STATE_AREA_API'),
                'operator': operator
        })

        elif not stateCovered:
            messages.error(request, "Please select a state before proceeding")
            return render(request, 'operator/operator-create_acc.html',{
                "formData": request.POST,
                "states":states,
                "API_KEY": os.getenv('GET_STATE_AREA_API'),
                'operator': operator
            })

        elif stateCovered not in excluded_states and not areaCovered:
            messages.error(request, "Please select an area before proceeding")
            return render(request, 'operator/operator-create_acc.html',{
                "formData": request.POST,
                "states":states,
                "API_KEY": os.getenv('GET_STATE_AREA_API'),
                'operator': operator
            })

        new_user = Driver(name=name,
                          email=email,
                          password=password,
                          phoneNumber=contact,
                          plateNumber=carPlate,
                          stateCovered=stateCovered,
                          areaCovered=areaCovered)
        new_user.save()

        return render(request, 'operator/operator-create_acc.html', {
            "Success":True,
            "states":states,
            "API_KEY": os.getenv('GET_STATE_AREA_API'),
            'operator': operator
        })

    return render(request, 'operator/operator-create_acc.html', {
        "states":states,
        "API_KEY": os.getenv('GET_STATE_AREA_API'),
        'operator': operator
    })

def reward_system(request):
    vouchers = Voucher.objects.all()
    
    paginator = Paginator(vouchers, 6)
    page = request.GET.get('page')
    vouchers = paginator.get_page(page)

    # return render(request, 'operator/operator-manageReq.html',{
    #     'vouchers': vouchers,
    #     })
    return render(request, 'operator/operator-rewardSystem.html', {"vouchers":vouchers, 'operator': get_profile_picture(request)})

def add_reward(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pointsRequired = request.POST.get('pointsRequired')
        quantity = request.POST.get('quantity')

        if Voucher.objects.filter(name=name).exists():
            return JsonResponse({'status': 'error', 'message': 'A voucher with this name already exists.'})

        voucher = Voucher(name=name, pointsRequired=int(pointsRequired), quantity=int(quantity))
        voucher.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Reward updated successfully!'})

        messages.success(request, 'Reward updated successfully!')
        return render(request, 'operator/operator-addReward.html', {'operator': get_profile_picture(request)})

    return render(request, 'operator/operator-addReward.html', {'operator': get_profile_picture(request)})

def edit_reward(request, voucherID):
    voucher = get_object_or_404(Voucher, voucherID=voucherID)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        pointsRequired = request.POST.get('pointsRequired', '').strip()
        quantity = request.POST.get('quantity', '').strip()

        # Update the voucher fields
        voucher.name = name
        voucher.pointsRequired = int(pointsRequired)
        voucher.quantity = int(quantity)
        voucher.save()

        # Handle AJAX requests separately
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Reward updated successfully!'})

        messages.success(request, 'Reward updated successfully!')
        return render(request, 'operator/operator-editReward.html', {"voucher": voucher, 'operator': get_profile_picture(request)})

    return render(request, 'operator/operator-editReward.html', {"voucher": voucher, 'operator': get_profile_picture(request)})

def completed_request(request):
    operatorID = get_userID_from_session(request)

    completedRequests = (
        ScheduleRequest.objects
        .filter(operator__operatorID=operatorID, status="Completed")
        .exclude(completed_date__isnull=True)
        .exclude(completed_time__isnull=True)
        .select_related('customer', 'category')  # optimize joins
        .values(
            'customer__name',
            'completed_date',
            'completed_time',
            'category__itemType'
        )
        .annotate(
            address=Case(
                When(state__in=excluded_states,
                    then=Concat(
                        F('street'), Value(', '),
                        F('postalCode'), Value(', '),
                        F('state'),
                        output_field=CharField()
                    )),
                default=Concat(
                    F('street'), Value(', '),
                    F('postalCode'), Value(', '),
                    F('area'), Value(', '),
                    F('state'),
                    output_field=CharField()
                ),
                output_field=CharField()
            )
        )
        .order_by('-completed_date', 'completed_time')
    )

    paginator = Paginator(completedRequests, 5)
    page = request.GET.get('page')
    completedRequests = paginator.get_page(page)

    return render(request, 'operator/operator-completedReq.html', {'completedRequests':completedRequests, 'operator': get_profile_picture(request)})
    # return render(request, 'operator/operator-completedReq.html')

def user_profile(request):
    operator = Operator.objects.get(operatorID=get_userID_from_session(request))

    if request.method == 'POST' and request.FILES.get('profile_picture'):

        # ✅ Only delete old picture IF a new one is uploaded
        if operator.profile_picture and operator.profile_picture.name != "profile_pics/default.jpg":
            operator.profile_picture.delete(save=False)

        # ✅ Save the new profile picture
        operator.profile_picture = request.FILES['profile_picture']
        operator.save()

        return JsonResponse({
            'new_profile_picture_url': operator.profile_picture.url
        })
    return render(request, 'operator/userprofile-operator.html', {'operator':operator})

def edit_profile(request):
    operator = Operator.objects.get(operatorID=get_userID_from_session(request))

    if request.method == 'POST':
        new_name = request.POST['name'].strip()
        new_email = request.POST['email'].strip()

        duplicate_email = Operator.objects.filter(email=new_email).exists()
        if duplicate_email:
            return render(request, 'operator/edituserprofile-operator.html', {'duplicate_email': True, 'operator': operator})

        operator.name = new_name
        operator.email = new_email

        operator.save()

        return render(request, 'operator/userprofile-operator.html', {'operator':operator, 'profile':True})

    return render(request, 'operator/edituserprofile-operator.html', {'operator': operator})

def edit_password(request):
    operator = Operator.objects.get(operatorID=get_userID_from_session(request))

    if request.method == 'POST':

        current_password = request.POST['current']
        new_password = request.POST['new']
        confirm_password = request.POST['confirm']

        if current_password != operator.password:
            return render(request, 'operator/editpassword-operator.html', {'wrong_current':True})

        if new_password != confirm_password:
            return render(request, 'operator/editpassword-operator.html', {'wrong_confirmation':True})

        operator.password = new_password
        operator.save()

        return render(request, 'operator/userprofile-operator.html', {'password': True, 'operator':operator})

    return render(request, 'operator/editpassword-operator.html', {'operator':operator})
