from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard"),

    path("monitoring/", views.monitoring_page, name="monitoring"),
    path("pods/", views.pods_page, name="pods"),
    path("provisioning/", views.provisioning_page, name="provisioning"),
    path("jobs/", views.jobs_page, name="jobs"),
    path("docs/", views.docs_page, name="docs"),
    path("settings/", views.settings_page, name="settings"),
]

