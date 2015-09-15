from django.db import models
from django.utils.translation import ugettext_lazy as _


class Address(models.Model):
    zipcode = models.CharField(_(u'zipcode'), max_length=8, unique=True)
    address = models.CharField(_(u'address'), max_length=255, null=True)
    neighborhood = models.CharField(
        _(u'neighborhood'),
        max_length=255,
        null=True
    )
    state = models.CharField(_(u'state'), max_length=2)
    city = models.CharField(_(u'city'), max_length=255)

    class Meta:
        verbose_name = _(u'address')
        verbose_name_plural = _(u'addresses')

    def __unicode__(self):
        return self.zipcode
