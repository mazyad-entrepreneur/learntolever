"""
API views for LearnToLever.

Public read-only views + current user endpoint.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Series, Module, Topic, Problem, RevisionNote
from .serializers import (
    SeriesListSerializer,
    SeriesDetailSerializer,
    ModuleListSerializer,
    ModuleDetailSerializer,
    TopicDetailSerializer,
    ProblemSerializer,
    RevisionNoteSerializer,
)


# ──────────────────────────────────────────────
# Auth
# ──────────────────────────────────────────────
class CurrentUserView(APIView):
    """GET /api/auth/me/ — returns current authenticated user info."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "is_staff": request.user.is_staff,
        })


# ──────────────────────────────────────────────
# Series views
# ──────────────────────────────────────────────
class SeriesListView(generics.ListAPIView):
    """GET /api/series/ — all published series."""
    serializer_class = SeriesListSerializer

    def get_queryset(self):
        return Series.objects.filter(is_published=True)


class SeriesDetailView(generics.RetrieveAPIView):
    """GET /api/series/<slug>/ — series detail with modules."""
    serializer_class = SeriesDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Series.objects.filter(is_published=True)


# ──────────────────────────────────────────────
# Module views
# ──────────────────────────────────────────────
class ModuleListView(generics.ListAPIView):
    """GET /api/modules/ — all published modules."""
    serializer_class = ModuleListSerializer

    def get_queryset(self):
        return Module.objects.filter(is_published=True)


class ModuleDetailView(generics.RetrieveAPIView):
    """GET /api/modules/<slug>/ — module with topics."""
    serializer_class = ModuleDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Module.objects.filter(is_published=True)


# ──────────────────────────────────────────────
# Topic views
# ──────────────────────────────────────────────
class TopicDetailView(generics.RetrieveAPIView):
    """GET /api/topics/<slug>/ — full topic content."""
    serializer_class = TopicDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Topic.objects.filter(is_published=True)


# ──────────────────────────────────────────────
# Problem views
# ──────────────────────────────────────────────
class TopicProblemsView(generics.ListAPIView):
    """GET /api/topics/<slug>/problems/"""
    serializer_class = ProblemSerializer

    def get_queryset(self):
        return Problem.objects.filter(
            topic__slug=self.kwargs["slug"],
            topic__is_published=True,
        )


# ──────────────────────────────────────────────
# Revision views
# ──────────────────────────────────────────────
class ModuleRevisionView(generics.ListAPIView):
    """GET /api/modules/<slug>/revision/"""
    serializer_class = RevisionNoteSerializer

    def get_queryset(self):
        return RevisionNote.objects.filter(
            module__slug=self.kwargs["slug"],
            module__is_published=True,
        )
