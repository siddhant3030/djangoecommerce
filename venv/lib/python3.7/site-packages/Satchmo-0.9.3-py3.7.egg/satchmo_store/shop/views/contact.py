from django import http
from django.shortcuts import render
from django.views.generic import FormView
try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy

from satchmo_store.mail import send_store_mail
from satchmo_store.shop.signals import contact_sender
from satchmo_store.shop.forms import ContactForm
import logging

log = logging.getLogger('satchmo_store.shop.views')

# Choices displayed to the user to categorize the type of contact request.

class ContactFormView(FormView):
    template_name = 'shop/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('satchmo_contact_thanks')
    
    def get_initial(self):
        initial = super(ContactFormView, self).get_initial()
        if self.request.user.is_authenticated:
            initial['sender'] = self.request.user.email
            initial['name'] = "%s %s" % (self.request.user.first_name, self.request.user.last_name)
        return initial

    def form_valid(self, form):
        c = {
            'request_type': form.cleaned_data['inquiry'],
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['sender'],
            'request_text': form.cleaned_data['contents']
        }
        send_store_mail(form.cleaned_data.get("subject", "Request"), c, 'shop/email/contact_us.txt',
                        send_to_store=True, sender=contact_sender)
        return super(ContactFormView, self).form_valid(form)
                
form = ContactFormView.as_view()        
