from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models

from .models import VpsServer, Pod


# ------------------- Dashboard -------------------

@login_required
def dashboard_home(request):
    return render(request, "dashboard.html", {})


# ------------------- Monitoring -------------------

@login_required
def monitoring_page(request):
    return render(request, "monitoring.html", {})


# ------------------- Devices (formerly "Pods" section) -------------------

@login_required
def devices_page(request):
    """
    Old 'Pods' overview page, now correctly labeled as Devices.
    """
    return render(request, "devices.html", {})


@login_required
def devices_vps_list(request):
    """
    Displays all VPS servers (Devices) with search + filtering.
    """
    qs = VpsServer.objects.select_related("pod").all()

    q = request.GET.get("q", "").strip()
    provider = request.GET.get("provider", "").strip()
    active = request.GET.get("active", "").strip()
    pod = request.GET.get("pod", "").strip()

    if q:
        qs = qs.filter(
            models.Q(code__icontains=q)
            | models.Q(friendly_name__icontains=q)
            | models.Q(main_ip__icontains=q)
            | models.Q(hostname__icontains=q)
            | models.Q(domain__icontains=q)
        )

    if provider:
        qs = qs.filter(provider=provider)

    if active == "true":
        qs = qs.filter(is_active=True)
    elif active == "false":
        qs = qs.filter(is_active=False)

    if pod:
        qs = qs.filter(pod__slug=pod)

    pods = Pod.objects.all()

    return render(
        request,
        "devices_vps_list.html",
        {
            "servers": qs,
            "q": q,
            "provider": provider,
            "active": active,
            "pod": pod,
            "pods": pods,
        },
    )


@login_required
def devices_vps_detail(request, slug):
    server = get_object_or_404(VpsServer.objects.select_related("pod"), slug=slug)
    return render(request, "devices_vps_detail.html", {"server": server})


# ------------------- Pods (NEW) -------------------

@login_required
def pods_page(request):
    """
    New Pods tab: list Pods and show counts.
    """
    qs = Pod.objects.all()

    q = request.GET.get("q", "").strip()
    provider = request.GET.get("provider", "").strip()

    if q:
        qs = qs.filter(
            models.Q(name__icontains=q)
            | models.Q(purpose__icontains=q)
            | models.Q(notes__icontains=q)
        )

    if provider:
        qs = qs.filter(provider__icontains=provider)

    # annotate device counts
    qs = qs.annotate(device_count=models.Count("devices"))

    return render(
        request,
        "pods.html",
        {
            "pods": qs,
            "q": q,
            "provider": provider,
        },
    )


@login_required
def pod_detail(request, slug):
    pod = get_object_or_404(Pod, slug=slug)
    devices = pod.devices.order_by("code")
    return render(request, "pods_detail.html", {"pod": pod, "devices": devices})


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
