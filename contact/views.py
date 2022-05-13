from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import Contact

from django.shortcuts import render



def contact(request):
	context ={}

	# create object of form
	form = ContactForm(request.POST or None, request.FILES or None)
	
	# check if form data is valid
	if form.is_valid():
		# save the form data to model
		form.save()
		messages.success(request, 'Your message has been sent!')
            # redirect to contact page
        

	template = 'contact/contact.html'
	context['form']= form
	return render(request, template, context)

