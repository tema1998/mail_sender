from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('success', views.Index.as_view(), name='success'),
    path('send-email', views.SendEmail.as_view(), name='send-email'),
]
