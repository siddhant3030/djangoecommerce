"""
ProductShipping  models
"""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _
from shipping.modules.base import BaseShipper
from product.models import Product
import datetime
import logging
import operator

log = logging.getLogger('shipping.productshipping')

class ProductShippingPriceException(Exception):
    def __init__(self, reason):
        self.reason = reason

class Shipper(BaseShipper):

    def __init__(self, carrier):
        self.id = carrier.key
        self.carrier = carrier
        super(BaseShipper, self).__init__()

    def __str__(self):
        """
        This is mainly helpful for debugging purposes
        """
        return "Shipper: %s" % self.id

    def description(self):
        """
        A basic description that will be displayed to the user when selecting their shipping options
        """
        return self.carrier.description

    def cost(self):
        """
        Complex calculations can be done here as long as the return value is a dollar figure
        """
        assert(self._calculated)
        total = Decimal("0.00")
        for cartitem in self.cart.cartitem_set.all():
            p = cartitem.product
            if p.is_shippable:
                total += self.carrier.price(p) * cartitem.quantity
        return total

    def method(self):
        """
        Describes the actual delivery service (Mail, FedEx, DHL, UPS, etc)
        """
        return self.carrier.method

    def expectedDelivery(self):
        """
        Can be a plain string or complex calcuation returning an actual date
        """
        return self.carrier.delivery

    def valid(self, order=None):
        """
        Can do complex validation about whether or not this option is valid.
        For example, may check to see if the recipient is in an allowed country
        or location.
        """
        if order:
            try:
                for item in order.orderitem_set.all():
                    p = item.product
                    price = self.carrier.price(p)
                            
            except ProductShippingPriceException:
                return False
                
        elif self.cart:
            try:
                price = self.cost()
            
            except ProductShippingPriceException:
                return False
                        
        return True


@python_2_unicode_compatible
class Carrier(models.Model):
    key = models.SlugField(_('Key'))
    ordering = models.IntegerField(_('Ordering'), default=0)
    active = models.BooleanField(_('Active'), default=True)

    def _find_translation(self, language_code=None):
        if not language_code:
            language_code = get_language()
            
        c = self.translations.filter(languagecode__exact = language_code)
        ct = c.count()

        if not c or ct == 0:
            pos = language_code.find('-')
            if pos>-1:
                short_code = language_code[:pos]
                log.debug("Carrier: Trying to find root language content for: [%s]", short_code)
                c = self.translations.filter(languagecode__exact = short_code)
                ct = c.count()
                if ct>0:
                    log.debug("Carrier: Found root language content for: [%s]", short_code)

        if not c or ct == 0:
            #log.debug("Trying to find default language content for: %s", self)
            c = self.translations.filter(languagecode__istartswith = settings.LANGUAGE_CODE)
            ct = c.count()

        if not c or ct == 0:
            #log.debug("Trying to find *any* language content for: %s", self)
            c = self.translations.all()
            ct = c.count()

        if ct > 0:
            trans = c[0]
        else:
            trans = None

        return trans

    def delivery(self):
        """Get the delivery, looking up by language code, falling back intelligently.
        """
        trans = self._find_translation()

        if trans:
            return trans.delivery
        else:
            return ""

    delivery = property(delivery)
 
    def description(self):
        """Get the description, looking up by language code, falling back intelligently.
        """
        trans = self._find_translation()

        if trans:
            return trans.description
        else:
            return ""

    description = property(description)
    
    def method(self):
        """Get the description, looking up by language code, falling back intelligently.
        """
        trans = self._find_translation()

        if trans:
            return trans.method
        else:
            return ""

    method = property(method)    
 
    def name(self):
        """Get the name, looking up by language code, falling back intelligently.
        """
        trans = self._find_translation()

        if trans:
            return trans.name
        else:
            return ""

    name = property(name)
    
    def price(self, product):
        """Get a price for this product."""
        prices = product.smart_relation('shipping_price')
        try:
            return prices.filter(carrier=self)[0].price
        except (AttributeError, IndexError):
            log.debug("No %s shipping price found for %s", self, product.slug)
            raise ProductShippingPriceException('No price available')
            
    def __str__(self):
        return "Carrier: %s [%s]" % (self.name, self.method)
        
    class Meta:
        ordering = ('ordering',)
        
        
class CarrierTranslation(models.Model):
    carrier = models.ForeignKey('Carrier', related_name='translations', on_delete=models.CASCADE)
    languagecode = models.CharField(_('language'), max_length=10, choices=settings.LANGUAGES)
    name = models.CharField(_('Carrier'), max_length=50, )
    description = models.CharField(_('Description'), max_length=200)
    method = models.CharField(_('Method'), help_text=_("i.e. US Mail"), max_length=200)
    delivery = models.CharField(_('Delivery Days'), max_length=200)
    
    class Meta:
        ordering=('languagecode','name')


@python_2_unicode_compatible
class ProductShippingPrice(models.Model):
    product = models.ForeignKey(Product, related_name="shipping_price", on_delete=models.CASCADE)
    carrier = models.ForeignKey('Carrier', related_name='tiers', on_delete=models.CASCADE)
    price = models.DecimalField(_("Shipping Price"), max_digits=10, decimal_places=2, )
    
    def __str__(self):
        return "ProductShippingPrice: %s" % self.price
    
    class Meta:
        ordering = ('carrier','price')

from . import config
