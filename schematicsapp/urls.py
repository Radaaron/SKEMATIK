from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^upload_schematic/', views.upload_schematic),
    url(r'^edit_schematic/', views.edit_schematic),
    url(r'^delete_schematic/', views.delete_schematic),
    url(r'^add_schematic_tag/', views.add_schematic_tag),
    url(r'^delete_schematic_tag/', views.delete_schematic_tag),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
