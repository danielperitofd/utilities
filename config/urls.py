"""
URL configuration for BmpConverter project.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from converter import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download-image/<int:image_id>/', views.download_image, name='download_image'),
    path('download-selected/', views.download_selected, name='download_selected'),
    path('download-all/', views.download_all, name='download_all'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('clear-images/', views.clear_images, name='clear_images'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
