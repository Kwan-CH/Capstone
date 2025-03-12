from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from database.models import Customer, PickupRequest, ItemCategory
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
    deliveries = PickupRequest.objects.filter(customer__customerID=customer_id)
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
        pickup_request = PickupRequest(
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


# def reward_points(request):
#     return render(request, 'customer/redeemRewards.html')




# def recent_activity(request):
#     return render(request, 'customer/xxx.html')

def logout(request):
    request.session.flush()
    return redirect('landing')