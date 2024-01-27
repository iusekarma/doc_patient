from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, default='Nil')
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    is_doctor = models.BooleanField(default=False)
    google_calendar_credentials = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    

CATEGORY_CHOICES = (
    ('1','Mental Health'), ('2','Heart Disease'), ('3','Covid19'), ('4','Immunization'), ('5','Others')
)

class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    image = models.ImageField(default='blog_pictures/default.jpg',upload_to='blog_images')
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    draft = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Post {self.title} by {self.author.username}'