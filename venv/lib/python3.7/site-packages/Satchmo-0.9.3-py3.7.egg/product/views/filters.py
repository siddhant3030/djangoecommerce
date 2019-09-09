from django.views.generic import ListView

from livesettings.functions import config_value

from product.models import Product
from product.queries import bestsellers

import logging
log = logging.getLogger('product.views.filters')


class BestsellersListView(ListView):
    model = Product
    template_name = "product/best_sellers.html"
    context_object_name = "products"
    count = 0

    def get_queryset(self):
        if self.count == 0:
            self.count = config_value('PRODUCT','NUM_PAGINATED')
        return bestsellers(self.count)        


class RecentListView(ListView):
    model = Product
    template_name = "product/recently_added.html"
    paginate_by = 0
    
    def get_queryset(self):
        return self.model.objects.recent_by_site()

    def get_paginate_by(self, queryset):
        if self.paginate_by:
            return self.paginate_by
        else:
            return config_value('PRODUCT','NUM_PAGINATED')

            
display_bestsellers = BestsellersListView.as_view()
display_recent = RecentListView.as_view()