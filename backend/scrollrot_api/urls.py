"""URL configuration for scrollrot_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from .views import HealthCheckView, APIRootView

v1_patterns = [
    path("", APIRootView.as_view(), name="api-root"),
    path("health/", HealthCheckView.as_view(), name="api-health"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    # Top-level health check alias
    path("health/", HealthCheckView.as_view(), name="top-health"),
    # Versioned API routes
    path("api/v1/", include((v1_patterns, "v1"))),
]
