import requests

from django.conf import settings
from django.utils.translation import ugettext as _
from restless.http import Http201, Http400
from restless.models import serialize
from restless.modelviews import ListEndpoint, DetailEndpoint

from .forms import ZipCodeForm
from .models import Address


class AddressListView(ListEndpoint):
    model = Address
    fields = ('city', 'neighborhood', 'zipcode', 'state', 'address')

    def serialize(self, objs):
        return serialize(objs, fields=self.fields)

    def get_query_set(self, request, *args, **kwargs):
        qs = super(AddressListView, self).get_query_set(request, *args,
                                                        **kwargs)
        if request.params.get('limit'):
            qs = qs.limit(request.params['limit'])
        return qs

    def post(self, request, *args, **kwargs):
        zipcode = request.data.get('zipcode')
        if not zipcode:
            zipcode = request.data.get('zip_code')

        if not zipcode:
            return Http400(_(u'zipcode not sent'))

        form = ZipCodeForm({'zipcode': zipcode})
        if not form.is_valid():
            return Http400(_(u'invalid data'), errors=form.errors)

        response = requests.get(
            '{}{}'.format(
                settings.ZIPCODE_API_URL,
                form.cleaned_data['zipcode']
            )
        ).json()

        obj = Address.objects.create(
            zipcode=response['cep'],
            address=response.get('logradouro'),  # nullable
            neighborhood=response.get('bairro'),  # nullable
            state=response['estado'],
            city=response['cidade'],
        )

        return Http201(self.serialize(obj))


class AddressDetailView(DetailEndpoint):
    model = Address
    lookup_field = 'zipcode'
    methods = ['GET', 'DELETE']
