from django.conf.urls import url
from frontend import views
from backend.requests import is_user


urlpatterns = [
    url(r'^$', views.index),
    url(r'^accounts/$', views.auth),
    url(r'^accounts/register/', views.UserCreate.as_view()),
    url(r'^accounts/is_user/', is_user),
    url(r'^app/$', views.app),
]
