from django.urls import path
from .views import CreateTimeSpend, AnalyticsTimeSpend

urlpatterns = [
    path('record/', CreateTimeSpend.as_view()),
    path('analytics/', AnalyticsTimeSpend.as_view()),
]
