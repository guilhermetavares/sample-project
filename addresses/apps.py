from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AddressesConfig(AppConfig):
    name = 'addresses'
    label = 'addresses'
    verbose_name = _('Addresses')
