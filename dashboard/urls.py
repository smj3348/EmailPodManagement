from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # Dashboard
    path("", views.dashboard_home, name="dashboard"),

    # Monitoring
    path("monitoring/", views.monitoring_page, name="monitoring"),

    # Devices (RENAMED from old "Pods" section)
    path("devices/", views.devices_page, name="devices"),
    path("devices/vps/", views.devices_vps_list, name="devices_vps_list"),
    path("devices/vps/<slug:slug>/", views.devices_vps_detail, name="devices_vps_detail"),

    # Pods (NEW tab)
    path("pods/", views.pods_page, name="pods"),
    path("pods/<slug:slug>/", views.pod_detail, name="pod_detail"),

    # Legacy routes (keep old URLs working)
    path("pods/vps/", lambda r: redirect("devices_vps_list"), name="pods_vps_list"),
    path("pods/vps/<slug:slug>/", lambda r, slug: redirect("devices_vps_detail", slug=slug), name="pods_vps_detail"),
    path("pods-old/", views.devices_page),

    # Provisioning
    path("provisioning/", views.provisioning_page, name="provisioning"),

    # Jobs
    path("jobs/", views.jobs_page, name="jobs"),

    # Documentation
    path("docs/", views.docs_page, name="docs"),

    # Settings
    path("settings/", views.settings_page, name="settings"),
]
