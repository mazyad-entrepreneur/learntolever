"""
Serializers for LearnToLever API (public read-only).

Nested serializers provide all data the frontend needs in minimal requests.
"""

from rest_framework import serializers
from .models import Series, Module, Topic, Concept, Problem, RevisionNote, ContentBlock


# ──────────────────────────────────────────────
# ContentBlock (public)
# ──────────────────────────────────────────────
class ContentBlockPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = ["id", "block_type", "content", "language", "meta_json", "order"]


# ──────────────────────────────────────────────
# Concept
# ──────────────────────────────────────────────
class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = ["id", "title", "explanation", "code_snippet", "language", "order"]


# ──────────────────────────────────────────────
# Problem
# ──────────────────────────────────────────────
class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            "id", "title", "description", "difficulty",
            "category", "hints", "solution_code",
            "solution_explanation", "is_assignment", "order",
        ]


# ──────────────────────────────────────────────
# Revision Note
# ──────────────────────────────────────────────
class RevisionNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevisionNote
        fields = ["id", "title", "summary", "key_points", "mindmap_data", "order"]


# ──────────────────────────────────────────────
# Topic — list (lightweight)
# ──────────────────────────────────────────────
class TopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "title", "slug", "order"]


# ──────────────────────────────────────────────
# Topic — detail (full content)
# ──────────────────────────────────────────────
class TopicDetailSerializer(serializers.ModelSerializer):
    concepts = ConceptSerializer(many=True, read_only=True)
    problems = ProblemSerializer(many=True, read_only=True)
    blocks = ContentBlockPublicSerializer(many=True, read_only=True)
    module_title = serializers.CharField(source="module.title", read_only=True)
    module_slug = serializers.CharField(source="module.slug", read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id", "title", "slug",
            "module_title", "module_slug",
            "introduction", "content_html", "code_examples",
            "logic_explanation", "common_mistakes",
            "beginner_notes", "visual_explanation",
            "blocks", "concepts", "problems",
            "order", "created_at", "updated_at",
        ]


# ──────────────────────────────────────────────
# Module — list (homepage)
# ──────────────────────────────────────────────
class ModuleListSerializer(serializers.ModelSerializer):
    topic_count = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ["id", "title", "slug", "description", "icon", "order", "topic_count"]

    def get_topic_count(self, obj):
        return obj.topics.filter(is_published=True).count()


# ──────────────────────────────────────────────
# Module — detail (with topics)
# ──────────────────────────────────────────────
class ModuleDetailSerializer(serializers.ModelSerializer):
    topics = TopicListSerializer(many=True, read_only=True)
    revision_notes = RevisionNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            "id", "title", "slug", "description", "icon",
            "topics", "revision_notes",
            "order", "created_at", "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Filter topics in memory — the queryset already fetched them
        published_slugs = set(
            instance.topics.filter(is_published=True).values_list("slug", flat=True)
        )
        data["topics"] = [t for t in data["topics"] if t["slug"] in published_slugs]
        return data


# ──────────────────────────────────────────────
# Series — list
# ──────────────────────────────────────────────
class SeriesListSerializer(serializers.ModelSerializer):
    module_count = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = ["id", "title", "slug", "description", "icon", "order", "module_count"]

    def get_module_count(self, obj):
        return obj.modules.filter(is_published=True).count()


# ──────────────────────────────────────────────
# Series — detail (with modules)
# ──────────────────────────────────────────────
class SeriesDetailSerializer(serializers.ModelSerializer):
    modules = ModuleListSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = [
            "id", "title", "slug", "description", "icon",
            "modules", "order", "created_at", "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Filter modules in memory — the queryset already fetched them
        published_slugs = set(
            instance.modules.filter(is_published=True).values_list("slug", flat=True)
        )
        data["modules"] = [m for m in data["modules"] if m["slug"] in published_slugs]
        return data
