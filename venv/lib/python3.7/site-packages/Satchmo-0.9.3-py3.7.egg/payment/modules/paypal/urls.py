from django.conf.urls import url

from satchmo_store.shop.satchmo_settings import get_satchmo_setting
from payment.views.confirm import confirm_free_order
from . import views  

ssl = get_satchmo_setting('SSL', default_value=False)

urlpatterns = [
     url(r'^$', views.pay_ship_info, {'SSL': ssl}, name='PAYPAL_satchmo_checkout-step2'),
     url(r'^confirm/$', views.confirm_info, {'SSL': ssl}, name='PAYPAL_satchmo_checkout-step3'),
     url(r'^success/$', views.success, {'SSL': ssl}, name='PAYPAL_satchmo_checkout-success'),
     url(r'^ipn/$', views.ipn, {'SSL': ssl}, name='PAYPAL_satchmo_checkout-ipn'),
     url(r'^confirmorder/$', confirm_free_order, {'SSL' : ssl, 'key' : 'PAYPAL'}, name='PAYPAL_satchmo_checkout_free-confirm')
]
