import requests

from django.conf import settings
from django.utils.translation import ugettext as _
from restless.http import Http201, Http400, Http404, JSONResponse
from restless.models import serialize
from restless.modelviews import ListEndpoint, DetailEndpoint

from .forms import ZipCodeForm
from .models import Address


class FieldsMixin(object):
    fields = NotImplemented

    def serialize(self, objs):
        return serialize(objs, fields=self.fields)


class Http204(JSONResponse):
    status_code = 204


class AddressListView(FieldsMixin, ListEndpoint):
    model = Address
    fields = ('city', 'neighborhood', 'zipcode', 'state', 'address',
              'address2')

    def get_query_set(self, request, *args, **kwargs):
        qs = super(AddressListView, self).get_query_set(request, *args,
                                                        **kwargs)
        # TODO implement a start
        limit = request.params.get('limit')
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                return Http400(_('invalid limit'))
            else:
                qs = qs[:limit]
        return qs

    def post(self, request, *args, **kwargs):
        zipcode = request.data.get('zipcode')
        if not zipcode:
            zipcode = request.data.get('zip_code')

        if not zipcode:
            return Http400(_('zipcode not sent'))

        form = ZipCodeForm({'zipcode': zipcode})
        if not form.is_valid():
            return Http400(_('invalid data'), errors=form.errors)

        response = requests.get(
            '{}{}'.format(
                settings.ZIPCODE_API_URL,
                form.cleaned_data['zipcode']
            )
        )
        if response.status_code == 404:
            return Http404(_(u'zipcode not found'))

        response = response.json()

        obj = Address.objects.create(
            zipcode=response['cep'],
            address=response.get('logradouro'),  # nullable
            neighborhood=response.get('bairro'),  # nullable
            state=response['estado'],
            city=response['cidade'],
            address2=response.get('complemento'),  # nullable
        )

        return Http201(self.serialize(obj))


class AddressDetailView(FieldsMixin, DetailEndpoint):
    model = Address
    lookup_field = 'zipcode'
    methods = ['GET', 'DELETE']
    fields = ('city', 'neighborhood', 'zipcode', 'state', 'address',
              'address2')

    def delete(self, request, *args, **kwargs):
        response = super(AddressDetailView, self).delete(request, *args,
                                                         **kwargs)
        return Http204({})
