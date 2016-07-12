from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone

from . import models


class MenuForm(forms.ModelForm):
    """Form to add new or edit existing menu."""

    class Meta:
        model = models.Menu
        fields = (
            'season',
            'items',
            'expiration_date',
        )
        widgets = {
            'expiration_date': SelectDateWidget,
        }

    def clean_expiration_date(self):
        """Checks that expiration date is in the future."""
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date and expiration_date < timezone.now().date():
            raise forms.ValidationError(
                'Expiration date must be in the future')
        return expiration_date
