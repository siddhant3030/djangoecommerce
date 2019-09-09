"""Urls which need to be loaded at root level."""
from django.conf.urls import url

from product.views import get_configurable_product_options
from product.views import adminviews

adminpatterns = [
    url(r'^admin/product/configurableproduct/(?P<id>\d+)/getoptions/', 
        get_configurable_product_options, name='satchmo_admin_configurableproduct'),
]

adminpatterns += [
    url(r'^admin/inventory/edit/$', adminviews.edit_inventory, name='satchmo_admin_edit_inventory'),
    url(r'^inventory/export/$', adminviews.export_products, name='satchmo_admin_product_export'),
    url(r'^inventory/import/$', adminviews.import_products, name='satchmo_admin_product_import'),
    # url(r'^inventory/report/$', adminviews.product_active_report, {}, 'satchmo_admin_product_report'),
    url(r'^admin/(?P<product_id>\d+)/variations/$', adminviews.variation_manager, name='satchmo_admin_variation_manager'),
    url(r'^admin/variations/$', adminviews.VariationListView.as_view(), name='satchmo_admin_variation_list'),
]