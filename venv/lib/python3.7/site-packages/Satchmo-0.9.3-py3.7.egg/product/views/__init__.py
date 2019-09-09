from decimal import Decimal

from django import http
from django.contrib.messages import constants, get_messages
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView

from l10n.utils import moneyfmt
from livesettings.functions import config_value
from product.models import Category, Product
from product.modules.configurable.models import ConfigurableProduct
from product.signals import index_prerender
from product.utils import find_best_auto_discount, display_featured, find_product_template, optionids_from_post
from satchmo_utils.satchmo_json import json_encode
from satchmo_utils.numbers import  RoundedDecimalError, round_decimal
from satchmo_utils.views import bad_or_missing
import logging

log = logging.getLogger('product.views')


class CategoryIndexView(ListView):
    model = Category
    template_name = "product/category_index.html"
    context_object_name = "categorylist"

    def get_queryset(self):
        return self.model.objects.root_categories()

category_index = CategoryIndexView.as_view()
        
# def category_index(request, template="product/category_index.html", root_only=True):
#     """Display all categories.

#     Parameters:
#     - root_only: If true, then only show root categories.
#     """
#     cats = Category.objects.root_categories()
#     return render(request, template, { 'categorylist' : cats })


class CategoryView(DetailView):
    model = Category
    template_name = "product/category.html"
    context_object_name = "category"

    def get_queryset(self):
        return self.model.objects.by_site()
        
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        products = list(self.object.active_products())
        context['child_categories'] = self.object.get_all_children()
        context['sale'] = find_best_auto_discount(products)
        context['products'] = products
        index_prerender.send(Product, request=self.request, context=context, category=self.object, object_list=products)
        return context

category_view = CategoryView.as_view()
        
# def category_view(request, slug, parent_slugs='', template='product/category.html'):
#     """Display the category, its child categories, and its products.

#     Parameters:
#      - slug: slug of category
#      - parent_slugs: ignored
#     """
#     try:
#         category =  Category.objects.get_by_site(slug=slug)
#         products = list(category.active_products())
#         sale = find_best_auto_discount(products)

#     except Category.DoesNotExist:
#         return bad_or_missing(request, _('The category you have requested does not exist.'))

#     child_categories = category.get_all_children()

#     ctx = {
#         'category': category,
#         'child_categories': child_categories,
#         'sale' : sale,
#         'products' : products,
#     }
#     index_prerender.send(Product, request=request, context=ctx, category=category, object_list=products)
#     return render(request, template, ctx)


def get_configurable_product_options(request, id):
    """Used by admin views"""
    cp = get_object_or_404(ConfigurableProduct, product__id=id)
    options = ''
    for og in cp.option_group.all():
        for opt in og.option_set.all():
            options += '<option value="%s">%s</option>' % (opt.id, str(opt))
    if not options:
        return '<option>No valid options found in "%s"</option>' % cp.product.slug
    return http.HttpResponse(options, content_type="text/html")


class ProductView(DetailView):
    model = Product
    context_object_name = "current_product"
    slug_url_kwarg = 'product_slug'
    default_view_tax = None
    selected_options = ()

    def get_template_names(self):
        template = find_product_template(self.product, producttypes=self.product.get_subtypes())
        return [template.template.name]

    def get_queryset(self):
        return self.model.objects.active_by_site()
        
    def get_context_data(self, **kwargs):
        self.product = self.get_product_variation()
        default_view_tax = self.get_default_view_tax()
        context = super(ProductView, self).get_context_data(**kwargs)
        context['product'] = self.product
        context['sale'] = find_best_auto_discount(self.product)
        context['error_message'] = self.get_error_message()
        context['default_view_tax'] = default_view_tax
        context = self.product.add_template_context(context=context, request=self.request,
                                                    selected_options=self.selected_options,
                                                    default_view_tax=default_view_tax)
        return context

    def get_error_message(self):
        errors = [m for m in get_messages(self.request) if m.level == constants.ERROR]            
        try:
            return errors[0]
        except IndexError:
            pass

    def get_default_view_tax(self):
        return self.default_view_tax or config_value('TAX', 'DEFAULT_VIEW_TAX')

    def get_product_variation(self):
        product = self.object
        if 'ProductVariation' in self.object.get_subtypes():
            self.selected_options = product.productvariation.unique_option_ids
            product = product.productvariation.parent.product
        return product

get_product = ProductView.as_view()
        
# def get_product(request, product_slug=None, selected_options=(),
#     default_view_tax=None):
#     """Basic product view"""

#     errors = [m for m in get_messages(request) if m.level == constants.ERROR]

#     try:
#         product = Product.objects.get_by_site(active=True, slug=product_slug)
#     except Product.DoesNotExist:
#         return bad_or_missing(request, _('The product you have requested does not exist.'))

#     if default_view_tax is None:
#         default_view_tax = config_value('TAX', 'DEFAULT_VIEW_TAX')

#     subtype_names = product.get_subtypes()

#     # Save product id for xheaders, in case we display a ConfigurableProduct
#     product_id = product.id

#     # Clone product object in order to have current product variations in context (extra_context)
#     current_product = product

#     if 'ProductVariation' in subtype_names:
#         selected_options = product.productvariation.unique_option_ids
#         #Display the ConfigurableProduct that this ProductVariation belongs to.
#         product = product.productvariation.parent.product
#         subtype_names = product.get_subtypes()

#     best_discount = find_best_auto_discount(product)

#     if errors:
#         error_message = errors[0]
#     else:
#         error_message = None

#     extra_context = {
#         'product': product,
#         'current_product' : current_product,
#         'default_view_tax': default_view_tax,
#         'sale': best_discount,
#         'error_message' : error_message,
#     }

#     # Get the template context from the Product.
#     extra_context = product.add_template_context(context=extra_context,
#         request=request, selected_options=selected_options,
#         default_view_tax=default_view_tax)
#     template = find_product_template(product, producttypes=subtype_names)
#     response = render(request, template.template.name, extra_context)
#     try:
#         from django.core.xheaders import populate_xheaders
#         populate_xheaders(request, response, Product, product_id)
#     except ImportError:
#         pass
#     return response


def get_price(request, product_slug):
    """Get base price for a product, returning the answer encoded as JSON."""
    quantity = Decimal('1')

    try:
        product = Product.objects.get_by_site(active=True, slug=product_slug)
    except Product.DoesNotExist:
        return http.HttpResponseNotFound(json_encode(('', _("not available"))), content_type="text/javascript")

    prod_slug = product.slug

    if request.method == "POST" and 'quantity' in request.POST:
        try:
            quantity = round_decimal(request.POST['quantity'], places=2, roundfactor=.25)
        except RoundedDecimalError:
            quantity = Decimal('1.0')
            log.warn("Could not parse a decimal from '%s', returning '1.0'", request.POST['quantity'])

    if 'ConfigurableProduct' in product.get_subtypes():
        cp = product.configurableproduct
        chosen_options = optionids_from_post(cp, request.POST)
        pvp = cp.get_product_from_options(chosen_options)

        if not pvp:
            return http.HttpResponse(json_encode(('', _("not available"))), content_type="text/javascript")
        prod_slug = pvp.slug
        price = moneyfmt(pvp.get_qty_price(quantity))
    else:
        price = moneyfmt(product.get_qty_price(quantity))

    if not price:
        return http.HttpResponse(json_encode(('', _("not available"))), content_type="text/javascript")

    return http.HttpResponse(json_encode((prod_slug, price)), content_type="text/javascript")


def get_price_detail(request, product_slug):
    """Get all price details for a product, returning the response encoded as JSON."""
    results = {
        "success" : False,
        "message" :  _("not available")
    }
    price = None

    if request.method=="POST":
        reqdata = request.POST
    else:
        reqdata = request.GET

    try:
        product = Product.objects.get_by_site(active=True, slug=product_slug)
        found = True

        prod_slug = product.slug

        if 'quantity' in reqdata:
            try:
                quantity = round_decimal(reqdata['quantity'], places=2, roundfactor=.25)
            except RoundedDecimalError:
                quantity = Decimal('1.0')
                log.warn("Could not parse a decimal from '%s', returning '1.0'", reqdata['quantity'])
        else:
            quantity = Decimal('1.0')

        if 'ConfigurableProduct' in product.get_subtypes():
            cp = product.configurableproduct
            chosen_options = optionids_from_post(cp, reqdata)
            product = cp.get_product_from_options(chosen_options)

        if product:
            price = product.get_qty_price(quantity)

            results['slug'] = product.slug
            results['price'] = float(price)
            results['success'] = True
            results['message'] = ""

    except Product.DoesNotExist:
        found = False

    data = json_encode(results)
    if found:
        return http.HttpResponse(data, content_type="text/javascript")
    else:
        return http.HttpResponseNotFound(data, content_type="text/javascript")
