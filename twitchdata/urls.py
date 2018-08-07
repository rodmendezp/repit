from django.conf.urls import url
from twitchdata import views


urlpatterns = [
    url(r'^twitch_user/$', views.TwitchUserList.as_view()),
    url(r'^twitch_user/(?P<pk>[0-9]+)$', views.TwitchUserDetail.as_view()),
    url(r'^channel/$', views.ChannelList.as_view()),
    url(r'^channel/(?P<pk>[0-9]+)$', views.ChannelDetail.as_view()),
    url(r'^streamer/$', views.StreamerList.as_view()),
    url(r'^streamer/(?P<pk>[0-9]+)$', views.StreamerDetail.as_view()),
    url(r'^game/$', views.GameList.as_view()),
    url(r'^game/(?P<pk>[0-9]+)$', views.GameDetail.as_view()),
    url(r'^video/$', views.VideoList.as_view()),
    url(r'^video/(?P<pk>[0-9]+)$', views.VideoDetail.as_view()),
    url(r'^clip/$', views.ClipList.as_view()),
    url(r'^clip/(?P<pk>[0-9]+)$', views.ClipDetail.as_view()),
    url(r'^emoticon/$', views.EmoticonList.as_view()),
    url(r'^emoticon/(?P<pk>[0-9]+)$', views.EmoticonDetail.as_view()),
    url(r'^chat/$', views.ChatList.as_view()),
    url(r'^chat/(?P<pk>[0-9]+)$', views.ChatDetail.as_view()),
    url(r'^message/$', views.MessageList.as_view()),
    url(r'^message/(?P<pk>[0-9]+)$', views.MessageDetail.as_view()),
]