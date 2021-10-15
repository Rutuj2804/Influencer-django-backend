from django.urls import path
from .views import GetMyApplicationAPIView, UpdateApplicationAPIView

urlpatterns = [
    path('get/', GetMyApplicationAPIView.as_view()),
    path('update/', UpdateApplicationAPIView.as_view()),
]