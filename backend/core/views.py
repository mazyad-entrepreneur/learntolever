"""
API views for LearnToLever.

Public read-only views + current user endpoint.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Series, Module, Topic, Problem, RevisionNote, ContentBlock
import re
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


# ──────────────────────────────────────────────
# Search
# ──────────────────────────────────────────────
class SearchView(APIView):
    """GET /api/search/?q=query"""

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response([])

        results = []
        topics = Topic.objects.filter(is_published=True, blocks__content__icontains=query).distinct()

        for topic in topics:
            matching_block = topic.blocks.filter(content__icontains=query).first()
            if not matching_block:
                continue

            heading_block = topic.blocks.filter(
                block_type="heading", 
                order__lte=matching_block.order
            ).order_by('-order').first()

            section_id = ""
            if heading_block:
                section_id = re.sub(r'[^a-z0-9]+', '-', heading_block.content.lower()).strip('-')

            snippet = matching_block.content
            idx = snippet.lower().find(query.lower())
            start = max(0, idx - 40)
            end = min(len(snippet), idx + len(query) + 40)
            snippet_text = snippet[start:end]
            if start > 0: snippet_text = "..." + snippet_text
            if end < len(snippet): snippet_text += "..."

            results.append({
                "topic_title": topic.title,
                "topic_slug": topic.slug,
                "module_slug": topic.module.slug if topic.module else "",
                "section_id": section_id,
                "snippet": snippet_text,
            })

        return Response(results)
