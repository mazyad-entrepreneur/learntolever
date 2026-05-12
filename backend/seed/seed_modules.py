"""
Seed script — Creates the 4 foundation modules (without topics).
Run: python manage.py shell < seed/seed_modules.py
"""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learntolever.settings")
django.setup()

from core.models import Module, Topic, Concept, Problem, RevisionNote

# Clear everything
Module.objects.all().delete()

# Module 1
Module.objects.create(
    title="Basics of Programming, Loops, and Patterns in C",
    slug="basics-programming-loops-patterns-c",
    description="Learn the fundamental building blocks of programming in C — variables, data types, conditional statements, loops, iterative constructs, and pattern printing.",
    icon="🧱", order=1, is_published=True,
)

# Module 2
Module.objects.create(
    title="Array Processing, Traversal, and Logical Operations in C",
    slug="array-processing-traversal-logical-operations-c",
    description="Master 1D arrays in C — traversal, conditional replacement, insertion, deletion, skipping, reversing, sorting, frequency counting, unique/duplicate detection, and combined operations.",
    icon="📊", order=2, is_published=True,
)

# Module 3
Module.objects.create(
    title="OOPs by Java",
    slug="oops-by-java",
    description="Understand Object-Oriented Programming through Java — classes, objects, inheritance, polymorphism, abstraction, and encapsulation.",
    icon="☕", order=3, is_published=True,
)

# Module 4
Module.objects.create(
    title="Practice More on Foundations",
    slug="practice-more-foundations",
    description="Reinforce your understanding of C basics, arrays, and Java OOPs with additional practice problems, exam simulations, and revision exercises.",
    icon="💪", order=4, is_published=True,
)

print(f"✅ Created {Module.objects.count()} modules.")
