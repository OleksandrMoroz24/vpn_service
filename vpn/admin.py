from django.contrib import admin

from vpn.models import UserSite, VpnUsageStatistics

admin.site.register(UserSite)
admin.site.register(VpnUsageStatistics)
