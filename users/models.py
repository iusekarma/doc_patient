from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, default='Nil')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_doctor = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} Profile'