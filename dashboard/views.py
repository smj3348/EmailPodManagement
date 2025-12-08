from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard_home(request):
    return render(request, "dashboard.html", {})

@login_required
def monitoring_page(request):
    return render(request, "monitoring.html", {})

@login_required
def pods_page(request):
    return render(request, "pods.html", {})

@login_required
def provisioning_page(request):
    return render(request, "provisioning.html", {})

@login_required
def jobs_page(request):
    return render(request, "jobs.html", {})

@login_required
def docs_page(request):
    return render(request, "docs.html", {})

@login_required
def settings_page(request):
    return render(request, "settings.html", {})
