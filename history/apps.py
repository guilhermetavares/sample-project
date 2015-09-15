from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class HistoryConfig(AppConfig):
    name = 'history'
    label = 'history'
    verbose_name = _('History logs')
