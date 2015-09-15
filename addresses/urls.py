from django.conf.urls import url

from .views import AddressListView, AddressDetailView


urlpatterns = [
    url(r'^zipcode/$', AddressListView.as_view(), name='list'),
    url(r'^zipcode/(?P<zipcode>\d+)/$',
        AddressDetailView.as_view(),
        name='detail'),
]
