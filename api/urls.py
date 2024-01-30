from django.urls import path, include
from . import views

urlpatterns = [
    path('get-videos/', views.getData, name="get_videos"),
    path('delete-all-videos/', views.delete_all_videos, name='delete_all_videos'),
]
