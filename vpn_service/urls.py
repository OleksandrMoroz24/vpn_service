from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("vpn.urls", namespace="vpn")),
    path("user/", include("user.urls", namespace="user")),
    path("accounts/", include("django.contrib.auth.urls")),
]
