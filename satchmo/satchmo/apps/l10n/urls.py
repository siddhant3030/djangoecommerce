from django.conf.urls import url
from django.views.i18n import set_language

urlpatterns = [
    url(r'^setlang/$', set_language, name='satchmo_set_language'),
]
