from django.conf.urls import url

import product
from satchmo_utils.signals import collect_urls
from product.views.filters import RecentListView, BestsellersListView

urlpatterns = [
    url(r'^(?P<product_slug>[-\w]+)/$', product.views.get_product, name='satchmo_product'),
    url(r'^(?P<product_slug>[-\w]+)/prices/$', product.views.get_price, name='satchmo_product_prices'),
    url(r'^(?P<product_slug>[-\w]+)/price_detail/$', product.views.get_price_detail, name='satchmo_product_price_detail'),
]

urlpatterns += [
    url(r'^view/recent/$', RecentListView.as_view(), name='satchmo_product_recently_added'),
    url(r'^view/bestsellers/$', BestsellersListView.as_view(), name='satchmo_product_best_selling'),
]

# here we are sending a signal to add patterns to the base of the shop.
collect_urls.send(sender=product, patterns=urlpatterns, section="product")
