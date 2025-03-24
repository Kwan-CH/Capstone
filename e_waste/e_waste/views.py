from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from database.models import Customer, Driver, Operator
from .utils import authenticate_user

def signup(request):
    # return render(request, 'e_waste/signup.html')
    if request.method =='POST':
        email = request.POST['email']
        fullname = request.POST['fullname']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        contact_number = request.POST['contact_number']
        address = request.POST['address']
        state = request.POST.get('state')

        # Check if email already exists
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email address already exists.')
            return redirect('signup')

        if not state:
            messages.error(request, "Please select your state.")
            return redirect('e_waste/signup')

        if password != confirm_password:
            return render(request, "e_waste/signup.html", {"error": "Password do not match!"})

        if len(password) < 8:
            return render(request, "e_waste/signup.html", {"error": "Password is too short!"})

        if not contact_number.isdigit():
            return render(request, "e_waste/signup.html", {"error": "Invalid contact number!"})

        new_user = Customer(email=email, name=fullname, password=password,phoneNumber=contact_number, address=address, state=state)
        new_user.save()

         #Store user in session
        request.session['user_id'] = new_user.customerID
        request.session['user_email'] = new_user.email
        request.session['user_role'] = 'customer'

        return redirect('customer:homepage-customer')
    return render(request, 'e_waste/signup.html')

def user_login(request):

    if request.method == 'POST':
        email = request.POST['email_input']
        password = request.POST['password']
        print(email)
        print(password)

        # Authenticate using the email field
        user = authenticate_user(email=email, password=password)
        print (user)

        if user is not None:
            # login(request, user)  # Logs the user in
            print(f"Logged in as {request.user}")

            # Check if the user is a Customer
            if Customer.objects.filter(email=email).exists():
                user_role = 'customer'
                user_obj = Customer.objects.get(email=email)
                userID = user_obj.customerID
                redirect_url = 'customer:homepage-customer'
            # Check if the user is a Driver
            elif Driver.objects.filter(email=email).exists():
                user_role = 'driver'
                user_obj = Driver.objects.get(email=email)
                userID = user_obj.driverID
                redirect_url = 'driver:homepage-driver'
            # Check if the user is an Operator
            elif Operator.objects.filter(email=email).exists():
                user_role = 'operator'
                user_obj = Operator.objects.get(email=email)
                userID = user_obj.operatorID
                redirect_url = 'operator:homepage-operator'

            # Store user details in session
            request.session['user_id'] = userID
            request.session['user_email'] = user_obj.email
            request.session['user_role'] = user_role
            return redirect(redirect_url)

        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'e_waste/login.html', {"Invalid":True})  # Redirect to login page

    return render(request, 'e_waste/login.html')  # Ensure GET requests return login page

def landing(request):
    return render(request, 'e_waste/landing.html')

