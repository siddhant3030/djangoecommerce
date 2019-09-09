from django import http
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.utils.translation import ugettext
from django.views.generic import DetailView, FormView, DeleteView
from django.views.generic.detail import SingleObjectMixin
try:
    from django.core.urlresolvers import reverse, reverse_lazy
except ImportError:
    from django.urls import reverse, reverse_lazy

from satchmo_store.contact import signals, CUSTOMER_ID
from satchmo_store.contact.forms import ExtendedContactInfoForm, ContactInfoForm, area_choices_for_country, AddressBookForm, YesNoForm
from satchmo_store.contact.models import Contact, AddressBook
from satchmo_store.shop.models import Config
import logging
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger('satchmo_store.contact.views')


class ContactDetailView(DetailView):
    model = Contact
    template_name = "contact/view_profile.html"
    context_object_name = "user_data"

    def get_object(self):
        try:
            return self.request.user.contact
        except Contact.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)
        signals.satchmo_contact_view.send(self.object, contact=self.object, contact_dict=context)        
        return context
        
view = login_required(ContactDetailView.as_view())            
        
# def view(request):
#     """View contact info."""
#     try:
#         user_data = Contact.objects.get(user=request.user.id)
#     except Contact.DoesNotExist:
#         user_data = None

#     contact_dict = {
#         'user_data': user_data,
#     }

#     signals.satchmo_contact_view.send(user_data, contact=user_data, contact_dict=contact_dict)

#     return render(request, 'contact/view_profile.html', contact_dict)


class ContactFromRequestMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.contact = self.get_contact()
        return super(ContactFromRequestMixin, self).dispatch(request, *args, **kwargs)
    
    def get_contact(self, create=False):
        try:
            return Contact.objects.from_request(self.request, create=create)
        except Contact.DoesNotExist:
            pass


class ContactUpdateView(ContactFromRequestMixin, SingleObjectMixin, FormView):
    template_name = "contact/update_form.html"
    model = Contact
    form_class = ExtendedContactInfoForm
    success_url = reverse_lazy('satchmo_account_info')
    context_object_name = "contact"
    
    def get_contact(self):
        contact = super(ContactUpdateView, self).get_contact()
        self.object = contact
        return contact

    def dispatch(self, request, *args, **kwargs):
        self.shop = Config.objects.get_current()
        return super(ContactUpdateView, self).dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        self.next_url = self.request.GET.get(REDIRECT_FIELD_NAME)
        return super(ContactUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.next_url = self.request.POST.get(REDIRECT_FIELD_NAME)
        return super(ContactUpdateView, self).post(request, *args, **kwargs)
            
    def form_valid(self, form):
        if self.object is None and self.request.user:
            self.object = self.model(user=self.request.user)
        cust_id = form.save(contact=self.object)
        self.request.session[CUSTOMER_ID] = cust_id
        return super(ContactUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ContactUpdateView, self).get_form_kwargs()
        kwargs["shop"] = self.shop
        kwargs["contact"] = self.object        
        kwargs["shippable"] = True
        return kwargs

    def get_success_url(self):
        if self.next_url and not '//' in self.next_url and not ' ' in self.next_url:
            return self.next_url
        return super(ContactUpdateView, self).get_success_url()

    def get_initial(self):
        init_data = super(ContactUpdateView, self).get_initial()
        init_data['next'] = self.next_url        
        if self.object:
            #If a person has their contact info, make sure we populate it in the form
            for item in self.object.__dict__.keys():
                init_data[item] = getattr(self.object, item)
            if self.object.shipping_address:
                for item in self.object.shipping_address.__dict__.keys():
                    init_data["ship_" + item] = getattr(self.object.shipping_address, item)
            if self.object.billing_address:
                for item in self.object.billing_address.__dict__.keys():
                    init_data[item] = getattr(self.object.billing_address, item)
            if self.object.primary_phone:
                init_data['phone'] = self.object.primary_phone.phone
            if self.object.organization:
                init_data['organization'] = self.object.organization.name
        else:
            #If a person has no contact info, try to get some from its user account
            if self.request.user:
                for field in ('email', 'first_name', 'last_name'):
                    if getattr(self.request.user, field, False):
                        init_data[field] = getattr(self.request.user, field)
        signals.satchmo_contact_view.send(self.object, contact=self.object, contact_dict=init_data)
        return init_data
        
    def get_context_data(self, **kwargs):
        context = super(ContactUpdateView, self).get_context_data(**kwargs)
        context['next'] = self.next_url
        if self.shop.in_country_only:
            context['country'] = self.shop.sales_country
        else:
            countries = self.shop.countries()
            if countries and countries.count() == 1:
                context['country'] = countries[0]
        return context

update = login_required(ContactUpdateView.as_view())
        
# def update(request):
#     """Update contact info"""

#     init_data = {}
#     shop = Config.objects.get_current()

#     try:
#         contact = Contact.objects.from_request(request, create=False)
#     except Contact.DoesNotExist:
#         contact = None


#     if request.method == "POST":
#         new_data = request.POST.copy()
#         init_data['next'] = request.POST.get(REDIRECT_FIELD_NAME, '')
#         form = ExtendedContactInfoForm(data=new_data, shop=shop, contact=contact, shippable=True,
#             initial=init_data)

#         if form.is_valid():
#             if contact is None and request.user:
#                 contact = Contact(user=request.user)
#             custID = form.save(contact=contact)
#             request.session[CUSTOMER_ID] = custID
#             redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
#             if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
#                 redirect_to = reverse('satchmo_account_info')

#             return http.HttpResponseRedirect(redirect_to)
#         else:
#             signals.satchmo_contact_view.send(contact, contact=contact, contact_dict=init_data)

#     else:
#         init_data['next'] = request.GET.get(REDIRECT_FIELD_NAME, '')
#         if contact:
#             #If a person has their contact info, make sure we populate it in the form
#             for item in contact.__dict__.keys():
#                 init_data[item] = getattr(contact,item)
#             if contact.shipping_address:
#                 for item in contact.shipping_address.__dict__.keys():
#                     init_data["ship_"+item] = getattr(contact.shipping_address,item)
#             if contact.billing_address:
#                 for item in contact.billing_address.__dict__.keys():
#                     init_data[item] = getattr(contact.billing_address,item)
#             if contact.primary_phone:
#                 init_data['phone'] = contact.primary_phone.phone
#             if contact.organization:
#                 init_data['organization'] = contact.organization.name
#         else:
#             #If a person has no contact info, try to get some from its user account
#             if request.user:
#                 for field in ('email', 'first_name', 'last_name'):
#                     if getattr(request.user, field, False):
#                         init_data[field] = getattr(request.user, field)


#         signals.satchmo_contact_view.send(contact, contact=contact, contact_dict=init_data)
#         form = ExtendedContactInfoForm(shop=shop, contact=contact, shippable=True, initial=init_data)

#     init_data['form'] = form
#     if shop.in_country_only:
#         init_data['country'] = shop.sales_country
#     else:
#         countries = shop.countries()
#         if countries and countries.count() == 1:
#             init_data['country'] = countries[0]

#     return render(request, 'contact/update_form.html', init_data)


class AddressCreateEditView(ContactFromRequestMixin, SingleObjectMixin, FormView):
    template_name = "contact/address_form.html"
    model = AddressBook
    form_class = AddressBookForm
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('satchmo_account_info')
    context_object_name = "entry"
    
    def get_object(self):
        try:
            super(AddressCreateEditView, self).get_object()
        except AttributeError:
            pass

    def dispatch(self, request, *args, **kwargs):
        self.next_url = request.GET.get('next', None)
        self.contact = self.get_contact()
        self.object = self.get_object()
        if self.object and not self.object.contact == self.contact:
            return http.HttpResponseRedirect(self.success_url)        
        return super(FormView, self).dispatch(request, *args, **kwargs)
            
    def form_valid(self, form):
        form.save(self.contact, address_entry=self.object)
        messages.success(self.request, _('Succcessfully saved addressbook changes.'))
        return super(AddressCreateEditView, self).form_valid(form)

    def get_success_url(self):
        if self.next_url:
            return self.next_url
        return super(AddressCreateEditView, self).get_success_url()

    def get_initial(self):
        initial_data = super(AddressCreateEditView, self).get_initial()
        if self.object:
            initial_data = model_to_dict(self.object, fields=[], exclude=['contact'])
            initial_data['addressee_name'] = initial_data["addressee"]
        return initial_data
        
    def get_context_data(self, **kwargs):
        context = super(AddressCreateEditView, self).get_context_data(**kwargs)
        context['next'] = self.next_url
        context['editing'] = self.object
        return context

address_create_edit = login_required(AddressCreateEditView.as_view())
        
# def address_create_edit(request, id=None):
#     """Create and edit new address book entries
#     """
#     initial_entry = None
#     initial_data = {}
#     editing = False
#     next_url = request.GET.get('next',None)
#     try:
#         contact = Contact.objects.from_request(request, create=False)
#     except Contact.DoesNotExist:
#         contact = None
#     if id:
#         initial_entry = get_object_or_404(AddressBook, pk=id)
#         # Make sure we only edit entries associated with this contact
#         if not initial_entry.contact == contact:
#             return http.HttpResponseRedirect(reverse('satchmo_account_info'))
#         initial_data = model_to_dict(initial_entry, fields=[], exclude=['contact'])
#         # This is a bit of a hack because we normally use jquery to populate the addressee
#         initial_data['addressee_name'] = initial_data["addressee"]
#     if request.method == 'POST':
#         form = AddressBookForm(request.POST)
#         if form.is_valid():
#             form.save(contact, address_entry=initial_entry)
#             messages.success(request, _('Succcessfully saved addressbook changes.'))
#             if next_url:
#                 return http.HttpResponseRedirect(next_url)
#             else:
#                 return http.HttpResponseRedirect(reverse('satchmo_account_info'))
#     else:
#         form = AddressBookForm(initial=initial_data)
#     if initial_entry:
#         editing = True
#     context = {'form':form, 'editing':editing, 'entry':initial_entry, 'next':next_url}  
#     return render(request, 'contact/address_form.html', context)
    

class AddressDeleteView(ContactFromRequestMixin, DeleteView):
    model = AddressBook
    template_name = 'contact/address_form_delete.html'
    success_url = reverse_lazy('satchmo_account_info')
    context_object_name = "entry"
    pk_url_kwarg = 'id'

    def get_object(self):
        try:
            super(AddressDeleteView, self).get_object()
        except AttributeError:
            pass

    def dispatch(self, request, *args, **kwargs):
        self.contact = self.get_contact()
        self.object = self.get_object()
        if self.object and not self.object.contact == self.contact:
            return http.HttpResponseRedirect(self.success_url)        
        return super(DeleteView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if self.object and request.POST['delete_entry'] == 'Yes':            
            return super(AddressDeleteView, self).post(request, *args, **kwargs)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.object.delete()
        return http.HttpResponseRedirect(success_url)
        
    def get_context_data(self, **kwargs):
        context = super(AddressDeleteView, self).get_context_data(**kwargs)
        context['form'] = YesNoForm()
        return context

address_delete = login_required(AddressDeleteView.as_view())        
    
# def address_delete(request, id=None):
#     """Delete an addressbook entry
#     """
#     initial_entry = None
#     try:
#         contact = Contact.objects.from_request(request, create=False)
#     except Contact.DoesNotExist:
#         contact = None
#     if id:
#         initial_entry = get_object_or_404(AddressBook, pk=id)
#         # Make sure we only edit entries associated with this contact
#         if not initial_entry.contact == contact:
#             return http.HttpResponseRedirect(reverse('satchmo_account_info'))
#     if request.method == 'POST' and initial_entry:
#         if request.POST['delete_entry'] == 'Yes':
#             initial_entry.delete()
#         return http.HttpResponseRedirect(reverse('satchmo_account_info'))
#     else:
#         form = YesNoForm()
#     context = {'form':form,'entry':initial_entry}   
#     return render(request, 'contact/address_form_delete.html', context)
    

class AjaxGetStateException(Exception):
    """Used to barf."""
    def __init__(self, message):
        self.message = message

def ajax_get_state(request, **kwargs):
    formdata = request.REQUEST.copy()

    try:
        if "country" in formdata:
            country_field = 'country'
        elif "ship_country" in formdata:
            country_field = 'ship_country'
        else:
            raise AjaxGetStateException("No country specified")

        form = ContactInfoForm(data=formdata)
        country_data = formdata.get(country_field)
        try:
            country_obj = form.fields[country_field].clean(country_data)
        except:
            raise AjaxGetStateException("Invalid country specified")

        areas = area_choices_for_country(country_obj, ugettext)

        return render(request, 'contact/_state_choices.html', { 'areas': areas })
    except AjaxGetStateException as e:
        log.error("ajax_get_state aborting: %s" % e.message)

    return http.HttpResponseServerError()
