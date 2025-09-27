from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import *
from .forms import LoginForm, SignupForm

otp_session = {}

@unautheticated_user
def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                user_type = getattr(user, 'user_type', None)

                if user_type == '1':
                    return redirect('/')
                elif user_type == '2':
                    return redirect('pharmacist_home')
                elif user_type == '3':
                    return redirect('doctor_home')
                elif user_type == '4':
                    return redirect('clerk_home')
                elif user_type == '5':
                    return redirect('patient_home')
                else:
                    messages.error(request, "⚠️ Unknown user type.")
                    return redirect('login')
            else:
                messages.error(request, "❌ Invalid username or password.")
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            # phone = form.cleaned_data['phone']
            if password == confirm_password:
                user = User.objects.create_user(username=username, email=email, password=password)
                # user.profile.phone = phone  # if custom User model
                user.save()
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# def loginPage(request):
#     if request.method == 'POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user=authenticate(request,username=username,password=password)
#         if user != None:
#             login(request, user)
#             user_type = user.user_type
#             if user_type == '1':
#                 return redirect('/')
#             elif user_type == '2':
#                 return redirect('pharmacist_home')
#             elif user_type == '3':
#                 return redirect('doctor_home')
#             elif user_type == '4':
#                 return redirect('clerk_home')
#             elif user_type == '5':
#                 return redirect('patient_home')
#             else:
#                 messages.error(request, "Invalid Login!")
#                 return redirect('login')
#         else:
#             messages.error(request, "Invalid Login Credentials!")
#             return redirect('login')    
#     return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def demo(request):
    return render (request,'demo.html')

