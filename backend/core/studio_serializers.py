"""
Studio serializers — write-capable serializers for the Creator Studio.
"""

from rest_framework import serializers
from .models import Series, Module, Topic, ContentBlock, Problem


class SeriesSerializer(serializers.ModelSerializer):
    module_count = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = [
            "id", "title", "slug", "description", "icon",
            "order", "is_published", "module_count",
            "created_at", "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]

    def get_module_count(self, obj):
        return obj.modules.count()


class ModuleStudioSerializer(serializers.ModelSerializer):
    topic_count = serializers.SerializerMethodField()
    series_title = serializers.CharField(source="series.title", read_only=True, default="")

    class Meta:
        model = Module
        fields = [
            "id", "series", "series_title", "title", "slug",
            "description", "icon", "order", "is_published",
            "topic_count", "created_at", "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]

    def get_topic_count(self, obj):
        return obj.topics.count()


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = [
            "id", "topic", "block_type", "content",
            "language", "meta_json", "order",
        ]


class TopicStudioSerializer(serializers.ModelSerializer):
    blocks = ContentBlockSerializer(many=True, read_only=True)
    module_title = serializers.CharField(source="module.title", read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id", "module", "module_title", "title", "slug",
            "status", "order", "is_published",
            "introduction", "content_html", "code_examples",
            "logic_explanation", "common_mistakes",
            "beginner_notes", "visual_explanation",
            "blocks", "created_at", "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]


class ProblemStudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            "id", "topic", "title", "description", "difficulty",
            "category", "hints", "solution_code",
            "solution_explanation", "is_assignment", "order",
        ]
