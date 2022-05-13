# import form class from django
from django import forms
from .models import Contact

# create a ModelForm
class ContactForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = Contact
		fields = "__all__"
