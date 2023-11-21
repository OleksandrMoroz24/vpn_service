from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm


@login_required
def update_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("vpn:index")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "user/update_profile.html", {"form": form})
