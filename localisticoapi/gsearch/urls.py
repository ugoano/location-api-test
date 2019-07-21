from django.urls import path

from . import views


urlpatterns = [
    path('', views.sync_index, name='sync_index'),
    path('async/', views.async_index, name='async_index'),
]
