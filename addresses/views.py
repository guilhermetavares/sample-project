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
        # Complementar o limit com paginação
        # request.params.get('page')
        
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
        zipcode = request.data.get('zipcode') or request.data.get('zip_code')
        
        # if not zipcode:
            # zipcode = request.data.get('zip_code')

        if not zipcode:
            return Http400(_('zipcode not sent'))
        
        # Usaria um Client aqui, em outro .py rs
        # Só uma idéia, por exemplo:
        # Separar os métodos ajudaria muito para testar, inserir o novo registro de forma assincrona e para alterar o postmon
        # Considerando o ZipCodeModelForm um ModelForm de Address
        # client.py
        # class ZipCodeClient(object):
        #     def __init__(self, zipcode):
        #         self.zipcode = zipcode
            
        #     def get_form_data(self):
        #         # aqui que facilitaria numa eventual troca de serviço
        #         response_data = self.get_response()
        #         return {
        #             'zipcode': response_data.get('cep'),
        #             'address': response_data.get('logradouro'),
        #             'neighborhood': response_data.get('bairro'),
        #             'state': response_data.get('estado'),
        #             'city': response_data.get('cidade'),
        #             'address2': response_data.get('complemento'),
        #         }
        #     def get_response(self):
        #         response = requests.get(
        #             '{}{}'.format(
        #                 settings.ZIPCODE_API_URL,
        #                 self.zipcode
        #             )
        #         )
        #         return response.json()
            
        #     def get_zipcode(self):
        #         try:
        #             return Address.objects.get(zipcode=zipcode)
        #         except:
        #             pass
                
        #         data = self.get_form_data()
        #         form = ZipCodeModelForm(data)
        #         if form.is_valid():
        #             return form.save()
        #         return None # ou um raise
        
        # Usando o client
        # client = ZipCodeClient(zipcode)
        # zipcode = client.get_zipcode()
        # if zipcode:
        #     return Http201(self.serialize(obj))
        # return Http400(_('zipcode invalid'))
        
        # - - - - - - - - - - -
        
        form = ZipCodeForm({'zipcode': zipcode})
        # validar formato e se existe não acho muito interessante
        # poderia fazer um ljust e a api de consulta trata os ceps invalidos: ex. 12345 formata para 00012345 por exemplo
        if not form.is_valid():
            return Http400(_('invalid data'), errors=form.errors)
        
        # timeout no get
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
            # forçar/esperar um erro KeyError aqui acho que não fica legal, até por isso o client
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
