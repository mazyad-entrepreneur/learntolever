"""
Master seed script for Module 2: Array Processing, Traversal, and Logical Operations in C.

This script clears all existing Module 2 topics/concepts/problems/revision notes
and re-seeds them with the comprehensive handbook content.

Run: cd /home/mazyad/learntolever/backend && python seed/seed_m2_all.py
"""
import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem,RevisionNote

# Get Module 2
m2 = Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# Clear all existing Module 2 content
print("🗑️  Clearing existing Module 2 content...")
old_topics = Topic.objects.filter(module=m2).count()
old_concepts = Concept.objects.filter(topic__module=m2).count()
old_problems = Problem.objects.filter(topic__module=m2).count()
old_revisions = RevisionNote.objects.filter(module=m2).count()
print(f"   Removing: {old_topics} topics, {old_concepts} concepts, {old_problems} problems, {old_revisions} revision notes")

RevisionNote.objects.filter(module=m2).delete()
Topic.objects.filter(module=m2).delete()  # cascades to concepts and problems

print("✅ Cleared. Now seeding new content...\n")

# Run each topic seed
seed_dir = os.path.dirname(os.path.abspath(__file__))
for i in range(1, 7):
    seed_file = os.path.join(seed_dir, f"seed_m2_t{i}.py")
    print(f"📥 Running seed_m2_t{i}.py...")
    exec(open(seed_file).read())
    print()

# Final summary
print("=" * 50)
print(f"🎉 Module 2 seeding complete!")
print(f"   Topics: {Topic.objects.filter(module=m2).count()}")
print(f"   Concepts: {Concept.objects.filter(topic__module=m2).count()}")
print(f"   Problems: {Problem.objects.filter(topic__module=m2).count()}")
print(f"   Revision Notes: {RevisionNote.objects.filter(module=m2).count()}")
print("=" * 50)
