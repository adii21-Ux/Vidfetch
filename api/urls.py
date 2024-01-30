from django.urls import path, include
from . import views

urlpatterns = [
    path('get-videos/', views.getData),
]
