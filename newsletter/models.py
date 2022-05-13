from django.db import models
from django.forms import ModelForm

class Subscribe(models.Model):
    email = models.EmailField(max_length= 250)