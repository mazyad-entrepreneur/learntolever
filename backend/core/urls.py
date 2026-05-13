"""
URL patterns for the core API.

All routes are prefixed with /api/ (set in learntolever/urls.py).
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)
from . import views
from . import studio_views

app_name = "core"

# ── Studio CRUD router ──
studio_router = DefaultRouter()
studio_router.register(r"series", studio_views.SeriesViewSet, basename="studio-series")
studio_router.register(r"modules", studio_views.ModuleViewSet, basename="studio-module")
studio_router.register(r"topics", studio_views.TopicViewSet, basename="studio-topic")
studio_router.register(r"blocks", studio_views.ContentBlockViewSet, basename="studio-block")
studio_router.register(r"problems", studio_views.ProblemViewSet, basename="studio-problem")

urlpatterns = [
    # ── Auth ──
    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/me/", views.CurrentUserView.as_view(), name="current-user"),

    # ── Studio CRUD (authenticated) ──
    path("studio/", include(studio_router.urls)),

    # ── Public read-only API ──
    path("series/", views.SeriesListView.as_view(), name="series-list"),
    path("series/<slug:slug>/", views.SeriesDetailView.as_view(), name="series-detail"),
    path("modules/", views.ModuleListView.as_view(), name="module-list"),
    path("modules/<slug:slug>/", views.ModuleDetailView.as_view(), name="module-detail"),
    path("modules/<slug:slug>/revision/", views.ModuleRevisionView.as_view(), name="module-revision"),
    path("topics/<slug:slug>/", views.TopicDetailView.as_view(), name="topic-detail"),
    path("topics/<slug:slug>/problems/", views.TopicProblemsView.as_view(), name="topic-problems"),
    path("search/", views.SearchView.as_view(), name="search"),
]
