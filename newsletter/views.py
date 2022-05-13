from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import Subscriber
from .models import Subscribe

from django.shortcuts import render
# Create your views here.

def newsletter(request):
    form = Subscriber(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Thank you for subscribing')

    context = {
        'form' : form
    }
    return render(request, "home/index.html", context)
