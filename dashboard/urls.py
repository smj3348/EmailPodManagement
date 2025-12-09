from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("", views.dashboard_home, name="dashboard"),

    # Monitoring
    path("monitoring/", views.monitoring_page, name="monitoring"),

    # Pods overview page
    path("pods/", views.pods_page, name="pods"),

    # VPS sub-pages (under Pods)
    path("pods/vps/", views.vps_list, name="pods_vps_list"),
    path("pods/vps/<slug:slug>/", views.vps_detail, name="pods_vps_detail"),

    # Provisioning
    path("provisioning/", views.provisioning_page, name="provisioning"),

    # Jobs
    path("jobs/", views.jobs_page, name="jobs"),

    # Documentation
    path("docs/", views.docs_page, name="docs"),

    # Settings
    path("settings/", views.settings_page, name="settings"),
]
