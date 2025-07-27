from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=250, unique=True, null=False)

class Client(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=250, unique=True)
    phone_number = models.CharField(max_length=20)


class Pet(models.Model):
    name = models.CharField(max_length=30, null=False)
    pet_type = models.CharField(max_length=30, null=False)
    breed = models.CharField(max_length=30, null=False)
    color = models.CharField(max_length=30, null=False) 
    adopted = models.BooleanField(default=False, null=False)
    adopted_at = models.DateTimeField(null=True)
    
    def save(self, *args, **kwargs):
        if self.adopted and self.adopted_at is None:
            datetime = timezone.now()
            self.adopted_at = datetime
        super().save(*args, **kwargs)

class Adoption(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='adoption')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='adoption')
    created_at = models.DateTimeField(auto_now_add=True)