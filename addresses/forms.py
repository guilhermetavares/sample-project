import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Address


RE_NOTNUMBER = re.compile(r'[^0-9]')


class ZipCodeForm(forms.Form):
    zipcode = forms.CharField(max_length=9, min_length=8)

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        zipcode = RE_NOTNUMBER.sub('', zipcode)
        if len(zipcode) != 8:
            raise forms.ValidationError(_('invalid zipcode'))

        if Address.objects.filter(zipcode=zipcode).exists():
            raise forms.ValidationError(_('zipcode info already exists'))
        return zipcode
