
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .forms import UserSiteForm
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserSite



@login_required
def index(request):
    """View function for the home page of the site."""

    # Counting the number of sites
    num_sites = UserSite.objects.count()

    context = {
        "num_sites": num_sites,
    }

    return render(request, "vpn/index.html", context=context)


def custom_proxy_view(request, user_site_name, user_site):
    # Construct the base URL dynamically from the request
    scheme = request.scheme
    host = request.get_host()
    proxy_base_url = f'{scheme}://{host}/{user_site_name}/'

    # Parse the user_site URL
    parsed_url = urlparse(user_site)
    scheme = parsed_url.scheme  # 'http' or 'https'
    netloc = parsed_url.netloc  # domain name
    path = parsed_url.path      # URL path

    if not netloc:
        return HttpResponse("Invalid URL", status=400)

    external_url = f'{scheme}://{netloc}{path}'

    try:
        response = requests.get(external_url)
        content = response.content

        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a', href=True):
            original_href = link['href']
            # Convert to absolute URL and prepend the dynamic proxy base URL
            full_url = urljoin(external_url, original_href)
            link['href'] = f'{proxy_base_url}{full_url}'

        return HttpResponse(soup.prettify(), content_type='text/html')
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error fetching the page: {e}", status=500)


class CreateSiteView(LoginRequiredMixin, CreateView):
    model = UserSite
    form_class = UserSiteForm
    template_name = 'vpn/site_form.html'
    success_url = reverse_lazy('vpn:site_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SiteListView(LoginRequiredMixin, ListView):
    model = UserSite
    template_name = 'vpn/site_list.html'
    context_object_name = 'sites'
    paginate_by = 10

    def get_queryset(self):
        return UserSite.objects.filter(user=self.request.user)


class SiteUpdateView(LoginRequiredMixin, UpdateView):
    model = UserSite
    fields = ['name', 'url']
    template_name = 'vpn/edit_site.html'
    success_url = reverse_lazy('vpn:site_list')

    def get_queryset(self):
        return UserSite.objects.filter(user=self.request.user)


class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = UserSite
    template_name = 'vpn/delete_site.html'
    success_url = reverse_lazy('vpn:site_list')

    def get_queryset(self):
        return UserSite.objects.filter(user=self.request.user)