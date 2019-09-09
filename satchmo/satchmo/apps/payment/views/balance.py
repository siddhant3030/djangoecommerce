from decimal import Decimal

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, UpdateView
from django.views.generic.detail import SingleObjectMixin
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from livesettings.functions import config_get_group
from payment import active_gateways
from payment.forms import PaymentMethodForm, CustomChargeForm
from satchmo_store.shop.models import Order, OrderItem
from satchmo_utils.dynamic import lookup_url
from satchmo_utils.views import bad_or_missing
import logging

log = logging.getLogger('payment.views.balance')
    
    
# def balance_remaining_order(request, order_id=None):
#     """Load the order into the session, so we can charge the remaining amount"""
#     # this will create an "OrderCart" - a fake cart to allow us to check out
#     request.session['cart'] = 'order'
#     request.session['orderID'] = order_id
#     return balance_remaining(request)
    

class BalanceRemainingView(SingleObjectMixin, FormView):
    model = Order
    template_name = "shop/checkout/balance_remaining.html"
    form_class = PaymentMethodForm
    context_object_name = "order"
    
    def get_object(self):
        try:
            return self.model.objects.get(pk=self.request.session.get('orderID'))
        except self.model.DoesNotExist:
            pass

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            return HttpResponseRedirect(reverse('satchmo_checkout-step1'))
        return super(BalanceRemainingView, self).dispatch(request, *args, **kwargs)
            
    def form_valid(self, form):
        modulename = form.cleaned_data['paymentmethod']
        if not modulename.startswith('PAYMENT_'):
            modulename = 'PAYMENT_' + modulename
        self.paymentmodule = config_get_group(modulename)
        return super(BalanceRemainingView, self).form_valid(form)
        
    def get_success_url(self):
        return lookup_url(self.paymentmodule, 'satchmo_checkout-step2')

    def get_form_kwargs(self):
        kwargs = super(BalanceRemainingView, self).get_form_kwargs()
        kwargs["order"] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(BalanceRemainingView, self).get_context_data(**kwargs)
        context['paymentmethod_ct'] = len(active_gateways())
        return context


class BalanceRemainingOrderView(BalanceRemainingView):
    pk_url_kwarg = 'order_id'
    
    def dispatch(self, request, *args, **kwargs):
        request.session['cart'] = 'order'
        request.session['orderID'] = kwargs.get(self.pk_url_kwarg)
        return super(BalanceRemainingOrderView, self).dispatch(request, *args, **kwargs)
        
        
# def balance_remaining(request):
#     """Allow the user to pay the remaining balance."""
#     order = None
#     orderid = request.session.get('orderID')
#     if orderid:
#         try:
#             order = Order.objects.get(pk=orderid)
#         except Order.DoesNotExist:
#             # TODO: verify user against current user
#             pass
            
#     if not order:
#         url = urlresolvers.reverse('satchmo_checkout-step1')
#         return HttpResponseRedirect(url)

#     if request.method == "POST":
#         new_data = request.POST.copy()
#         form = PaymentMethodForm(data=new_data, order=order)
#         if form.is_valid():
#             data = form.cleaned_data
#             modulename = data['paymentmethod']
#             if not modulename.startswith('PAYMENT_'):
#                 modulename = 'PAYMENT_' + modulename
            
#             paymentmodule = config_get_group(modulename)
#             url = lookup_url(paymentmodule, 'satchmo_checkout-step2')
#             return HttpResponseRedirect(url)
        
#     else:
#         form = PaymentMethodForm(order=order)
        
#     ctx = {
#         'form' : form, 
#         'order' : order,
#         'paymentmethod_ct': len(active_gateways())
#     }
#     return render(request, 'shop/checkout/balance_remaining.html', ctx)


class ChargeRemainingUpdateView(UpdateView):
    template_name = 'payment/admin/charge_remaining_confirm.html'
    model = OrderItem
    form_class = CustomChargeForm
    pk_url_kwarg = 'orderitem_id'

    def get_form_kwargs(self):
        kwargs = super(ChargeRemainingUpdateView, self).get_form_kwargs()
        kwargs["orderitem"] = self.object.pk
        kwargs["amount"] = self.object.product.customproduct.full_price
        return kwargs
    
    def get_success_url(self):
        #return reverse('journal', kwargs={'year': self.object.date.year, 'month': self.object.date.month, 'day': self.object.date.day})
        return '/admin/shop/order/%i' % self.object.order.pk
        
    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'Charged for custom product and recalculated totals.')
        return super(ChargeRemainingUpdateView, self).form_valid(form)
        
        
def charge_remaining(request, orderitem_id):
    """Given an orderitem_id, this returns a confirmation form."""
    
    try:
        orderitem = OrderItem.objects.get(pk = orderitem_id)
    except OrderItem.DoesNotExist:
        return bad_or_missing(request, _("The orderitem you have requested doesn't exist, or you don't have access to it."))
        
    amount = orderitem.product.customproduct.full_price
        
    data = {
        'orderitem' : orderitem_id,
        'amount' : amount,
        }
    form = CustomChargeForm(data)
    return render(request, 'payment/admin/charge_remaining_confirm.html', {'form' : form})

def charge_remaining_post(request):
    if not request.method == 'POST':
        return bad_or_missing(request, _("No form found in request."))
    
    data = request.POST.copy()
    
    form = CustomChargeForm(data)
    if form.is_valid():
        data = form.cleaned_data
        try:
            orderitem = OrderItem.objects.get(pk = data['orderitem'])
        except OrderItem.DoesNotExist:
            return bad_or_missing(request, _("The orderitem you have requested doesn't exist, or you don't have access to it."))
        
        price = data['amount']
        line_price = price*orderitem.quantity
        orderitem.unit_price = price
        orderitem.line_item_price = line_price
        orderitem.save()
        #print("Orderitem price now: %s" % orderitem.line_item_price)
        
        order = orderitem.order
    
        if not order.shipping_cost:
            order.shipping_cost = Decimal("0.00")
    
        if data['shipping']:
            order.shipping_cost += data['shipping']
            
        order.recalculate_total()
        
        messages.add_message(request, messages.INFO, 'Charged for custom product and recalculated totals.')

        notes = data['notes']
        if not notes:
            notes = 'Updated total price'
            
        order.add_status(notes=notes)
        
        return HttpResponseRedirect('/admin/shop/order/%i' % order.id)
    else:
        return render(request, 'admin/charge_remaining_confirm.html', {'form': form})
