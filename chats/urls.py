from django.urls import path
from .views import CreateChatRoom, AddMessages, GetChatRooms, GetMessages, SeenMessages

urlpatterns = [
    path('create/', CreateChatRoom.as_view()),
    path('add/', AddMessages.as_view()),
    path('get/', GetChatRooms.as_view()),
    path('seen/', SeenMessages.as_view()),
    path('get-messages/', GetMessages.as_view()),
]