
from django.shortcuts import render, redirect
from django.contrib import messages
from database.models import Driver, PickupRequest, Reason
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse



def homepage_operator(request):
    return render(request, 'e_waste_operator/operator-homepage.html')

def manageReq(request):
    requests = PickupRequest.objects.all()
    return render(request, 'e_waste_operator/operator-manageReq.html',{'requests': requests})

def update_request_status(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        name = data.get("name")
        status = data.get("status")

        try:
            request_obj = PickupRequest.objects.get(customer__name=name)
            request_obj.status = status
            request_obj.save()
            return JsonResponse({"success": True})
        except PickupRequest.DoesNotExist:
            return JsonResponse({"success": False, "error": "Request not found."})


def operator_createacc(request):

    if request.method =='POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phone_number']
        state_covered = request.POST.get('state_covered')
        car_plate = request.POST['car_plate']
        print(f"🔹 Received Data: Name={full_name}, Email={email}, Phone={phone_number}, State={state_covered}, Plate={car_plate}")

        # Check if email already exists
        if Driver.objects.filter(email=email).exists():
            messages.error(request, 'Email address already exists.')
            return redirect('createacc')

    
        if len(password) < 8:
            return render(request, "e_waste_operator/operator-createacc.html", {"error": "Password is too short!"})

        if not phone_number.isdigit():
            return render(request, "e_waste_operator/operator-createacc.html", {"error": "Invalid contact number!"})
        
        if not state_covered:
            messages.error(request, "Please select your state.")
            return redirect('createacc')

        new_user = Driver(name=full_name, email=email, password=password,phoneNumber=phone_number, plateNumber=car_plate, stateCovered=state_covered)
        new_user.save()

        
        return redirect('e_waste_operator:operator-homepage')
    return render(request, 'e_waste_operator/operator-createacc.html')