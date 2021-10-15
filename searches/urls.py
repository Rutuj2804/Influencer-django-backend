from django.urls import path
from .views import SetSearch

urlpatterns = [
    path('query/', SetSearch.as_view())
]