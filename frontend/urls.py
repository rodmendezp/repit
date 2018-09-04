from django.conf.urls import url
from frontend import views

#TODO: CREATE UserCreate (View) and add it
urlpatterns = [
    url(r'^$', views.index),
    url(r'^accounts/$', views.auth),
    url(r'^accounts/register/', views.UserCreate.as_view()),
    url(r'^app/$', views.app),
]
