from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm, LoginForm, OTPForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from .utils import send_otp_email#, send_otp_sms
import random

otp_session = {}

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             confirm_password = form.cleaned_data['confirm_password']
#             # phone = form.cleaned_data['phone']
#             if password == confirm_password:
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 # user.profile.phone = phone  # if custom User model
#                 user.save()
#                 return redirect('login')
#             else:
#                 messages.error(request, "Passwords do not match")
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('success')
#             else:
#                 messages.error(request, "❌ Invalid username or password.")
#                 #messages.error(request, "Invalid credentials")
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # phone = request.POST.get('phone')
        user = User.objects.filter(email=email).first()

        if user:
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['reset_email'] = email
            send_otp_email(email, otp)
            # send_otp_sms(phone, otp)

            messages.success(request, "✅ OTP sent successfully!")
            return redirect('verify_otp')
        else:
            messages.error(request, "❌ Email not registered!")
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == request.session.get('otp'):
                return redirect('reset_password')
            #else:
                #messages.error(request, "Invalid OTP")
            else:
                messages.error(request, "❌ Invalid OTP. Please try again.")
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                email = request.session.get('reset_email')
                user = User.objects.filter(email=email).first()

                if user:
                    user.set_password(new_password)
                    user.save()
                    del request.session['otp']
                    del request.session['reset_email']
                    messages.success(request, "✅ Password reset successfully.")
                    return redirect('login')
                else:
                    messages.error(request, "❌ User not found.")
            else:
                messages.error(request, "❌ Passwords do not match.")
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})

# @login_required
# def success(request):
#     return render(request, 'success.html')