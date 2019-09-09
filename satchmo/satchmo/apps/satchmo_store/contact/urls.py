"""
URLConf for Satchmo Contacts.
"""
from django.conf.urls import url

from satchmo_utils.signals import collect_urls
from satchmo_store import contact
from satchmo_store.shop.satchmo_settings import get_satchmo_setting
from satchmo_store.contact import views

ssl = get_satchmo_setting('SSL', default_value=False)

urlpatterns = [
    url(r'^$', views.view, name='satchmo_account_info'),
    url(r'^update/$', views.update, name='satchmo_profile_update'),
    url(r'^address/create/$', views.address_create_edit, name='satchmo_address_create'),
    url(r'^address/edit/(?P<id>\d+)/$',views.address_create_edit, name='satchmo_address_edit'),
    url(r'^address/delete/(?P<id>\d+)/$',views.address_delete, name='satchmo_address_delete'),
    url(r'^ajax_state/$', views.ajax_get_state, {'SSL': ssl}, 'satchmo_contact_ajax_state'),
]

collect_urls.send(sender=contact, patterns=urlpatterns)
