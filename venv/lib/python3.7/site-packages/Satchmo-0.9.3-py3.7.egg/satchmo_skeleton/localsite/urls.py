from django.conf.urls import url

from simple.localsite.views import example

urlpatterns = [
    url(r'example/', example),
]
