from django.conf.urls import url

from .views import home_view, host_view

urlpatterns = [
	url(r'^$', home_view),
    url(r'^(?P<host_name>\w*)/$', host_view, name='host'),
    
    
]