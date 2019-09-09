from django.contrib.sites.models import Site
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView

from product import signals
from product.models import Product
from product.utils import find_best_auto_discount
from .models import Brand, BrandCategory, BrandProduct

import logging

log = logging.getLogger("satchmo_brand.views")


class BrandListView(ListView):
    template_name = 'brand/index.html'
    model = Brand
    context_object_name = 'brands'

    def get_queryset(self):
        return self.model.objects.active()

    def get_context_data(self, **kwargs):
        context = super(BrandListView, self).get_context_data(**kwargs)
        signals.index_prerender.send(self.model, request=self.request, context=context, object_list=self.object_list)
        return context
    
brand_list = BrandListView.as_view()
    
# def brand_list(request):
#     brands = Brand.objects.active()
#     ctx = {
#         'brands' : brands,
#     }
#     signals.index_prerender.send(Brand, request=request, context=ctx, object_list=brands)
#     return render(request, 'brand/index.html')


class BrandDetailView(DetailView):
    template_name = 'brand/view_brand.html'
    model = Brand
    slug_url_kwarg = 'brandname'
    context_object_name = 'brand'

    def get_context_data(self, **kwargs):
        context = super(BrandDetailView, self).get_context_data(**kwargs)
        products = list(self.object.active_products())
        context['products'] = products
        context['sale'] = find_best_auto_discount(products)
        signals.index_prerender.send(self.model, request=self.request, context=context, brand=self.object, object_list=products)
        return context
    
brand_page = BrandDetailView.as_view()
    
#def brand_page(request, brandname):
#    try:
#        brand = Brand.objects.by_slug(brandname)
#        
#    except Brand.DoesNotExist:
#        raise Http404(_('Brand "%s" does not exist') % brandname)
#
#        
#    products = list(brand.active_products())
#    sale = find_best_auto_discount(products)
#
#    ctx = {
#        'brand' : brand,
#        'products': products,
#        'sale' : sale,
#    }
#    signals.index_prerender.send(BrandProduct, request=request, context=ctx, brand=brand, object_list=products)
#
#    return render(request, 'brand/view_brand.html', ctx)


class BrandCategoryDetailView(DetailView):
    template_name = 'brand/view_brand.html'
    model = BrandCategory
    slug_url_kwarg = 'catname'
    brand_slug_url_kwarg = 'brandname'
    context_object_name = 'brand'

    def get_object(self, queryset=None):
        brandname = self.kwargs.get(self.brand_slug_url_kwarg)
        catname = self.kwargs.get(self.slug_url_kwarg)
        try:
            cat = self.model.objects.by_slug(brandname, catname)
        except Brand.DoesNotExist:
            raise Http404(_('Brand "%s" does not exist') % brandname)
        except self.model.DoesNotExist:
            raise Http404(_('No category "%{category}s" in brand "%{brand}s"').format(category=catname, brand=brandname))        

    def get_context_data(self, **kwargs):
        context = super(BrandCategoryDetailView, self).get_context_data(**kwargs)
        products = list(self.object.active_products())
        context['sale'] = find_best_auto_discount(products)
        return context
    
brand_category_page = BrandCategoryDetailView.as_view()
    
#def brand_category_page(request, brandname, catname):
#    try:
#        cat = BrandCategory.objects.by_slug(brandname, catname)
#
#    except Brand.DoesNotExist:
#        raise Http404(_('Brand "%s" does not exist') % brandname)
#        
#    except BrandCategory.DoesNotExist:
#        raise Http404(_('No category "%{category}s" in brand "%{brand}s"').format(category=catname, brand=brandname))
#        
#    products = list(cat.active_products())
#    sale = find_best_auto_discount(products)
#    
#    ctx = {
#        'brand' : cat,
#        'sale' : sale,
#    }
#    return render(request, 'brand/view_brand.html', ctx)
