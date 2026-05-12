import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learntolever.settings")
django.setup()

from core.models import Series, Module

# Create a default series for existing content if it doesn't exist
series, created = Series.objects.get_or_create(
    title="C Programming Foundation",
    defaults={
        "description": "Master the fundamentals of C programming, from basics to advanced array operations.",
        "icon": "🚀",
        "is_published": True,
        "order": 1
    }
)
if not created:
    series.is_published = True
    series.save()

# Assign all unassigned modules to this series
updated = Module.objects.filter(series__isnull=True).update(series=series)
print(f"Updated {updated} modules to belong to the new Series.")

# Also ensure modules are published
Module.objects.all().update(is_published=True)
print("Ensured all modules are published.")
