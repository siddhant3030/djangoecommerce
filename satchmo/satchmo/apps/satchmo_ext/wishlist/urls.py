"""
Urls for wishlists, note that this does not have to get added manually to the urls, it will be added automatically by satchmo core if this app is installed.
"""
from django.conf.urls import url, include

from livesettings.functions import config_value_safe
from . import views
import logging

log = logging.getLogger('wishlist.urls')

urlpatterns = [
    url(r'^$', views.wishlist_view, name='satchmo_wishlist_view'),
    url(r'^add/$', views.wishlist_add, name='satchmo_wishlist_add'),
    url(r'^add/ajax/$', views.wishlist_add_ajax, name='satchmo_wishlist_add_ajax'),
    url(r'^remove/$', views.wishlist_remove, name='satchmo_wishlist_remove'),
    url(r'^remove/ajax$', views.wishlist_remove_ajax, name='satchmo_wishlist_remove_ajax'),
    url(r'^add_cart/$', views.wishlist_move_to_cart, name='satchmo_wishlist_move_to_cart'),
]

def add_wishlist_urls(sender, patterns=(), **kwargs):
    wishbase = r'^' + config_value_safe('SHOP', 'WISHLIST_SLUG', "wishlist") + '/'    
    log.debug('adding wishlist urls at %s', wishbase)
    wishpatterns = [
        url(wishbase, include('satchmo_ext.wishlist.urls'))
    ]
    patterns += wishpatterns