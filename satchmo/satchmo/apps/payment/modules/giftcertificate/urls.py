from django.conf.urls import url

from satchmo_store.shop.satchmo_settings import get_satchmo_setting
from payment.views.checkout import success
from payment.modules.giftcertificate import views

ssl = get_satchmo_setting('SSL', default_value=False)

urlpatterns = [
     url(r'^$', views.pay_ship_info, {'SSL':ssl}, name='GIFTCERTIFICATE_satchmo_checkout-step2'),
     url(r'^confirm/$', views.confirm_info, {'SSL':ssl}, name='GIFTCERTIFICATE_satchmo_checkout-step3'),
     url(r'^success/$', success, {'SSL':ssl}, name='GIFTCERTIFICATE_satchmo_checkout-success'),
     url(r'^balance/$', views.check_balance, {'SSL':ssl}, name='satchmo_giftcertificate_balance'),
]