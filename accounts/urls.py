from django.urls import path
from .views import RegisterUser, EditUserApiView, GetUserApiView, EditUserPhoto, StatusChangeOfUser, CheckAuthentication, TopPerformers, GetDisplayUserApiView

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('edit/', EditUserApiView.as_view()),
    path('edit-photo/', EditUserPhoto.as_view()),
    path('check_authentication/', CheckAuthentication.as_view()),
    path('get/', GetUserApiView.as_view()),
    path('get-user/', GetDisplayUserApiView.as_view()),
    path('status/', StatusChangeOfUser.as_view()),
    path('top/', TopPerformers.as_view()),
]
