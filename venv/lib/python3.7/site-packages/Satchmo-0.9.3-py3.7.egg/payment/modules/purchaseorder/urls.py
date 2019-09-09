from django.conf.urls import url

from satchmo_store.shop.satchmo_settings import get_satchmo_setting
from payment.views.checkout import success
from . import views

ssl = get_satchmo_setting('SSL', default_value=False)

urlpatterns = [
    url(r'^$', views.pay_ship_info, {'SSL':ssl}, name='PURCHASEORDER_satchmo_checkout-step2'),
    url(r'^confirm/$', views.confirm_info, {'SSL':ssl}, name='PURCHASEORDER_satchmo_checkout-step3'),
    url(r'^success/$', success, {'SSL':ssl}, name='PURCHASEORDER_satchmo_checkout-success'),
]
