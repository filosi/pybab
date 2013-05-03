from django import forms
from ..models import UserIndicatorLink

class UserIndicatorLinkForm(forms.ModelForm):
    class Meta:
        model = UserIndicatorLink

