from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    image = models.ImageField(default='default.jpg',upload_to='blog_images')
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__():
        return f'Post()'