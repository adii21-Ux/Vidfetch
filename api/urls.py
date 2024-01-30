from django.urls import path, include
from . import views

urlpatterns = [
    path('get-videos/', views.VideoListView.as_view(), name="get_videos"),
    path('delete-all-videos/', views.DeleteAllVideosView.as_view(), name='delete_all_videos'),
    path('filter-videos/', views.FilteredVideoListView.as_view(), name='delete_all_videos'),
]
