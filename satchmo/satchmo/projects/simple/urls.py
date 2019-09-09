from django.conf.urls import url, include

from satchmo_store.urls import urlpatterns

urlpatterns += [
    url(r'test/', include('simple.localsite.urls'))
]
