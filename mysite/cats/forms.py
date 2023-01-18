from django.forms import ModelForm
from .models import Breed


# Create the form class.
class BreedForm(ModelForm):
    class Meta:
        model = Breed
        fields = '__all__'