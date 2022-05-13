from django.db import models
from django.forms import ModelForm

class Contact(models.Model):
    name = models.CharField(max_length= 100)
    email = models.EmailField(max_length= 250)
    subject = models.CharField(max_length=40)
    message = models.CharField(max_length=500)