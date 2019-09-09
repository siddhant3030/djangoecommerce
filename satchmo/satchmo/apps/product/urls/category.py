from django.conf.urls import url

from product.views import CategoryView, CategoryIndexView

urlpatterns = [
    url(r'^(?P<parent_slugs>([-\w]+/)*)?(?P<slug>[-\w]+)/$', CategoryView.as_view(), name='satchmo_category'),
    url(r'^$', CategoryIndexView.as_view(), name='satchmo_category_index'),
]