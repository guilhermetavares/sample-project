from django.db import models
from django.utils.translation import ugettext_lazy as _


class History(models.Model):
    model = models.CharField(_('model'), max_length=255)
    key = models.CharField(_('key'), max_length=255)
    action = models.CharField(_('action'), max_length=255)
    date = models.DateTimeField(_('date'))

    class Meta:
        verbose_name = _('history log')
        verbose_name_plural = _('history logs')

    def __unicode__(self):
        return '{} {} - {} ({})'.format(
            self.key,
            self.action,
            self.date.strftime('%d/%m/%Y %H:%M'),
            self.model,
        )
