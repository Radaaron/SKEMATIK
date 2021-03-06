from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.Login, name='home'),
    url(r'^login/', views.Login, name='login'),
    url(r'^logout/', views.Logout, name='logout'),
    url(r'^home/', views.Home, name='site home'),
    url(r'^register/', views.Register, name='register'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
