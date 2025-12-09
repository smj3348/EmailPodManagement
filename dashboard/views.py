from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import VpsServer


# ------------------- Dashboard -------------------

@login_required
def dashboard_home(request):
    return render(request, "dashboard.html", {})


# ------------------- Monitoring -------------------

@login_required
def monitoring_page(request):
    return render(request, "monitoring.html", {})


# ------------------- Pods Overview -------------------

@login_required
def pods_page(request):
    """
    Pods overview: links to VPS servers, Main Engine servers, and full pods.
    """
    return render(request, "pods.html", {})


# ------------------- VPS List Page -------------------

@login_required
def vps_list(request):
    """
    Displays all VPS servers with search + filtering.
    """
    qs = VpsServer.objects.all()

    # Filters
    q = request.GET.get("q", "").strip()
    provider = request.GET.get("provider", "").strip()
    active = request.GET.get("active", "").strip()

    # Search
    if q:
        qs = qs.filter(
            models.Q(code__icontains=q)
            | models.Q(friendly_name__icontains=q)
            | models.Q(main_ip__icontains=q)
            | models.Q(hostname__icontains=q)
            | models.Q(domain__icontains=q)
        )

    # Provider filter
    if provider:
        qs = qs.filter(provider__iexact=provider)

    # Active filter
    if active == "true":
        qs = qs.filter(is_active=True)
    elif active == "false":
        qs = qs.filter(is_active=False)

    context = {
        "servers": qs,
        "q": q,
        "provider": provider,
        "active": active,
    }
    return render(request, "pods_vps_list.html", context)


# ------------------- VPS Detail Page -------------------

@login_required
def vps_detail(request, slug):
    server = get_object_or_404(VpsServer, slug=slug)
    return render(request, "pods_vps_detail.html", {"server": server})


# ------------------- Provisioning -------------------

@login_required
def provisioning_page(request):
    return render(request, "provisioning.html", {})


# ------------------- Jobs -------------------

@login_required
def jobs_page(request):
    return render(request, "jobs.html", {})


# ------------------- Documentation -------------------

@login_required
def docs_page(request):
    return render(request, "docs.html", {})


# ------------------- Settings -------------------

@login_required
def settings_page(request):
    return render(request, "settings.html", {})
