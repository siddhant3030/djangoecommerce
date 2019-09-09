"""
Urls for Product Brand module, note that you do not have to add this to your urls file, it will get automatically included by collect_urls.
"""
from django.conf.urls import url, include
from satchmo_store.shop import get_satchmo_setting
from . import views
import logging

log = logging.getLogger('brand.urls')

urlpatterns = [
    url(r'^$', views.brand_list, name='satchmo_brand_list'),
    url(r'^(?P<brandname>.*)/(?P<catname>.*)/$', views.brand_category_page, name='satchmo_brand_category_view'),
    url(r'^(?P<brandname>.*)/$', views.brand_page, name='satchmo_brand_view'),
]

brandbase = r'^' + get_satchmo_setting('BRAND_SLUG') + '/'

prodbase = r'^' + get_satchmo_setting('PRODUCT_SLUG') + '/'
brandpatterns = [
    url(brandbase, include('satchmo_ext.brand.urls'))
]

def add_brand_urls(sender, patterns=(), section="", **kwargs):
    if section=="__init__":
        log.debug('adding brand urls at %s', brandbase)
        patterns += brandpatterns
