# -*- coding: utf-8 -*-

from django.test import TestCase

from addresses.models import Address
from history.models import History


default_test_data = [{
    'zipcode': '14010140',
    'address': u'Praça Barão do Rio Branco',
    'neighborhood': 'Centro',
    'state': 'SP',
    'city': u'Ribeirão Preto',
    'address2': None,
}, ]


class HistoryTest(TestCase):
    def create_data(self):
        for address in default_test_data:
            Address.objects.create(**address)

    def test_history_created(self):
        self.create_data()
        address_count = Address.objects.count()
        history_count = History.objects.count()
        self.assertEqual(address_count, history_count)

    def test_history_delete(self):
        self.create_data()
        address_count_before_delete = Address.objects.count()
        Address.objects.first().delete()
        history_count = History.objects.count()
        self.assertEqual(address_count_before_delete + 1, history_count)

    def test_history_unicode(self):
        self.create_data()
        history = History.objects.first()
        self.assertEqual(
            unicode(history),
            u'{} {} - {} ({})'.format(
                history.key,
                history.action,
                history.date.strftime('%d/%m/%Y %H:%M'),
                history.model,
            )
        )
