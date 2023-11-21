import requests

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from .models import UserSite, VpnUsageStatistics
from .forms import UserSiteForm


@login_required
def index(request):
    """View function for the home page of the site."""

    # Counting the number of sites
    user_stats = VpnUsageStatistics.objects.filter(user=request.user)

    return render(request, "vpn/index.html", {"user_stats": user_stats})


class CustomProxyView(View):
    def modify_links(self, soup, proxy_base_url, external_url):
        # Modify all links (href)
        for link in soup.find_all("a", href=True):
            original_href = link["href"]
            full_url = urljoin(external_url, original_href)
            proxy_url = f"{proxy_base_url}{full_url}"
            link["href"] = proxy_url

        # Modify form actions (action)
        for form in soup.find_all("form", action=True):
            original_action = form["action"]
            full_url = urljoin(external_url, original_action)
            proxy_url = f"{proxy_base_url}{full_url}"
            form["action"] = proxy_url

    def get(self, request, user_site_name, user_site):
        proxy_base_url = f"/proxy/{user_site_name}/"
        parsed_url = urlparse(user_site)
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc
        path = parsed_url.path

        if not netloc:
            return HttpResponse("Invalid URL", status=400)

        external_url = f"{scheme}://{netloc}{path}"

        try:
            response = requests.get(external_url)
            response.raise_for_status()

            # Update statistics
            self.update_statistics(request.user, external_url, response)

            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            self.modify_links(soup, proxy_base_url, external_url)

            return HttpResponse(soup.prettify(), content_type="text/html")

        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Error fetching the page: {e}", status=500)

    def update_statistics(self, user, url, response):
        stats, created = VpnUsageStatistics.objects.get_or_create(
            user=user, site_url=url
        )

        stats.page_transitions += 1

        # Check if request body is not None before calculating its length
        if response.request.body:
            stats.data_sent += len(response.request.body)

        # Check if response content is not None before calculating its length
        if response.content:
            stats.data_received += len(response.content)

        stats.save()


class CreateSiteView(LoginRequiredMixin, CreateView):
    model = UserSite
    form_class = UserSiteForm
    template_name = "vpn/site_form.html"
    success_url = reverse_lazy("vpn:site_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SiteListView(LoginRequiredMixin, ListView):
    model = UserSite
    template_name = "vpn/site_list.html"
    context_object_name = "sites"
    paginate_by = 10

    def get_queryset(self):
        return UserSite.objects.filter(user=self.request.user)


class SiteUpdateView(LoginRequiredMixin, UpdateView):
    model = UserSite
    fields = ["name", "url"]
    template_name = "vpn/edit_site.html"
    success_url = reverse_lazy("vpn:site_list")

    def get_queryset(self):
        return UserSite.objects.filter(user=self.request.user)


class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = UserSite
    template_name = "vpn/delete_site.html"
    success_url = reverse_lazy("vpn:site_list")

    def get_queryset(self):
        return UserSite.objects.filter(user=self.request.user)
