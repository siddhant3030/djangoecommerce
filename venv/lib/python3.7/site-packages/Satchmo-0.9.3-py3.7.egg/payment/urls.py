from django.conf.urls import url

from livesettings.functions import config_value_safe
from satchmo_store.shop.satchmo_settings import get_satchmo_setting
import logging

from .views import contact, checkout, balance, cron

log = logging.getLogger('payment.urls')

ssl = get_satchmo_setting('SSL', default_value=False)

urlpatterns = [
    url(r'^$', contact.contact_info_view, {'SSL': ssl}, name='satchmo_checkout-step1'),
    url(r'^success/$', checkout.success, {'SSL' : ssl}, name='satchmo_checkout-success'),
    url(r'custom/charge/(?P<orderitem_id>\d+)/$', balance.ChargeRemainingUpdateView.as_view(), name='satchmo_charge_remaining'),
    #url(r'custom/charge/$', balance.charge_remaining_post, name="satchmo_charge_remaining_post"),
    url(r'^balance/(?P<order_id>\d+)/$', balance.BalanceRemainingOrderView.as_view(), {'SSL' : ssl}, name='satchmo_balance_remaining_order'),
    url(r'^balance/$', balance.BalanceRemainingView.as_view(), {'SSL' : ssl}, name="satchmo_balance_remaining"),
    url(r'^cron/$', cron.cron_rebill, name='satchmo_cron_rebill'),
    url(r'^mustlogin/$', contact.authentication_required, {'SSL' : ssl}, name='satchmo_checkout_auth_required'),
]

# now add all enabled module payment settings

def make_urlpatterns():
    patterns = []
    try:
        from django.apps import apps
        app_list = [app_config.models_module for app_config in apps.get_app_configs() if app_config.models_module is not None]
    except ImportError:
        from django.db import models
        app_list = models.get_apps()
    for app in app_list:
        if hasattr(app, 'PAYMENT_PROCESSOR'):
            parts = app.__name__.split('.')
            key = parts[-2].upper()
            modulename = 'PAYMENT_%s' % key
            name = app.__name__
            name = name[:name.rfind('.')]
            #log.debug('payment module=%s, key=%s', modulename, key)
            # BJK: commenting out Bursar settings here
            # try:
            #     cfg = config_get(modulename, 'INTERFACE_MODULE')
            #     interface = cfg.editor_value
            # except SettingNotSet:
            #     interface = name[:name.rfind('.')]
            # urlmodule = "%s.urls" % interface
            urlmodule = '.'.join(parts[:-1]) + '.urls'
            urlbase = config_value_safe(modulename, 'URL_BASE', key.lower())
            log.debug('Found payment processor: %s, adding urls at %s', key, urlbase)
            patterns.append(url(urlbase, [urlmodule, '', '']))
    return patterns

urlpatterns += make_urlpatterns()
