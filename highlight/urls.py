from django.conf.urls import url
from highlight import views


urlpatterns = [
    url(r'^type/$', views.TypeList.as_view()),
    url(r'^type/(?P<pk>[0-9]+)$', views.TypeDetail.as_view()),
    url(r'^highlight/$', views.HighlightList.as_view()),
    url(r'^highlight/(?P<pk>[0-9]+)$', views.HighlightDetail.as_view()),
]