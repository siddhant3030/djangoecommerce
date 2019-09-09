from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView

from satchmo_store.contact.models import Contact
from satchmo_store.contact.views import ContactFromRequestMixin
from satchmo_store.shop.models import Order
from satchmo_utils.views import bad_or_missing
from livesettings.functions import config_value 


class OrderHistoryView(DetailView):
    model = Contact
    template_name = 'shop/order_history.html'
    context_object_name = 'contact'

    def get_object(self, queryset=None):
        return self.model.objects.from_request(self.request, create=False)
        
    def get_context_data(self, **kwargs):
        context = super(OrderHistoryView, self).get_context_data(**kwargs)
        context['default_view_tax'] = config_value('TAX', 'DEFAULT_VIEW_TAX')
        context['orders'] = self.get_orders()
        return context        

    def get_orders(self):
        return Order.objects.filter(contact=self.object).order_by('-time_stamp')

order_history = login_required(OrderHistoryView.as_view())
        

# def order_history(request):
#     orders = None
#     try:
#         contact = Contact.objects.from_request(request, create=False)
#         orders = Order.objects.filter(contact=contact).order_by('-time_stamp')
    
#     except Contact.DoesNotExist:
#         contact = None
        
#     ctx = {
#         'contact' : contact,
#         'default_view_tax': config_value('TAX', 'DEFAULT_VIEW_TAX'),
#         'orders' : orders
#     }

#     return render(request, 'shop/order_history.html', ctx)

# order_history = login_required(order_history)


class OrderTrackingView(ContactFromRequestMixin, DetailView):
    model = Order
    template_name = 'shop/order_tracking.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    contact = None

    def get_queryset(self):
        queryset = super(OrderTrackingView, self).get_queryset()
        if self.contact:
            return queryset.filter(contact=self.contact)
        else:
            return queryset.none()
        
    def get_context_data(self, **kwargs):
        context = super(OrderTrackingView, self).get_context_data(**kwargs)
        context['default_view_tax'] = config_value('TAX', 'DEFAULT_VIEW_TAX')
        context['contact'] = self.contact
        return context        
            
order_tracking = login_required(OrderTrackingView.as_view())
        
        
# def order_tracking(request, order_id):
#     order = None
#     try:
#         contact = Contact.objects.from_request(request, create=False)
#         try:
#             order = Order.objects.get(id__exact=order_id, contact=contact)
#         except Order.DoesNotExist:
#             pass
#     except Contact.DoesNotExist:
#         contact = None

#     if order is None:
#         return bad_or_missing(request, _("The order you have requested doesn't exist, or you don't have access to it."))

#     ctx = {
#         'default_view_tax': config_value('TAX', 'DEFAULT_VIEW_TAX'),
#         'contact' : contact,
#         'order' : order
#     }

#     return render(request, 'shop/order_tracking.html', ctx)

# order_tracking = login_required(order_tracking)
