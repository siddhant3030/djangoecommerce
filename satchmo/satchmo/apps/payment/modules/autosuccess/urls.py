from django.conf.urls import url

from satchmo_store.shop.satchmo_settings import get_satchmo_setting
from payment.views.checkout import success
from payment.modules.autosuccess.views import one_step

ssl = get_satchmo_setting('SSL', default_value=False)

urlpatterns = [
    url(r'^$', one_step, {'SSL': ssl}, name='AUTOSUCCESS_satchmo_checkout-step2'),
    url(r'^success/$', success, {'SSL': ssl}, name='AUTOSUCCESS_satchmo_checkout-success'),
]
