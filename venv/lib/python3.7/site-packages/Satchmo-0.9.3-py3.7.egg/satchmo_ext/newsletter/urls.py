"""
URLConf for Satchmo Newsletter app

This will get automatically added by satchmo_store, under the url given in your livesettings "NEWSLETTER","NEWSLETTER_SLUG"
"""

from django.conf.urls import url, include

from livesettings.functions import config_value_safe
from . import views
import logging

log = logging.getLogger('newsletter.urls')

urlpatterns = [
    url(r'^subscribe/$', views.add_subscription, name='newsletter_subscribe'),
    url(r'^subscribe/ajah/$', views.add_subscription, 
        {'result_template' : 'newsletter/ajah.html'}, name='newsletter_subscribe_ajah'),
    url(r'^unsubscribe/$', views.remove_subscription, name='newsletter_unsubscribe'),
    url(r'^unsubscribe/ajah/$', views.remove_subscription, 
        {'result_template' : 'newsletter/ajah.html'}, name='newsletter_unsubscribe_ajah'),
    url(r'^update/$', views.update_subscription, name='newsletter_update'),
]

def add_newsletter_urls(sender, patterns=(), **kwargs):
    newsbase = r'^' + config_value_safe('NEWSLETTER', 'NEWSLETTER_SLUG', "newsletter") + '/'    
    log.debug("Adding newsletter urls at %s", newsbase)
    newspatterns = [
        url(newsbase, include('satchmo_ext.newsletter.urls'))
    ]
    patterns += newspatterns