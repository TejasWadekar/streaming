from django.urls import path
from .views import StreamVideoView, render_video_stream

urlpatterns = [
    path(
        "stream/",
        StreamVideoView.as_view(),
        name="stream_video",
    ),
    path(
        "video/",
        render_video_stream,
        name="render_video_stream",
    ),
]
