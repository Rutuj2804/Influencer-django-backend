from django.urls import path
from .views import CreateListing, UpdateListing, GetListings, GetListingsDetailView, FetchMyListings, ApplyToListing, HiredInProjectAPIView, ListingDetailViewAnalytics, ListingAnalytics, StaticticsAnalytics, TopPerformers, DeleteListing, FilterDataOfListing, GetRecentListings, GetHiredRatings, RateUserByOrganisation, FetchDisplayUsersListings

urlpatterns = [
    path('create/', CreateListing.as_view()),
    path('update/', UpdateListing.as_view()),
    path('get/', GetListings.as_view()),
    path('get-recent/', GetRecentListings.as_view()),
    path('delete/', DeleteListing.as_view()),
    path('filter/', FilterDataOfListing.as_view()),
    path('get-my/', FetchMyListings.as_view()),
    path('get-detail/', GetListingsDetailView.as_view()),
    path('apply/', ApplyToListing.as_view()),
    path('hired/', HiredInProjectAPIView.as_view()),
    path('get-ratings/', GetHiredRatings.as_view()),
    path('rate-user/', RateUserByOrganisation.as_view()),
    path('analytics-detail/', ListingDetailViewAnalytics.as_view()),
    path('analytics/', ListingAnalytics.as_view()),
    path('user-analytics/', StaticticsAnalytics.as_view()),
    path('top-performers/', TopPerformers.as_view()),
    path('get-listings-user/', FetchDisplayUsersListings.as_view()),
]