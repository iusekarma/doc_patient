from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterationForm
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Patient Account Created')
            return redirect('login')
    else:
        form = UserRegisterationForm()
    return render(request, 'users/register.html', {'form':form, 'form_name':'Patient' })

def register_doctor(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            image = form.cleaned_data.get('image')
            user = User.objects.filter(username=username).first()
            user.profile.is_doctor = True
            user.profile.image = image
            user.profile.save()
            messages.success(request, 'Doctor Account Created')
            return redirect('login')
    else:
        form = UserRegisterationForm()
    return render(request, 'users/register.html', {'form':form, 'form_name':'Doctor' })

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')