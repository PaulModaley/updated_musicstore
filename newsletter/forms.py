# import form class from django
from django import forms
from .models import Subscribe

# create a ModelForm
class Subscriber(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = Subscribe
		fields = "__all__"
