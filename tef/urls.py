from django.conf.urls import url
from . import views

app_name = 'tef'
urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^review/(?P<te_id>[0-9]+)/$', views.review, name='review')
]
