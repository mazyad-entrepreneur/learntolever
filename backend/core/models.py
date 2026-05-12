"""
Core models for LearnToLever.

Database schema:
    Series → Module → Topic → ContentBlock
    Topic  → Concept
    Topic  → Problem
    Module → RevisionNote
"""

from django.db import models
from slugify import slugify


# ──────────────────────────────────────────────
# Series — top-level learning program
# ──────────────────────────────────────────────
class Series(models.Model):
    """
    A learning series (e.g. "Foundation Logic", "Learn React").
    Contains multiple modules.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(
        blank=True,
        help_text="Brief description shown on the homepage card.",
    )
    icon = models.CharField(
        max_length=50, default="📘",
        help_text="Emoji or icon class.",
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name_plural = "series"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# ──────────────────────────────────────────────
# Module — grouping within a series
# ──────────────────────────────────────────────
class Module(models.Model):
    """
    A learning module (e.g. "Basics of Programming", "Arrays").
    Belongs to a series, contains topics and revision notes.
    """

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name="modules",
        null=True, blank=True,
        help_text="Parent series. Null for legacy modules.",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(
        help_text="Brief description shown on the homepage card."
    )
    icon = models.CharField(
        max_length=50, default="📘",
        help_text="Emoji or icon class for the module card.",
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# ──────────────────────────────────────────────
# Topic — individual lesson within a module
# ──────────────────────────────────────────────
class Topic(models.Model):
    """
    A topic/lesson within a module.
    Content lives in ContentBlock children (or legacy fixed fields).
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("review", "In Review"),
        ("published", "Published"),
    ]

    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="topics",
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)

    # ── Legacy content fields (kept for backward compatibility) ──
    introduction = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    code_examples = models.TextField(blank=True)
    logic_explanation = models.TextField(blank=True)
    common_mistakes = models.TextField(blank=True)
    beginner_notes = models.TextField(blank=True)
    visual_explanation = models.TextField(blank=True)

    # ── Publishing workflow ──
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft",
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return f"{self.module.title} → {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Sync status with is_published
        if self.status == "published":
            self.is_published = True
        super().save(*args, **kwargs)


# ──────────────────────────────────────────────
# ContentBlock — structured content within a topic
# ──────────────────────────────────────────────
class ContentBlock(models.Model):
    """
    A single content block within a topic.
    Topics are composed of ordered blocks (like Notion).
    """

    BLOCK_TYPES = [
        ("heading", "Heading"),
        ("paragraph", "Paragraph"),
        ("code", "Code"),
        ("callout", "Callout"),
        ("assignment", "Assignment"),
        ("revision", "Revision"),
        ("divider", "Divider"),
    ]

    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="blocks",
    )
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    content = models.TextField(
        blank=True,
        help_text="Block content — text, markdown, or code.",
    )
    language = models.CharField(
        max_length=30, blank=True, default="",
        help_text="Language for code blocks (e.g. 'c', 'python').",
    )
    meta_json = models.JSONField(
        default=dict, blank=True,
        help_text="Extra metadata: {level, style, difficulty, hints, keyPoints}",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        preview = self.content[:40] if self.content else "(empty)"
        return f"[{self.block_type}] {preview}"


# ──────────────────────────────────────────────
# Concept — reusable building-block within a topic
# ──────────────────────────────────────────────
class Concept(models.Model):
    """A focused concept card within a topic."""

    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="concepts",
    )
    title = models.CharField(max_length=300)
    explanation = models.TextField()
    code_snippet = models.TextField(blank=True)
    language = models.CharField(max_length=30, default="python")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
# Problem — practice questions
# ──────────────────────────────────────────────
class Problem(models.Model):
    """A practice problem attached to a topic."""

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard"),
    ]
    CATEGORY_CHOICES = [
        ("guided", "Guided Problem"),
        ("practice", "Practice"),
        ("challenge", "Challenge"),
    ]

    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="problems",
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="easy")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="guided")
    hints = models.TextField(blank=True)
    solution_code = models.TextField(blank=True)
    solution_explanation = models.TextField(blank=True)
    is_assignment = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "difficulty"]

    def __str__(self):
        return f"[{self.difficulty}] {self.title}"


# ──────────────────────────────────────────────
# RevisionNote — quick-reference for a module
# ──────────────────────────────────────────────
class RevisionNote(models.Model):
    """Quick revision content for a module."""

    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="revision_notes",
    )
    title = models.CharField(max_length=300)
    summary = models.TextField()
    key_points = models.TextField(blank=True)
    mindmap_data = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Revision: {self.title}"
