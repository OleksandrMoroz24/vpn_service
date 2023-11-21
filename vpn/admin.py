from django.contrib import admin

from vpn.models import UserSite, UserActivity

admin.site.register(UserSite)
admin.site.register(UserActivity)
