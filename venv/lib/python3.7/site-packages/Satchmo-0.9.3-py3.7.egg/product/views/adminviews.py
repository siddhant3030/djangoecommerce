from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.db import IntegrityError
from django.views.generic import ListView, FormView, View
from django.views.generic.detail import SingleObjectMixin
try:
    from django.core.urlresolvers import reverse_lazy, reverse
except ImportError:
    from django.urls import reverse_lazy, reverse

from product.forms import VariationManagerForm, InventoryForm, ProductExportForm, ProductImportForm
from product.models import Product
from product.modules.configurable.models import ConfigurableProduct
from satchmo_utils.views import bad_or_missing
import logging

log = logging.getLogger('product.views.adminviews')


class InventoryEditView(FormView):
    template_name = "product/admin/inventory_form.html"
    form_class = InventoryForm
    success_url = reverse_lazy('satchmo_admin_edit_inventory')
    page_title = _('Inventory Editor')
    
    def form_valid(self, form):
        form.save(self.request)
        return super(InventoryEditView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(InventoryEditView, self).get_context_data(**kwargs)
        context['title'] = self.page_title
        return context

# def edit_inventory(request):
#     """A quick inventory price, qty update form"""
#     if request.method == "POST":
#         new_data = request.POST.copy()
#         form = InventoryForm(new_data)
#         if form.is_valid():
#             form.save(request)
#             url = reverse('satchmo_admin_edit_inventory')
#             return HttpResponseRedirect(url)
#     else:
#         form = InventoryForm()

#     ctx = {
#         'title' : _('Inventory Editor'),
#         'form' : form
#     }

#     return render(request, 'product/admin/inventory_form.html', ctx)

edit_inventory = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/accounts/login/')(InventoryEditView.as_view())


class ExportProductsView(FormView):
    template_name = "product/admin/product_export_form.html"
    form_class = ProductExportForm
    importform_class = ProductImportForm
    page_title = _('Product Import/Export')
    
    def form_valid(self, form):
        return form.export(self.request)
    
    def get_context_data(self, **kwargs):
        context = super(InventoryEditView, self).get_context_data(**kwargs)
        context['title'] = self.page_title
        context['importform'] = self.importform_class()
        return context

# def export_products(request, template='product/admin/product_export_form.html'):
#     """A product export tool"""
#     if request.method == 'POST':
#         new_data = request.POST.copy()
#         form = ProductExportForm(new_data)
#         if form.is_valid():
#             return form.export(request)
#     else:
#         form = ProductExportForm()
#     fileform = ProductImportForm()


#     ctx = {
#         'title' : _('Product Import/Export'),
#         'form' : form,
#         'importform': fileform
#     }

#     return render(request, template, ctx)

export_products = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/accounts/login/')(ExportProductsView.as_view())


class ImportProductsView(View):
    form_class = ProductImportForm
    template_name = "product/admin/product_import_result.html"
    redirect_url = reverse_lazy('satchmo_admin_product_export')
    maxsize = 10000000
    
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.redirect_url)

    def post(self, request, *args, **kwargs):
        errors = []
        results = []
        if 'upload' in request.FILES:
            infile = request.FILES['upload']
            form = self.form_class()
            results, errors = form.import_from(infile, maxsize=self.maxsize)
        else:
            errors.append('File: %s' % request.FILES.keys())
            errors.append(_('No upload file found'))

        ctx = {
            'errors' : errors,
            'results' : results
        }
        return render(request, self.template_name, ctx)        

# def import_products(request, maxsize=10000000):
#     """
#     Imports product from an uploaded file.
#     """

#     if request.method == 'POST':
#         errors = []
#         results = []
#         if 'upload' in request.FILES:
#             infile = request.FILES['upload']
#             form = ProductImportForm()
#             results, errors = form.import_from(infile, maxsize=maxsize)

#         else:
#             errors.append('File: %s' % request.FILES.keys())
#             errors.append(_('No upload file found'))

#         ctx = {
#             'errors' : errors,
#             'results' : results
#         }
#         return render(request, "product/admin/product_import_result.html", ctx)
#     else:
#         url = reverse('satchmo_admin_product_export')
#         return HttpResponseRedirect(url)

import_products = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/accounts/login/')(ImportProductsView.as_view())

# def product_active_report(request):
#
#     products = Product.objects.filter(active=True)
#     products = [p for p in products.all() if 'productvariation' not in p.get_subtypes]
#     ctx = {title: 'Active Product Report', 'products' : products }
#     return render(request, 'product/admin/active_product_report.html', ctx)
#
# product_active_report = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/accounts/login/')(product_active_report)


class VariationListView(ListView):
    model = Product
    template_name = "product/admin/variation_manager_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return super(VariationListView, self).get_queryset().filter(configurableproduct__in=ConfigurableProduct.objects.all())
        
variation_list = VariationListView.as_view()
        
# def variation_list(request):
#     products = Product.objects.filter(configurableproduct__in = ConfigurableProduct.objects.all())
#     return render(request, 'product/admin/variation_manager_list.html', { 'products' : products })


class VariationManagerView(SingleObjectMixin, FormView):
    model = Product
    template_name = "product/admin/variation_manager.html"
    form_class = VariationManagerForm
    pk_url_kwarg = 'product_id'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()                
        self.product = self.object
        subtypes = self.object.get_subtypes()
        if 'ProductVariation' in subtypes:
            self.product = self.product.productvariation.parent.product
            if 'ConfigurableProduct' in self.product.get_subtypes():
                url = reverse("satchmo_admin_variation_manager", kwargs={ 'product_id' : self.product.id })
                return HttpResponseRedirect(url)            

        if 'ConfigurableProduct' not in subtypes:
            return bad_or_missing(self.request, _('The product you have requested is not a Configurable Product.'))
                
        return super(VariationManagerView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(VariationManagerView, self).get_form_kwargs()
        kwargs["product"] = self.product
        return kwargs
        
    def form_valid(self, form):
        log.debug("Saving form")
        try:
            form.save(self.request)
        except IntegrityError:
            messages.error(self.request, _('The product you are attempting to remove is linked to an order and can not be removed.'))
        return self.render_to_response(self.get_context_data())

    def form_invalid(self, form):
        log.debug('errors on form')
        return super(VariationManagerView, self).form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super(VariationManagerView, self).get_context_data(**kwargs)
        context['product'] = self.product
        return context

# def variation_manager(request, product_id = ""):
#     try:
#         product = Product.objects.get(id=product_id)
#         subtypes = product.get_subtypes()

#         if 'ProductVariation' in subtypes:
#             # got a variation, we want to work with its parent
#             product = product.productvariation.parent.product
#             if 'ConfigurableProduct' in product.get_subtypes():
#                 url = reverse("satchmo_admin_variation_manager",
#                     kwargs = {'product_id' : product.id})
#                 return HttpResponseRedirect(url)

#         if 'ConfigurableProduct' not in subtypes:
#             return bad_or_missing(request, _('The product you have requested is not a Configurable Product.'))

#     except Product.DoesNotExist:
#             return bad_or_missing(request, _('The product you have requested does not exist.'))

#     if request.method == 'POST':
#         new_data = request.POST.copy()
#         form = VariationManagerForm(new_data, product=product)
#         if form.is_valid():
#             log.debug("Saving form")
#             try:
#                 form.save(request)
#             except IntegrityError:
#                 messages.error(request, _('The product you are attempting to remove is linked to an order and can not be removed.'))
#             # rebuild the form
#             form = VariationManagerForm(product=product)
#         else:
#             log.debug('errors on form')
#     else:
#         form = VariationManagerForm(product=product)

#     ctx = {
#         'product' : product,
#         'form' : form,
#     }
#     return render(request, 'product/admin/variation_manager.html', ctx)

variation_manager = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/accounts/login/')(VariationManagerView.as_view())
