from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterationForm, PostCreationForm
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post


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
            # user.profile.image = image
            user.profile.save()
            messages.success(request, 'Doctor Account Created')
            return redirect('login')
    else:
        form = UserRegisterationForm()
    return render(request, 'users/register.html', {'form':form, 'form_name':'Doctor' })

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