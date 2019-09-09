from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from l10n.utils import moneyfmt
from satchmo_store.shop.models import Order


@python_2_unicode_compatible
class PurchaseOrder(models.Model):
    po_number = models.CharField(_('Customer PO Number'), max_length=20)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    balance = models.DecimalField(_("Outstanding Balance"),
        max_digits=18, decimal_places=10, blank=True, null=True)
    paydate = models.DateField(_('Paid on'), blank=True, null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    def __str__(self):
        return "PO: #%s" % self.po_number

    def balance_due(self):
        if self.balance:
            b = self.balance
        else:
            b = Decimal('0.00')
            
        return moneyfmt(b)

    def order_link(self):
        return mark_safe('<a href="/admin/shop/order/%i/">%s #%i (%s)</a>' % (
            self.order.id,
            ugettext('Order'), 
            self.order.id, 
            moneyfmt(self.order.total)))
            
    order_link.allow_tags = True
    
    def save(self):
        if self.balance is None:
            self.balance = self.order.balance
        super(PurchaseOrder, self).save()

from . import config
PAYMENT_PROCESSOR=True
