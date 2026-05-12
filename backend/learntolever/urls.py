"""
URL configuration for LearnToLever.

Routes:
    /admin/    → Django Admin CMS
    /api/      → REST API for frontend
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]
