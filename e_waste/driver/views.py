from django.shortcuts import render, redirect, get_object_or_404
from database.models import Driver, ScheduleRequest, PickedUpRequest, CompletedRequest
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.timezone import now
import json

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
    # get logged in customer id
    driverID = request.session.get("user_id")
    userInfo = Driver.objects.get(driverID=driverID)
    return render(request, "driver/userprofile-driver.html", {"profile": userInfo})

def edit_profile(request):
    driverID = request.session.get("user_id")
    # userInfo = Driver.objects.get(driverID=driverID)

    try:
        userInfo = Driver.objects.get(driverID=driverID)
        print(f"DEBUG: Retrieved user - Name: {userInfo.name}, Email: {userInfo.email}")
    except Driver.DoesNotExist:
        print("DEBUG: No driver found for this ID.")
        return HttpResponse("Driver not found", status=404)

    if request.method == 'POST':
        userInfo.name = request.POST.get('fullname')
        userInfo.email = request.POST.get('email')
        userInfo.phoneNumber = request.POST.get('contact_number')
        userInfo.address = request.POST.get('address')
        userInfo.stateCovered = request.POST.get('state')

        # update the corresponding data
        userInfo.save()

        return render(request, "driver/userprofile-driver.html", {"profile": userInfo, "update_success": True})

    # reason to create a list at here, is to populate the option field while being able to set selected category
    states = ['Johor', 'Kedah', 'Kelantan', 'Kuala Lumpur', 'Labuan', 'Melaka',
              'Negeri Sembilan', 'Pahang', 'Perak', 'Perlis', 'Pulau Pinang', 'Sabah', 'Sarawak',
              'Selangor', 'Terengganu', 'Putrajaya']

    return render(request, "driver/edituserprofile-driver.html", {"profile": userInfo, "states": states})

def edit_password(request):
    driverID = request.session.get("user_id")
    driver = Driver.objects.get(driverID=driverID)
    if request.method == "POST":
        current_password_input = request.POST['currentPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['confirmPassword']

        if len(new_password) < 8:
            return render(request, 'driver/editpassword-driver.html', {'Invalid':True})

        if driver.password != current_password_input:
            messages.error(request, "Incorrect current password.")
            return render(request, "driver/editpassword-driver.html")

        if driver.password == current_password_input and new_password == confirm_password:
            Driver.objects.filter(driverID=driverID).update(password=new_password)
            messages.success(request, "Password has been changed successfully")
            return render(request, "driver/userprofile-driver.html", {"profile": driver, "update_success": True})

    return render(request, 'driver/editpassword-driver.html')


def logout(request):
    request.session.flush()
    return redirect('e_waste: landing')
