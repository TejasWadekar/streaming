from django.urls import path
from .views import StreamVideoView, render_video_stream

urlpatterns = [
    path(
        "stream/<int:candidate_id>/",
        StreamVideoView.as_view(),
        name="stream_video",
    ),
    path(
        "video/<int:candidate_id>/",
        render_video_stream,
        name="render_video_stream",
    ),
]
