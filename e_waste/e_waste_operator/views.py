
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from database.models import Driver, PickupRequest, Reason, Voucher
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse



def homepage_operator(request):
    return render(request, 'operator/operator-homepage.html')

def manageReq(request):
    requests = PickupRequest.objects.all()
    return render(request, 'operator/operator-manageReq.html',{'requests': requests})

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


def operator_create_acc_page(request):
    states = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan",
              "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak",
              "Selangor", "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya"]
    return render(request, 'operator/operator-create_acc.html', {"states":states})

def save_driver_account(request):
    states = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan",
              "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak",
              "Selangor", "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya"]

    if request.method == 'POST':
        name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        contact = request.POST['phone_number']
        state = request.POST.get('state_covered')
        carPlate = request.POST['car_plate']

        # Check if email already exists
        if Driver.objects.filter(email=email).exists():
            messages.error(request, "Email existed in the database already, please try a new one")
            return render(request, 'operator/operator-create_acc.html',{"formData": request.POST, "states":states})

        if len(password) < 8:
            messages.error(request, "Password is too short, minimum length is 8")
            return render(request, 'operator/operator-create_acc.html',{"formData": request.POST, "states":states})

        if not contact.isdigit():
            messages.error(request, "Contact number should not have alphabet")
            return render(request, 'operator/operator-create_acc.html',{"formData": request.POST, "states":states})

        if not state:
            messages.error(request, "PLease select a state before proceeding")
            return render(request, 'operator/operator-create_acc.html',{"formData": request.POST, "states":states})

        new_user = Driver(name=name, email=email, password=password,phoneNumber=contact, plateNumber=carPlate, stateCovered=state)
        new_user.save()

        return render(request, 'operator/operator-create_acc.html', {"Success":True, "states":states})

    return render(request, 'operator/operator-create_acc.html', {"states":states})


def reward_system(request):
    vouchers = Voucher.objects.all()
    return render(request, 'operator/operator-rewardSystem.html', {"vouchers":vouchers})

# def add_reward(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         pointsRequired = request.POST.get('pointsRequired')
#         quantity = request.POST.get('quantity')

#         # Save the new voucher
#         voucher = Voucher(name=name, pointsRequired=int(pointsRequired), quantity=int(quantity))
#         voucher.save()

#         return render(request, 'operator/operator-addReward.html')

#     return render(request, 'operator/operator-addReward.html')

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
        return render(request, 'operator/operator-addReward.html')

    return render(request, 'operator/operator-addReward.html')


from django.core.exceptions import ValidationError

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
        return render(request, 'operator/operator-editReward.html', {"voucher": voucher})

    return render(request, 'operator/operator-editReward.html', {"voucher": voucher})

def assign_driver(request):
    return render(request, 'operator/assign-driver.html')