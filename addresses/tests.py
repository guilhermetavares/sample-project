# -*- coding: utf-8 -*-

import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Address


default_test_data = [{
    'zipcode': '14010140',
    'address': u'Praça Barão do Rio Branco',
    'neighborhood': 'Centro',
    'state': 'SP',
    'city': u'Ribeirão Preto',
    'address2': None,
}, {
    'zipcode': '14025390',
    'address': u'Avenida Independência',
    'neighborhood': u'Jardim Sumaré',
    'state': 'SP',
    'city': u'Ribeirão Preto',
    'address2': u'de 1201 a 2159 - lado ímpar',
}]


class AddressTest(TestCase):
    def create_data(self):
        for address in default_test_data:
            Address.objects.create(**address)

    def test_address_empty_list(self):
        response = self.client.get(reverse('addresses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')

    def test_address_list_with_data(self):
        self.create_data()
        response = self.client.get(reverse('addresses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, json.dumps(default_test_data))

    def test_address_list_valid_limit(self):
        self.create_data()
        url = u'{}?limit=1'.format(reverse('addresses:list'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            json.dumps(default_test_data[:1])
        )

    def test_address_list_invalid_limit(self):
        self.create_data()
        url = u'{}?limit=invalid'.format(reverse('addresses:list'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            '{"error": "invalid limit"}'
        )

    def test_address_create_with_valid_data(self):
        address = default_test_data[0]
        response = self.client.post(
            reverse('addresses:list'),
            data={'zip_code': address['zipcode']},  # key as zip_code
        )
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content, json.dumps(address))
 
    def test_address_create_with_valid_data2(self):
        address = default_test_data[1]
        self.assertEqual(address['zipcode'], '14025390')
        response = self.client.post(
            reverse('addresses:list'),
            data={'zipcode': '14025-390'},  # value as xxxxx-xxx
        )
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content, json.dumps(address))

    def test_address_create_valid_data_but_not_found(self):
        response = self.client.post(
            reverse('addresses:list'),
            data={'zipcode': '14046475'},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, '{"error": "zipcode not found"}')

    def test_address_create_zipcode_not_sent(self):
        response = self.client.post(reverse('addresses:list'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, '{"error": "zipcode not sent"}')

    def test_address_create_valid_data_but_duplicated(self):
        self.create_data()
        response = self.client.post(
            reverse('addresses:list'),
            data={'zipcode': default_test_data[0]['zipcode']}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            ('{"errors": {"zipcode": ["zipcode info already exists"]}, '
             '"error": "invalid data"}')
        )

    def test_address_create_with_invalid_data(self):
        response = self.client.post(
            reverse('addresses:list'),
            data={'zipcode': '1402-260'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            ('{"errors": {"zipcode": ["invalid zipcode"]}, '
             '"error": "invalid data"}')
        )

    def test_address_detail_valid(self):
        self.create_data()
        address = default_test_data[0]
        response = self.client.get(
            reverse(
                'addresses:detail',
                args=[address['zipcode'], ]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            json.dumps(address),
        )

    def test_address_detail_not_found(self):
        response = self.client.get(
            reverse(
                'addresses:detail',
                args=['14010140', ]  # any zip code, since nothing was created
            )
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.content,
            '{"error": "Resource Not Found"}',
        )

    def test_address_delete_valid(self):
        self.create_data()
        address = default_test_data[0]
        response = self.client.delete(
            reverse(
                'addresses:detail',
                args=[address['zipcode'], ]
            )
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, '')

    def test_address_delete_not_found(self):
        response = self.client.delete(
            reverse(
                'addresses:detail',
                args=['14010140', ]  # any zip code, since nothing was created
            )
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, '{"error": "Resource Not Found"}')

    def test_address_unicode(self):
        self.create_data()
        address = Address.objects.get(zipcode='14010140')
        self.assertEqual(unicode(address), '14010140')
