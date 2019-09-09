"""
Used to manage raw inventory and supplier relationships.  This is still
under heavy development.
"""
import datetime
import six

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _

from satchmo_store.contact.models import Contact, Organization


@python_2_unicode_compatible
class RawItem(models.Model):
    """
    A raw good supplied by a supplier.  For instance, it could be a plain 
    shirt that you process to make your Item
    """
    supplier = models.ForeignKey(Organization, verbose_name=_('Supplier'), on_delete=models.CASCADE)
    supplier_num = models.CharField(_("Supplier ID"), max_length=50)
    description = models.CharField(_("Description"), max_length=200)
    unit_cost = models.DecimalField(_("Unit Cost"), max_digits=6, decimal_places=2)
    inventory = models.DecimalField(_("Inventory"),  max_digits=18,  decimal_places=6)
    
    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = _("Raw Item")
        verbose_name_plural = _("Raw Items")


@python_2_unicode_compatible
class SupplierOrder(models.Model):
    """
    An order the store owner places to a supplier for a raw good.
    """
    supplier = models.ForeignKey(Organization, verbose_name=_('Supplier'), on_delete=models.CASCADE)
    date_created = models.DateField(_("Date Created"))
    order_sub_total = models.DecimalField(_("Subtotal"), max_digits=6, decimal_places=2)
    order_shipping = models.DecimalField(_("Shipping"), max_digits=6, decimal_places=2)
    order_tax = models.DecimalField(_("Tax"), max_digits=6, decimal_places=2)
    order_notes = models.CharField(_("Notes"), max_length=200, blank=True)
    order_total = models.DecimalField(_("Total"), max_digits=6, decimal_places=2)
    
    def __str__(self):
        return six.text_type(self.date_created)
    
    def _status(self):
        return(self.supplierorderstatus_set.latest('date').status)
    status = property(_status)  
    
    def save(self, **kwargs):
        """Ensure we have a date_created before saving the first time."""
        if not self.pk:
            self.date_created = datetime.date.today()
        super(SupplierOrder, self).save(**kwargs)
    
    class Meta:
        verbose_name = _("Supplier Order")
        verbose_name_plural = _("Supplier Orders")
    
    
@python_2_unicode_compatible
class SupplierOrderItem(models.Model):
    """
    Individual line items for an order
    """
    order = models.ForeignKey(SupplierOrder, on_delete=models.CASCADE)
    line_item = models.ForeignKey(RawItem, verbose_name=_('Line Item'), on_delete=models.CASCADE)
    line_item_quantity = models.IntegerField(_("Line Item Quantity"), )
    line_item_total = models.DecimalField(_("Line Item Total"), max_digits=6,decimal_places=2)
    
    def __str__(self):
        return six.text_type(self.line_item_total) 


SUPPLIERORDER_STATUS = (
    (_('Sent in'), _('Sent in')),
    (_('Shipped'), _('Shipped')),
    (_('Received'), _('Received')),
)


@python_2_unicode_compatible
class SupplierOrderStatus(models.Model):
    """
    Status of a supplier's order.  There will be multiple statuses as it is
    placed and subsequently processed and received.
    """
    order = models.ForeignKey(SupplierOrder, on_delete=models.CASCADE)
    status = models.CharField(_("Status"), max_length=20, choices=SUPPLIERORDER_STATUS, blank=True)
    notes = models.CharField(_("Notes"), max_length=100, blank=True)
    date = models.DateTimeField(_('Date'), blank=True)
    
    def __str__(self):
        return self.status
        
    class Meta:
        verbose_name = _("Supplier Order Status")
        verbose_name_plural = _("Supplier Order Statuses")
