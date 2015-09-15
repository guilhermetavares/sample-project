from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _

from addresses.models import Address


class History(models.Model):
    model = models.CharField(_('model'), max_length=255)
    key = models.CharField(_('key'), max_length=255)
    action = models.CharField(_('action'), max_length=255)
    date = models.DateTimeField(_('date'), auto_now_add=True)

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

    @classmethod
    def save_log(cls, model, key, action):
        History.objects.create(
            model=model._meta.verbose_name_raw,
            key=key,
            action=action,
        )


def history_obj_save(sender, instance, *args, **kwargs):
    History.save_log(sender, instance.get_key(), 'created')


def history_obj_delete(sender, instance, *args, **kwargs):
    History.save_log(sender, instance.get_key(), 'deleted')


post_save.connect(history_obj_save, sender=Address)
post_delete.connect(history_obj_delete, sender=Address)
