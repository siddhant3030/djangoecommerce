from decimal import Decimal

from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from livesettings.functions import config_value
from product.models import Product
from satchmo_store.shop.models import OrderPaymentFailure, OrderPayment, OrderAuthorization
from satchmo_store.shop.signals import satchmo_cart_details_query, satchmo_cart_add_complete
from satchmo_utils.numbers import RoundedDecimalError, round_decimal, PositiveRoundedDecimalField
from payment.config import labelled_gateway_choices
import logging

log = logging.getLogger('shop.forms')


class MultipleProductForm(forms.Form):
    """A form used to add multiple products to the cart."""

    def __init__(self, *args, **kwargs):
        products = kwargs.pop('products', None)

        super(MultipleProductForm, self).__init__(*args, **kwargs)

        if products:
            products = [p for p in products if p.active]
        else:
            products = Product.objects.active_by_site()

        self.slugs = [p.slug for p in products]

        for product in products:
            kw = {
                'label' : product.name,
                'help_text' : product.description,
                'initial' : 0,
                'widget' : forms.TextInput(attrs={'class': 'text'}),
                'required' : False
            }

            qty = PositiveRoundedDecimalField(**kw)
            qty.product = product
            self.fields['qty__%s' % product.slug] = qty

    def save(self, cart, request):
        log.debug('saving');
        self.full_clean()
        cartplaces = config_value('SHOP', 'CART_PRECISION')
        roundfactor = config_value('SHOP', 'CART_ROUNDING')
        site = Site.objects.get_current()

        for name, value in self.cleaned_data.items():
            opt, key = name.split('__')
            log.debug('%s=%s', opt, key)

            quantity = 0
            product = None

            if opt=='qty':
                try:
                    quantity = round_decimal(value, places=cartplaces, roundfactor=roundfactor)
                except RoundedDecimalError:
                    quantity = 0

            if not key in self.slugs:
                log.debug('caught attempt to add product not in the form: %s', key)
            else:
                try:
                    product = Product.objects.get(slug=key, site=site)
                except Product.DoesNotExist:
                    log.debug('caught attempt to add an non-existent product, ignoring: %s', key)

            if product and quantity > Decimal('0'):
                log.debug('Adding %s=%s to cart from MultipleProductForm', key, value)
                details = []
                formdata = request.POST
                satchmo_cart_details_query.send(
                    cart,
                    product=product,
                    quantity=quantity,
                    details=details,
                    request=request,
                    form=formdata
                )
                added_item = cart.add_item(product, number_added=quantity, details=details)
                satchmo_cart_add_complete.send(cart, cart=cart, cartitem=added_item,
                    product=product, request=request, form=formdata)


EMAIL_CHOICES = (
    ("General Question", _("General question")),
    ("Order Problem", _("Order problem")),
)

class ContactForm(forms.Form):
    name = forms.CharField(label=_("Name"), max_length=100)
    sender = forms.EmailField(label=_("Email address"), max_length=75)
    subject = forms.CharField(label=_("Subject"))
    inquiry = forms.ChoiceField(label=_("Inquiry"), choices=EMAIL_CHOICES)
    contents = forms.CharField(label=_("Contents"), widget=forms.widgets.Textarea(attrs={'cols': 40, 'rows': 5}))


class OrderPaymentBaseAdminForm(forms.ModelForm):
    payment = forms.ChoiceField(required=False)        
    
    def __init__(self, *args, **kwargs):
        super(OrderPaymentBaseAdminForm, self).__init__(*args, **kwargs)
        self.fields['payment'].choices = [('','--------')] + labelled_gateway_choices()