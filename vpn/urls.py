from django.urls import path
from .views import custom_proxy_view, CreateSiteView, SiteListView, SiteUpdateView, SiteDeleteView, index

urlpatterns = [
    path("", index, name="index"),
    path('<str:user_site_name>/<path:user_site>', custom_proxy_view, name='proxy'),

    path('create-site/', CreateSiteView.as_view(), name='create_site'),
    path('sites/', SiteListView.as_view(), name='site_list'),
    path('sites/<int:pk>/edit/', SiteUpdateView.as_view(), name='edit_site'),
    path('sites/<int:pk>/delete/', SiteDeleteView.as_view(), name='delete_site'),
]

app_name = "vpn"
