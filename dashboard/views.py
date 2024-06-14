from django.shortcuts import render, redirect, get_object_or_404
from .models import AccountBalance, Transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseServerError
from django.urls import reverse
from decimal import Decimal
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
# from paystackapi.transaction import Transaction
import requests





def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to home page after successful login
        else:
            # Handle invalid login
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')  # Changed to password1
        password2 = request.POST.get('password2')
        
        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')  
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('register')  # Redirect back to registration page

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please choose a different one.")
            return redirect('register') 
        
        # Create the user if username is available
        user = User.objects.create_user(username=username, email=email, password=password1)  # Changed to password1
        messages.success(request, "Account registered successfully!")
        return redirect('login')  # Redirect to login page after successful registration
    
    return render(request, 'register.html') 

@login_required(login_url='login')
def index(request):
    # Retrieve or create the account balance object for the current user
    account_balance, created = AccountBalance.objects.get_or_create(user=request.user)

    # Call the transaction handling functions (assuming deposit and transfer are defined elsewhere)
    deposit(request)
    transfer(request)

    # Pass the balance amount to the context
    context = {
        'balance_amount': account_balance.balance_amount,
    }

    # Render the index.html template with the context
    return render(request, 'index.html', context)

@login_required(login_url='login')    
def transfer(request):
    

    return render(request, 'transfer.html')
@login_required(login_url='login')
def recipient(request, username):
    recipient_user = get_object_or_404(User, username=username)
    current_user_balance = AccountBalance.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        transfer_amt = Decimal(request.POST.get('transfer', 0))
        
        if current_user_balance.balance_amount >= transfer_amt:
            # Deduct amount from current user's balance
            current_user_balance.balance_amount -= transfer_amt
            current_user_balance.save()

            # Add amount to recipient's balance
            recipient_balance, _ = AccountBalance.objects.get_or_create(user=recipient_user)
            recipient_balance.balance_amount += transfer_amt
            recipient_balance.save()

            # Store sender, receiver, and amount in session
            request.session['sender_username'] = request.user.username
            request.session['receiver_username'] = recipient_user.username
            request.session['amount'] = str(transfer_amt)
            
            # Redirect to transaction success page
            return redirect('transaction_success')
        else:
            messages.error(request, 'Insufficient balance!')

    context = {
        'recipient_username': recipient_user.username,
        'username': username,
        'account_balance': current_user_balance.balance_amount
    }
    return render(request, 'recipient.html', context)

@login_required(login_url='login')
def initiate_transaction(request, sender_username, receiver_username, amount):
    # Assuming sender and receiver are User instances
    sender = request.user
    receiver = User.objects.get(username=receiver_username)
    
    # Store transaction data in session
    request.session['sender_id'] = sender.id
    request.session['receiver_id'] = receiver.id
    request.session['amount'] = amount
    
    # Redirect to transaction success page
    return redirect('transaction_success')

@login_required(login_url='login')
def transaction_success(request):
    # Retrieve sender_username, receiver_username, and amount from session
    sender_username = request.session.get('sender_username')
    receiver_username = request.session.get('receiver_username')
    amount = request.session.get('amount')
    
    # Retrieve sender and receiver objects
    sender = User.objects.get(username=sender_username)
    receiver = User.objects.get(username=receiver_username)
    
    # Create transaction object
    transaction = Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
    
    # Generate receipt URL (this can be a link to a PDF file)
    receipt_url = "URL_TO_YOUR_RECEIPT_PDF_FILE"
    
    # Render template with transaction details and receipt URL
    template = loader.get_template('transaction_success.html')
    context = {
        'transaction': transaction,
        'receipt_url': receipt_url,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def fetch_users(request):
    if request.method == 'GET' and 'username' in request.GET:
        username = request.GET.get('username')
        users = User.objects.filter(username__icontains=username).values('username')
        user_list = list(users)
        return JsonResponse(user_list, safe=False)
    else:
        users = User.objects.all()
        return render(request, 'recipient.html', {'users': users})

@login_required(login_url='login')
def deposit(request):
    if request.method == 'POST':
        deposit_amt = Decimal(request.POST.get('deposit', 0))

        account_balance, created = AccountBalance.objects.get_or_create(user=request.user)
        
        # Update the account balance with the deposit amount
        account_balance.balance_amount += deposit_amt
        account_balance.save()

        # Create a new transaction for the deposit
        transaction = Transaction(sender=request.user, amount=deposit_amt, date=timezone.now())
        transaction.save()

    return render(request, 'deposit.html')

@login_required(login_url='login')
def initiate_deposit(request):
    if request.method == 'POST':
        deposit_amt = Decimal(request.POST.get('deposit', 0))

        # Assuming you have a profile model with phone number
        phone_number = request.user.profile.phone_number if hasattr(request.user, 'profile') else None
        
        # Generate Paystack API URL to create a payment
        paystack_url = 'https://api.paystack.co/dedicated_account'
        headers = {
            'Authorization': 'Bearer {}'.format('sk_test_a8fb8517f9853bdbbd98380f5e3b8a570e47218c'),
            'Content-Type': 'application/json'
        }
        payload = {
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': phone_number,
            'preferred_bank': 'wema-bank',  # You can change the preferred bank here
            'country': 'NG'  # Country code
        }

        # Make a POST request to Paystack API to create a dedicated virtual account
        response = requests.post(paystack_url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['status']:
                account_name = data['data']['account_name']
                account_number = data['data']['account_number']

                # Pass the virtual account details to the template
                return render(request, 'deposit.html', {'account_name': account_name, 'account_number': account_number})
            else:
                return render(request, 'error.html', {'error_message': data.get('message', 'Failed to create virtual account')})
        else:
            return render(request, 'error.html', {'error_message': 'Failed to create virtual account: {}'.format(response.status_code)})
    else:
        # If the request method is not POST, just render the deposit form
        return render(request, 'deposit.html')
def verify_payment(request):
    # Logic to verify payment with Paystack and update user's account balance
    # This part would depend on the Paystack API and how you manage transactions in your system
    pass

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='login')
def history(request):
    try:
        if request.user.is_authenticated:
            # Retrieve or create AccountBalance for the authenticated user
            account_balance, created = AccountBalance.objects.get_or_create(user=request.user)
            
            # Retrieve and order transaction history for the authenticated user
            transaction_history = Transaction.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-date')
            
            return render(request, 'history.html', {'account_balance': account_balance, 'created': created, 'transaction_history': transaction_history})
        else:
            return HttpResponseServerError("User is not authenticated.")
    except AccountBalance.DoesNotExist:
        return HttpResponseServerError("Account balance not found for the authenticated user.")
    except Transaction.DoesNotExist:
        return HttpResponseServerError("Transaction history not found for the authenticated user.")
    except Exception as e:
        return HttpResponseServerError("An error occurred: {}".format(str(e)))

def settings(request):
    

    return render(request, 'settings.html')

def update_profile_picture(request):
    if request.method == 'POST':
        # Handle profile picture update logic here
        # Example: save the uploaded image to user's profile picture field
        return redirect('settings')  # Redirect back to settings page after updating profile picture
    else:
        return render(request, 'update_profile_picture.html')  # Render the form to upload profile picture

@login_required
def update_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        
        # Check if the new username is available
        if User.objects.filter(username=new_username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('settings')  # Redirect back to settings page
            
        # Update the username if available
        request.user.username = new_username
        request.user.save()
        messages.success(request, "Username updated successfully!")
        return redirect('settings')  # Redirect back to settings page
    else:
        return render(request, 'update_username.html')  # Render the form to update username

@login_required
def change_password(request):
    if request.method == 'POST':
        # Handle password change logic here
        return redirect('settings')  # Redirect back to settings page after changing password
    else:
        return render(request, 'change_password.html') 

