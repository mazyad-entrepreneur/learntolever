"""
Studio API views — authenticated CRUD for content creation.

All views require JWT authentication (staff users only).
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Series, Module, Topic, ContentBlock, Problem
from .studio_serializers import (
    SeriesSerializer, ModuleStudioSerializer,
    TopicStudioSerializer, ContentBlockSerializer,
    ProblemStudioSerializer,
)


class IsStaffUser(permissions.BasePermission):
    """Only allow staff/admin users."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


# ──────────────────────────────────────────────
# Series CRUD
# ──────────────────────────────────────────────
class SeriesViewSet(viewsets.ModelViewSet):
    """Full CRUD for learning series."""
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsStaffUser]
    lookup_field = "id"

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        """Bulk reorder series. Expects: {"items": [{"id": 1, "order": 0}, ...]}"""
        for item in request.data.get("items", []):
            Series.objects.filter(id=item["id"]).update(order=item["order"])
        return Response({"status": "ok"})


# ──────────────────────────────────────────────
# Module CRUD
# ──────────────────────────────────────────────
class ModuleViewSet(viewsets.ModelViewSet):
    """Full CRUD for modules within a series."""
    serializer_class = ModuleStudioSerializer
    permission_classes = [IsStaffUser]
    lookup_field = "id"

    def get_queryset(self):
        qs = Module.objects.all()
        series_id = self.request.query_params.get("series")
        if series_id:
            qs = qs.filter(series_id=series_id)
        return qs

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        for item in request.data.get("items", []):
            Module.objects.filter(id=item["id"]).update(order=item["order"])
        return Response({"status": "ok"})


# ──────────────────────────────────────────────
# Topic CRUD
# ──────────────────────────────────────────────
class TopicViewSet(viewsets.ModelViewSet):
    """Full CRUD for topics within a module."""
    serializer_class = TopicStudioSerializer
    permission_classes = [IsStaffUser]
    lookup_field = "id"

    def get_queryset(self):
        qs = Topic.objects.all()
        module_id = self.request.query_params.get("module")
        if module_id:
            qs = qs.filter(module_id=module_id)
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        for item in request.data.get("items", []):
            Topic.objects.filter(id=item["id"]).update(order=item["order"])
        return Response({"status": "ok"})

    @action(detail=True, methods=["post"])
    def publish(self, request, id=None):
        topic = self.get_object()
        topic.status = "published"
        topic.is_published = True
        topic.save()
        return Response({"status": "published"})

    @action(detail=True, methods=["post"])
    def unpublish(self, request, id=None):
        topic = self.get_object()
        topic.status = "draft"
        topic.is_published = False
        topic.save()
        return Response({"status": "draft"})


# ──────────────────────────────────────────────
# ContentBlock CRUD
# ──────────────────────────────────────────────
class ContentBlockViewSet(viewsets.ModelViewSet):
    """Full CRUD for content blocks within a topic."""
    serializer_class = ContentBlockSerializer
    permission_classes = [IsStaffUser]
    lookup_field = "id"

    def get_queryset(self):
        qs = ContentBlock.objects.all()
        topic_id = self.request.query_params.get("topic")
        if topic_id:
            qs = qs.filter(topic_id=topic_id)
        return qs

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        for item in request.data.get("items", []):
            ContentBlock.objects.filter(id=item["id"]).update(order=item["order"])
        return Response({"status": "ok"})

    @action(detail=False, methods=["post"])
    def bulk_save(self, request):
        """Save all blocks for a topic at once. Expects: {"topic": id, "blocks": [...]}"""
        topic_id = request.data.get("topic")
        blocks_data = request.data.get("blocks", [])

        if not topic_id:
            return Response({"error": "topic required"}, status=400)

        # Delete existing blocks and recreate
        ContentBlock.objects.filter(topic_id=topic_id).delete()
        for i, block in enumerate(blocks_data):
            ContentBlock.objects.create(
                topic_id=topic_id,
                block_type=block.get("block_type", "paragraph"),
                content=block.get("content", ""),
                language=block.get("language", ""),
                meta_json=block.get("meta_json", {}),
                order=i,
            )
        return Response({"status": "ok", "count": len(blocks_data)})


# ──────────────────────────────────────────────
# Problem CRUD
# ──────────────────────────────────────────────
class ProblemViewSet(viewsets.ModelViewSet):
    """Full CRUD for problems within a topic."""
    serializer_class = ProblemStudioSerializer
    permission_classes = [IsStaffUser]
    lookup_field = "id"

    def get_queryset(self):
        qs = Problem.objects.all()
        topic_id = self.request.query_params.get("topic")
        if topic_id:
            qs = qs.filter(topic_id=topic_id)
        return qs
