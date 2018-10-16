from django.conf.urls import url
from frontend import views
from backend.requests import is_user, user_activation


urlpatterns = [
    url(r'^$', views.index),
    url(r'^accounts/$', views.auth),
    url(r'^accounts/login/$', views.EmailLoginView.as_view()),
    url(r'^accounts/register/', views.UserCreate.as_view()),
    url(r'^accounts/is_user/', is_user),
    url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_activation, name='user_activation'),
    url(r'^app/$', views.app),
]
