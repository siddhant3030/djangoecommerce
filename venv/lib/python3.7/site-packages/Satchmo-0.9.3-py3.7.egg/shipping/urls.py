from django.conf.urls import url

from shipping.views import displayDoc

#Urls which need to be loaded at root level.
adminpatterns = [
    url(r'^admin/print/(?P<doc>[-\w]+)/(?P<id>\d+)', displayDoc, name='satchmo_print_shipping'),
]