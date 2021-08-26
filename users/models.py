from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_kitchen = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    sq1 = models.CharField(max_length=255, default='1')
    sq2 = models.CharField(max_length=255, default='1')
    aq1 = models.CharField(max_length=255, default='1')
    aq2 = models.CharField(max_length=255, default='1')