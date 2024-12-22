from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_notifications, name='get_notifications'),
    path('<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
]