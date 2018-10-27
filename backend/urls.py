from django.conf.urls import url
from backend import views


urlpatterns = [
    url(r'^task/$', views.TaskView.as_view()),
    url(r'^filler_game/$', views.FillerGame.as_view()),
    url(r'^filler_streamer/$', views.FillerStreamer.as_view()),
    url(r'^game_queue_status/$', views.GameQueueStatus.as_view()),
    url(r'^custom_queue_status/$', views.CustomQueueStatus.as_view())
]
