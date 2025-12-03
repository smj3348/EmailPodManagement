from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_home(request):
    # Placeholder for now – later we'll show servers, jobs, etc.
    return render(request, "dashboard.html", {})
