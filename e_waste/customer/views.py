from django.contrib.admin.templatetags.admin_list import pagination
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from database.models import Customer, ScheduleRequest, ItemCategory, CustomerRedemption, Voucher
from django.core.paginator import Paginator
from django.db.models import F
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator
import json, re
from django.http import JsonResponse


# from .utils import authenticate_user

def index(request):
    return render(request, 'landing.html')

def homepage_customer(request):
    return render(request, 'customer/homepage-customer.html')

@login_required
def pickup_status(request):
    customer_id = request.session.get('user_id')
    if not customer_id:
        return redirect('login')
    pickUpRequest = ScheduleRequest.objects.filter(customer__customerID=customer_id).order_by('-trackingnumber')

    pagination = Paginator(pickUpRequest, 5)
    page = request.GET.get('page')

    deliveries = pagination.get_page(page)

    if not deliveries.object_list:
        return render(request, 'customer/pickupStatus.html', {'Empty': True})

    return render(request, 'customer/pickupStatus.html', {'deliveries': deliveries})

@login_required
def schedule_pickup(request):
    pickup_request = None
    if request.method == 'POST':
        category_id = request.POST.get('waste_type')
        quantity = request.POST.get('quantity_items')
        weight = request.POST.get('quantity_weight')
        address = request.POST.get('address')
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time')

        # Get the logged-in user
        customer_id = request.session.get("user_id")

        if not customer_id:
            return redirect("login")  # Redirect to login if session expired

        try:
            customer = Customer.objects.get(customerID=customer_id)  # Fetch customer object
        except Customer.DoesNotExist:
            messages.error(request, "Customer not found!")
            return redirect("login")

        try:
            category = ItemCategory.objects.get(categoryID=category_id)
        except ItemCategory.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            return redirect('customer:schedule_pickup')

        # Create a new PickupRequest
        pickup_request = ScheduleRequest(
            customer=customer,
            category=category,
            quantity=quantity,
            weight=weight,
            address=address,
            date=pickup_date,
            time=pickup_time,
            status="Pending",
            driver=None,  # Driver will be assigned later
            operator=None  # Operator will be assigned later
        )
        pickup_request.trackingnumber = pickup_request.generate_tracking_number()
        pickup_request.save()

        tracking_number = pickup_request.trackingnumber  # Store tracking number

        messages.success(request, 'Pickup request submitted successfully!')
        # return redirect('customer:schedulePick.html')

        return render(request, 'customer/schedulePick.html', {
            'categories': ItemCategory.objects.all(),
            'submitted': True,
            'tracking_number': tracking_number
        })

    # Handle GET request
    return render(request, 'customer/schedulePick.html', {
        'categories': ItemCategory.objects.all(),
        'submitted': False,  # Ensures no undefined variable usage
        # 'tracking_number': tracking_number
    })

def user_profile(request):
    # get logged in customer id
    customerID = request.session.get("user_id")
    userInfo = Customer.objects.get(customerID=customerID)
    return render(request, "customer/userprofile-customer.html", {"profile": userInfo})

def edit_profile(request):
    customerID = request.session.get("user_id")
    userInfo = Customer.objects.get(customerID=customerID)

    if request.method == 'POST':
        new_name = request.POST.get('fullname')
        new_email = request.POST.get('email')
        new_phoneNumber = request.POST.get('contact_number')
        new_address = request.POST.get('address')
        new_state = request.POST.get('state')

        # Check if any field is empty
        if not new_name or not new_email or not new_phoneNumber or not new_address or not new_state :
            return render(request, 'customer/edituserprofile-customer.html', {
                'Invalid': True,
                'error_message': "All fields must be filled",
                'profile': userInfo,  # Pass back the profile details and state selection
                'states': ['Johor', 'Kedah', 'Kelantan', 'Kuala Lumpur', 'Labuan', 'Melaka',
                           'Negeri Sembilan', 'Pahang', 'Perak', 'Perlis', 'Pulau Pinang', 'Sabah', 'Sarawak',
                           'Selangor', 'Terengganu', 'Putrajaya']
            })

        # Validate email
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+$", new_email):
             return render(request, "customer/edituserprofile-customer.html", {
                "profile": userInfo,
                "Invalid": True,
                "error_message": "Invalid email format. Please enter a valid email.",
            })

        # Validate Phone Number
        if not new_phoneNumber.isdigit():
            return render(request, "customer/edituserprofile-customer.html", {
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
        return render(request, "customer/edituserprofile-customer.html", {
            "profile": userInfo,
            "update_success": True
        })

    # reason to create a list at here, is to populate the option field while being able to set selected category
    states = ['Johor', 'Kedah', 'Kelantan', 'Kuala Lumpur', 'Labuan', 'Melaka',
              'Negeri Sembilan', 'Pahang', 'Perak', 'Perlis', 'Pulau Pinang', 'Sabah', 'Sarawak',
              'Selangor', 'Terengganu', 'Putrajaya']
    return render(request, "customer/edituserprofile-customer.html", {"profile": userInfo, "states": states})

#function for getting user address
def get_user_address(request):
    # Get the user_id from session
    user_id = request.session.get("user_id")

    if not user_id:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    try:
        # Fetch customer using session user_id
        customer = Customer.objects.get(customerID=user_id)
        return JsonResponse({"address": customer.address})
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Address not found"}, status=404)

def edit_password(request):
    customerID = request.session.get("user_id")
    customer = Customer.objects.get(customerID=customerID)
    if request.method == "POST":
        current_password_input = request.POST['currentPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['confirmPassword']

        #Check if all field is entered
        if not current_password_input or not new_password or not confirm_password:
            return render(request, 'customer/editpassword-customer.html', {
                'Invalid': True,
                'error_message': "All fields must be filled"
            })

         # Check if the current password matches
        if customer.password != current_password_input:
            return render(request, 'customer/editpassword-customer.html', {
                'Invalid': True,
                'error_message': "Current password is incorrect"
            })

         # Check if new password matches confirm password
        if new_password != confirm_password:
            return render(request, 'customer/editpassword-customer.html', {
                'Invalid': True,
                'error_message': "New password and confirm password do not match"
            })

        #---------OLD-VERSION------
        # if customer.password == current_password_input and new_password == confirm_password:
        #     Customer.objects.filter(customerID=customerID).update(password=new_password)
        #     # messages.success(request, "Password has been changed successfully")
        #     return render(request, "customer/userprofile-customer.html", {"profile": customer, "update_success": True})

        # Then check if the password length is atleast 8 char
        if len(new_password) < 8:
            # messages.error(request, "Password must be at least 8 characters long")
            return render(request, 'customer/editpassword-customer.html',  {'Invalid': True, 'error_message': "Password must be at least 8 characters long"})


  # If all checks pass, update the password
        Customer.objects.filter(customerID=customerID).update(password=new_password)
        messages.success(request, "Password has been changed successfully")
        return render(request, "customer/editpassword-customer.html", {
            "profile": customer,
            "update_success": True
        })

        # messages.error(request, "Password does not match or is incorrect")
        # return render(request, 'customer/editpassword-customer.html', {'Invalid': True})

    return render(request, 'customer/editpassword-customer.html')

def recent_activity(request):
    return render(request, 'customer/xxx.html')

def waste_category(request):
    return render(request, 'customer/wasteCategory.html')

def history_all(request):
    customerID = request.session.get('user_id')
      # Get device recycling history
    device_history = (ScheduleRequest.objects.filter(~Q(status='Pending'), customer__customerID=customerID)
                      .select_related('category')
                      .values('trackingnumber', 'address', 'category__itemType', 'date', 'quantity', 'status', 'rejectedReason__reason')
                      .annotate(total=F('quantity') * F('category__pointsGiven'))
                      .order_by('-date')  # Sort by date (latest first)
                      )

    # Get voucher redemption history
    voucher_history = (CustomerRedemption.objects.filter(customer__customerID=customerID, status=False)
                       .select_related('voucher')
                       .values('voucher__voucherID', 'voucher__name', 'date', 'time', 'voucher__pointsRequired')
                       .order_by('-date', '-time')  # Sort by date (latest first, then by time)
                       )

    # Combine both lists
    combined_history = list(chain(device_history, voucher_history))

    # Sort by date (latest first)
    combined_history.sort(key=lambda x: x['date'], reverse=True)

    # Paginate combined history
    pagination = Paginator(combined_history, 4)  # 4 items per page
    page = request.GET.get('page')
    activities = pagination.get_page(page)

    # If no activity data available, show empty message
    if not activities.object_list:
        return render(request, 'customer/activityHis-All.html', {"Empty": True})

    return render(request, 'customer/activityHis-All.html', {"activities": activities})

def device_recycled(request):
    customerID = request.session.get('user_id')

    # select the pickup request that the customer made, while retrieve the item type based on categoryID
    # reason using small 'c' in customer is because it is not referring to the table but refer to the field itself
    # same goes to the select_relate(), it refers to the field not table
    pickup_requests = (ScheduleRequest.objects.filter(~Q(status='Pending'), customer__customerID=customerID)
                        # ~Q functions to exclude condition specified
                       .select_related('category')
                       .values('trackingnumber', 'address', 'category__itemType', 'date', 'quantity', 'status', 'rejectedReason__reason')
                       .annotate(total=F('quantity') * F('category__pointsGiven')) #this here is to calculate the total points using F()
                       .order_by('-trackingnumber') # order by desc tracking number, later on after the data is finalised, changed back to date
                        )


    pagination = Paginator(pickup_requests, 4) # limit 4 data per page
    page = request.GET.get('page') #keep track on what page is the user in

    #some sort like put all data into the size we set and ready to be use in a loop
    devices = pagination.get_page(page)

    if not devices.object_list:
        return render(request, 'customer/activityHis-Device.html', {"Empty": True})

    return render(request, 'customer/activityHis-Device.html', {"historyPages": devices})

def voucher_redeemed(request):
    customerID = request.session.get('user_id')

    vouchers_redeemed = (CustomerRedemption.objects.filter(customer__customerID=customerID, status=False).select_related('voucher')
                         .values('voucher__voucherID', 'voucher__name', 'date', 'time', 'voucher__pointsRequired')
                         .order_by('-time')
                         )

    pagination = Paginator(vouchers_redeemed, 4)
    page = request.GET.get('page')

    vouchers = pagination.get_page(page)

    if not vouchers.object_list:
        return render(request, 'customer/activityHis-Point.html', {"Empty": True})

    return render(request, 'customer/activityHis-Point.html', {'vouchers':vouchers})

def logout(request):
    request.session.flush()
    return redirect('e-waste: landing')

def redeem_rewards_page(request): # need to add paginator in the future to consider the case of too much voucher
    customerID = request.session.get('user_id')
    customerPoint = Customer.objects.filter(customerID=customerID).values_list('points', flat=True).first()

    vouchersAvailable = Voucher.objects.all().filter(quantity__gt=0).order_by('voucherID')
    pagination = Paginator(vouchersAvailable, 4)
    page = request.GET.get('page')

    vouchers = pagination.get_page(page)

    if not vouchers.object_list:
        return render(request, 'customer/redeemRewards.html', {"Empty": True, 'points':customerPoint})

    return render(request, 'customer/redeemRewards.html', {'vouchers':vouchers, 'points':customerPoint})

def redeem_voucher(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            voucherID = data.get("reward")
            points_required = data.get("points")

            customerID = request.session.get('user_id')
            customer = Customer.objects.get(customerID=customerID)
            voucher = Voucher.objects.get(voucherID=voucherID)

            # check if customer have enough points
            if customer.points < points_required:
                return JsonResponse({"success": False, "message": "Not enough points."}, status=400)

            customer.points -=points_required
            customer.save()
            voucher.quantity -= 1
            voucher.save()

            print("save pending")
            redemption = CustomerRedemption.objects.create(customer=customer, voucher=voucher, status=False)
            print("saved")
            redemption.save()
            return JsonResponse({"success": True, "message": "Voucher redeemed successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)