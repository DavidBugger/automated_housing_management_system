from django.db import models
from django.contrib.auth.models import User
from .utils import user_upload_directory_path

# Create your models here.
class Location (models.Model):
    address_1 = models.CharField(max_length=128, blank=True)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=128, blank=True)  
    zip_code = models.CharField(max_length=128,blank=True)

    def __str__(self):
        return f'Location {self.id}'

class Profile(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_upload_directory_path, null=True)
    bio = models.CharField(max_length=140, blank=True)
    email_address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.users.username} \'s Profile'
    

