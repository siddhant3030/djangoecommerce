"""
URLConf for Django user registration.

Recommended usage is to use a call to ``include()`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/accounts/'.

"""
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from satchmo_store.accounts.views import RegistrationComplete
# extending the urls in contacts
from satchmo_store.contact.urls import urlpatterns
from satchmo_utils.signals import collect_urls
from satchmo_store import accounts
# The following import of satchmo_store.contact.config should not be removed
# because it is sometimes indirectly important for loading config_value('SHOP', 'ACCOUNT_VERIFICATION')
import satchmo_store.contact.config

# Activation keys get matched by \w+ instead of the more specific
# [a-fA-F0-9]+ because a bad activation key should still get to the view;
# that way it can return a sensible "invalid key" message instead of a
# confusing 404.
urlpatterns += [
    url(r'^activate/(?P<activation_key>\w+)/$', accounts.views.activate, name='registration_activate'),
    url(r'^login/$', accounts.views.emaillogin, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^register/$', accounts.views.register, name='registration_register'),
    url(r'^secure/login/$', accounts.views.emaillogin, {'SSL' : True, 'template_name': 'registration/login.html'}, name='auth_secure_login'),
]

urlpatterns += [
    url('^logout/$', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='auth_logout'),
]

urlpatterns += [
    url(r'^register/complete/$', RegistrationComplete.as_view(template_name='registration/registration_complete.html'), name='registration_complete'),
]

#Dictionary for authentication views
password_reset_dict = {
    'template_name': 'registration/password_reset_form.html',
    'email_template_name': 'registration/password_reset.txt',
}

# the "from email" in password reset is problematic... it is hard coded as None
urlpatterns += [
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), password_reset_dict, name='auth_password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='auth_password_change'),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view()),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view()),
]

collect_urls.send(sender=accounts, patterns=urlpatterns)
