from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField, USZipCodeField
from .utils import user_directory_path

class Location(models.Model):
    current_address = models.CharField(max_length=128, blank=True)
    permanent_address = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    state = USStateField(default='NY')
    zip_code = USZipCodeField(blank=True)

    def __str__(self):
        return f'Address {self.id}'


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path,null=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    location = models.OneToOneField("users.Location",on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


