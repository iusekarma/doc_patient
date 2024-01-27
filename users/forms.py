from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    address = forms.CharField()
    # image = forms.ImageField()
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name','address']
        
# class UserImageForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image']

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','category','image','summary','content','draft']
        

CATEGORY_CHOICES = (
    ('1','Mental Health'), ('2','Heart Disease'), ('3','Covid19'), ('4','Immunization'), ('5','Others')
)

class EventForm(forms.Form):
    speciality = forms.ChoiceField(choices=CATEGORY_CHOICES)
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time'}))