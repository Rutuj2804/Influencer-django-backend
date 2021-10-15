from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest_auth_links/', obtain_auth_token),
    path('accounts/', include("accounts.urls")),
    path('listings/', include("listings.urls")),
    path('notifications/', include("notifications.urls")),
    path('chats/', include("chats.urls")),
    path('applications/', include("applications.urls")),
    path('useractivity/', include("useractivity.urls")),
    path('searches/', include("searches.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
