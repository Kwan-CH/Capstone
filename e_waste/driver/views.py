from django.shortcuts import render, redirect, get_object_or_404
from database.models import Driver, ScheduleRequest, PickedUpRequest, CompletedRequest, Customer
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.timezone import now
import json
import re



def homepage_driver(request):
    return render(request, 'driver/homepage-driver.html')

def pickup_details(request):
    driverID = request.session.get("user_id")
    pickups = ScheduleRequest.objects.filter(driver_id=driverID, status="Approved").order_by('date', 'time') #Sort by closest date and time
    return render(request, 'driver/pickupDetails.html', {'pickups': pickups})

@require_POST
def update_pickup_status(request, requestID):
    try:
        pickUpRequest = ScheduleRequest.objects.get(requestID=requestID)
        pickUpRequest.status = "Picked Up"
        pickUpRequest.save()

        customer = Customer.objects.get(customerID=pickUpRequest.customer.customerID)
        customer.points += (pickUpRequest.category.pointsGiven * pickUpRequest.quantity)
        customer.save()

        PickedUpRequest.objects.create(requestID=pickUpRequest)

        messages.success(request, f"Pickup request {requestID} has been updated successfully!")
        return JsonResponse({'status': 'success'})
    except ScheduleRequest.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Pickup not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def complete_pickup(request):
    driverID = request.session.get("user_id")
    pickups = ScheduleRequest.objects.filter(driver_id=driverID, status="Picked Up").order_by('-date', '-time') #Sort by closest date and time
    return render(request, 'driver/completePick.html', {'pickups': pickups})

@csrf_protect  # Allow AJAX to send requests
def update_complete_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            request_ids = data.get("request_ids", [])  # Get request IDs from AJAX

            if not request_ids:
                return JsonResponse({"success": False, "error": "No requests selected."}, status=400)

            # Update the status of selected requests
            requests_to_complete = ScheduleRequest.objects.filter(requestID__in=request_ids)
            requests_to_complete.update(status="Completed")
            for request in requests_to_complete:
                CompletedRequest.objects.get_or_create(requestID=request)

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

def pickup_history(request):
    driverID = request.session.get("user_id")
    pickups = ScheduleRequest.objects.filter(driver_id=driverID, status="Completed").order_by('-date', '-time') #Sort by closest date and time
    return render(request, 'driver/pickupHis.html', {"pickups": pickups})

def user_profile(request):
    # get logged in driver id
    driverID = request.session.get("user_id")
    userInfo = Driver.objects.get(driverID=driverID)
    return render(request, "driver/userprofile-driver.html", {"profile": userInfo})

def edit_profile(request):
    driverID = request.session.get("user_id")
    userInfo = Driver.objects.get(driverID=driverID)

    if request.method == 'POST':
        new_name = request.POST.get('fullname')
        new_email = request.POST.get('email')
        new_phoneNumber = request.POST.get('contact_number')
        new_address = request.POST.get('address')
        new_state = request.POST.get('state')

        # Check if any field is empty
        if not new_name or not new_email or not new_phoneNumber or not new_address or not new_state :
            return render(request, 'driver/edituserprofile-driver.html', {
                'Invalid': True,
                'error_message': "All fields must be filled",
                'profile': userInfo,  # Pass back the profile details and state selection
                'states': ['Johor', 'Kedah', 'Kelantan', 'Kuala Lumpur', 'Labuan', 'Melaka',
                           'Negeri Sembilan', 'Pahang', 'Perak', 'Perlis', 'Pulau Pinang', 'Sabah', 'Sarawak',
                           'Selangor', 'Terengganu', 'Putrajaya']
            })

        # Validate email
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+$", new_email):
             return render(request, "driver/edituserprofile-driver.html", {
                "profile": userInfo,
                "Invalid": True,
                "error_message": "Invalid email format. Please enter a valid email.",
            })

        # Validate Phone Number
        if not new_phoneNumber.isdigit():
            return render(request, "driver/edituserprofile-driver.html", {
                "profile": userInfo,
                "phone_error": True,
                "states" : ['Johor', 'Kedah', 'Kelantan', 'Kuala Lumpur', 'Labuan', 'Melaka',
                            'Negeri Sembilan', 'Pahang', 'Perak', 'Perlis', 'Pulau Pinang', 'Sabah', 'Sarawak',
                            'Selangor', 'Terengganu', 'Putrajaya']
            })

        # if Validate passes only update userinfo
        userInfo.name = new_name
        userInfo.email = new_email
        userInfo.phoneNumber = new_phoneNumber
        userInfo.addressr = new_address
        userInfo.state = new_state

        # update the corresponding data
        userInfo.save()
        return render(request, "driver/edituserprofile-driver.html", {
            "profile": userInfo,
            "update_success": True
        })

    # reason to create a list at here, is to populate the option field while being able to set selected category
    states = ['Johor', 'Kedah', 'Kelantan', 'Kuala Lumpur', 'Labuan', 'Melaka',
              'Negeri Sembilan', 'Pahang', 'Perak', 'Perlis', 'Pulau Pinang', 'Sabah', 'Sarawak',
              'Selangor', 'Terengganu', 'Putrajaya']
    return render(request, "driver/edituserprofile-driver.html", {"profile": userInfo, "states": states})

#function for getting user address
def get_user_address(request):
    # Get the user_id from session
    user_id = request.session.get("user_id")

    if not user_id:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    try:
        # Fetch driver using session user_id
        driver = Driver.objects.get(driverID=user_id)
        return JsonResponse({"address": driver.address})
    except Driver.DoesNotExist:
        return JsonResponse({"error": "Address not found"}, status=404)



def edit_password(request):
    driverID = request.session.get("user_id")
    driver = Driver.objects.get(driverID=driverID)
    if request.method == "POST":
        current_password_input = request.POST['currentPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['confirmPassword']

        #Check if all field is entered
        if not current_password_input or not new_password or not confirm_password:
            return render(request, 'driver/editpassword-driver.html', {
                'Invalid': True,
                'error_message': "All fields must be filled"
            })

         # Check if the current password matches
        if driver.password != current_password_input:
            return render(request, 'driver/editpassword-driver.html', {
                'Invalid': True,
                'error_message': "Current password is incorrect"
            })

         # Check if new password matches confirm password
        if new_password != confirm_password:
            return render(request, 'driver/editpassword-driver.html', {
                'Invalid': True,
                'error_message': "New password and confirm password do not match"
            })

       
        # Then check if the password length is atleast 8 char
        if len(new_password) < 8:
            # messages.error(request, "Password must be at least 8 characters long")
            return render(request, 'driver/editpassword-driver.html',  {'Invalid': True, 'error_message': "Password must be at least 8 characters long"})


  # If all checks pass, update the password
        Driver.objects.filter(driverID=driverID).update(password=new_password)
        messages.success(request, "Password has been changed successfully")
        return render(request, "driver/editpassword-driver.html", {
            "profile": driver,
            "update_success": True
        })

       

    return render(request, 'driver/editpassword-driver.html')



def logout(request):
    request.session.flush()
    return redirect('e_waste: landing')
