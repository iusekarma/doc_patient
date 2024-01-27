from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterationForm, PostCreationForm, EventForm
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Profile
import json, os

CALENDER_API_ID = os.getenv('CALENDER_API_ID')
CALENDER_API_SECRET = os.getenv('CALENDER_API_SECRET')


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
        form = UserRegisterationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            image = form.cleaned_data.get('image')
            user = User.objects.filter(username=username).first()
            user.profile.is_doctor = True
            user.profile.image = image
            user.profile.save()
            login(request,user)
            messages.success(request, 'Doctor Account Created')
            return redirect('google-oauth-consent')
    else:
        form = UserRegisterationForm()
    return render(request, 'users/register.html', {'form':form, 'form_name':'Doctor' })

from urllib.parse import urlencode

def google_oauth_consent(request):
    
    oauth_params = {
        'client_id': CALENDER_API_ID,
        'redirect_uri': 'https://iusekarma.pythonanywhere.com/oauth-completion/',
        'scope': 'https://www.googleapis.com/auth/calendar',
        'response_type': 'code',
    }
    oauth_url = 'https://accounts.google.com/o/oauth2/auth?' + urlencode(oauth_params)
    
    return redirect(oauth_url)


from django.http import HttpResponse, HttpResponseRedirect
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime, timedelta


def handle_google_auth_callback(request):
    
    redirect_uri = 'https://iusekarma.pythonanywhere.com/oauth-completion/'

    auth_code = request.GET.get('code')

    client_config = {
        'web': {
            'client_id': CALENDER_API_ID,
            'client_secret': CALENDER_API_SECRET,
            'redirect_uris': [redirect_uri],
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'access_type': 'offline'
        }
    }

    flow = Flow.from_client_config(client_config, scopes=['https://www.googleapis.com/auth/calendar'], redirect_uri=redirect_uri)

    flow.fetch_token(code=auth_code)

    credentials = flow.credentials

    user = request.user
    user.profile.google_calendar_credentials = json.dumps(credentials_to_dict(credentials))
    
    user.profile.save()

    return redirect('login')

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


@login_required
def list_doctors(request):
    context = {
        'doctors' : Profile.objects.filter(is_doctor=True).all()
    }
    return render(request, 'users/list_doctors.html', context)


@login_required
def add_event_to_calendar(request, doctor_username):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            speciality = form.cleaned_data['speciality']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            date_and_time = datetime.combine(date, time)
            
            doctor = User.objects.filter(username=doctor_username).first()
            user_credentials = credentials.Credentials(**json.loads(doctor.profile.google_calendar_credentials))
            service = build('calendar', 'v3', credentials=user_credentials)

            event = {
                'summary': f'Appointment',
                'description': f'An appoitment by patient {request.user.username} for speciality : {speciality}',
                'start': {
                    'dateTime': date_and_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': (date_and_time + timedelta(minutes=45)).strftime('%Y-%m-%dT%H:%M:%S'),
                    'timeZone': 'Asia/Kolkata',
                },
            }

            try:
                event = service.events().insert(calendarId='primary', body=event).execute()
                return HttpResponse('Event created: %s' % (event.get('htmlLink')))
            except Exception as e:
                return HttpResponse('Error: %s' % str(e))
    else:
        form = EventForm()
    return render(request, 'users/add_event.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


CATEGORY_CHOICES = (
    ('1','Mental Health'), ('2','Heart Disease'), ('3','Covid19'), ('4','Immunization'), ('5','Others')
)
@login_required
def dashboard(request):
    if request.user.profile.is_doctor:
        context = {
            'posts' : Post.objects.filter(author = request.user).all()
        }
        return render(request, 'users/dashboard_doctor.html', context)
    
    context = {
        'posts_by_categories' : {}
    }
    for i,cat in CATEGORY_CHOICES:
        context['posts_by_categories'][cat] = Post.objects.filter(category = i).all()
    return render(request, 'users/dashboard.html', context)


@login_required
def create_blog(request):
    if request.user.profile.is_doctor:
        if request.method == 'POST':
            form = PostCreationForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('dashboard')
        else:
            form = PostCreationForm()
        return render(request, 'users/create_blog.html', {'form':form})
    return redirect('dashboard')