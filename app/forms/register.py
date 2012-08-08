__author__ = 'yousuf'

from django.forms import ModelForm
from app.models import UserProfile

class CompleteRegistrationForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'accepted_eula',
            'gender',
        )
