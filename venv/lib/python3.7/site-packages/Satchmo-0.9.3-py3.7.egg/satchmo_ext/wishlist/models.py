import datetime
import json

from django.db import models
from django.utils.translation import ugettext_lazy as _

from satchmo_store import shop
from satchmo_store.contact.models import Contact
from product.models import Product
from satchmo_store.shop.signals import cart_add_view
from satchmo_utils.signals import collect_urls
from .listeners import wishlist_cart_add_listener


class ProductWishManager(models.Manager):
    def create_if_new(self, product, contact, details):
        if details:
            encoded = json.dumps(details)
            products = ProductWish.objects.filter(product=product, contact=contact, _details=encoded)
        else:
            products = ProductWish.objects.filter(product=product, contact=contact, _details__isnull=True)

        if products and len(products) > 0:
            wish = products[0]
            if len(products) > 1:
                for p in products[1:]:
                    p.delete()
        else:
            wish = ProductWish(product=product, contact=contact)
            wish.details = details
            wish.save()
            
        return wish        


class ProductWish(models.Model):
    contact = models.ForeignKey(Contact, verbose_name=_("Contact"), related_name="wishlist", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_("Product"), related_name="wishes", on_delete=models.CASCADE)
    _details = models.TextField(_('Details'), null=True, blank=True)
    create_date = models.DateTimeField(_("Creation Date"))
    
    objects = ProductWishManager()

    class Meta:
        verbose_name = _('Product Wish')
        verbose_name_plural = _('Product Wishes')

    def set_details(self, raw):
        """Set the details from a raw list"""
        if raw:
            self._details = json.dumps(raw)
    
    def get_details(self):
        """Convert the pickled details into a list"""
        if self._details:
            return json.loads(self._details)
        else:
            return []

    details = property(fget=get_details, fset=set_details)

    def save(self, **kwargs):
        """Ensure we have a create_date before saving the first time."""
        if not self.pk:
            self.create_date = datetime.date.today()
        super(ProductWish, self).save(**kwargs)


cart_add_view.connect(wishlist_cart_add_listener)

from . import config
from .urls import add_wishlist_urls
collect_urls.connect(add_wishlist_urls, sender=shop)
