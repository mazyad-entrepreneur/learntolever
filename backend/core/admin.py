"""Django Admin configuration for LearnToLever."""

from django.contrib import admin
from .models import Series, Module, Topic, ContentBlock, Concept, Problem, RevisionNote


# ── Inlines ──
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ["title", "order", "is_published"]


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0
    fields = ["title", "order", "status", "is_published"]


class ContentBlockInline(admin.StackedInline):
    model = ContentBlock
    extra = 0
    fields = ["block_type", "content", "language", "meta_json", "order"]


class ConceptInline(admin.StackedInline):
    model = Concept
    extra = 0


class ProblemInline(admin.StackedInline):
    model = Problem
    extra = 0


class RevisionNoteInline(admin.StackedInline):
    model = RevisionNote
    extra = 0


# ── Model Admins ──
@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_published", "updated_at"]
    list_editable = ["order", "is_published"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ["title", "series", "order", "is_published", "updated_at"]
    list_editable = ["order", "is_published"]
    list_filter = ["series", "is_published"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TopicInline, RevisionNoteInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "module", "order", "status", "is_published"]
    list_editable = ["order", "status"]
    list_filter = ["module", "status", "is_published"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ContentBlockInline, ConceptInline, ProblemInline]
    fieldsets = (
        (None, {"fields": ("module", "title", "slug", "status", "order", "is_published")}),
        ("Legacy Content", {
            "classes": ("collapse",),
            "fields": (
                "introduction", "content_html", "code_examples",
                "logic_explanation", "common_mistakes",
                "beginner_notes", "visual_explanation",
            ),
        }),
    )


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ["__str__", "topic", "block_type", "order"]
    list_filter = ["block_type"]


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ["title", "topic", "difficulty", "category"]
    list_filter = ["difficulty", "category"]
