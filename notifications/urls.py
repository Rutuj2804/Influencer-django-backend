from django.urls import path
from .views import CreateNotification, SeenByUser, GetSeenNotifications, GetUnSeenNotifications

urlpatterns = [
    path('create/', CreateNotification.as_view()),
    path('seen/', SeenByUser.as_view()),
    path('get/', GetSeenNotifications.as_view()),
    path('get-unseen/', GetUnSeenNotifications.as_view()),
]