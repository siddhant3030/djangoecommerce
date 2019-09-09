from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, TemplateView
from django.http import Http404

from satchmo_store.shop.models import Order
from satchmo_utils.views import bad_or_missing
from payment.utils import gift_certificate_processor


# def success(request):
#     """
#     The order has been succesfully processed.  This can be used to generate a receipt or some other confirmation
#     """
#     try:
#         order = Order.objects.from_request(request)
#     except Order.DoesNotExist:
#         return bad_or_missing(request, _('Your order has already been processed.'))

#     del request.session['orderID']
#     # We check to see if there are any gift certificates in the order
#     gc_email_sent = False
#     gc_in_orderitems = len(filter(lambda x: 'GiftCertificateProduct' in x.product.get_subtypes(), order.orderitem_set.all()))
#     if gc_in_orderitems:
#         gc_email_sent = gift_certificate_processor(order)
#     return render(request, 'shop/checkout/success.html',
#                               {'order': order,
#                                'gc_email_sent': gc_email_sent})


class SuccessDetailView(DetailView):
    model = Order
    template_name = "shop/checkout/success.html"
    context_object_name = "order"
    
    def get_object(self, queryset=None):
        try:
            return self.model.objects.from_request(self.request)
        except:
            raise Http404("Your order has already been processed.")
        del self.request.session['orderID']
            
    def get_context_data(self, **kwargs):
        context = super(SuccessDetailView, self).get_context_data(**kwargs)
        gc_email_sent = False
        gc_in_orderitems = len(list(filter(lambda x: 'GiftCertificateProduct' in x.product.get_subtypes(), self.object.orderitem_set.all())))
        if gc_in_orderitems:
            gc_email_sent = gift_certificate_processor(self.object)
        context['gc_email_sent'] = gc_email_sent
        return context
                
success = never_cache(SuccessDetailView.as_view())


class FailureTemplateView(TemplateView):
    template_name = "shop/checkout/failure.html"
    
failure = FailureTemplateView.as_view()
    
# def failure(request):
#     return render(request, 'shop/checkout/failure.html')
