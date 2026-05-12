import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 3: Deletion & Skipping ──
t3=Topic.objects.create(
    module=m2, title="Deletion and Skipping in Array", slug="deletion-skipping-array",
    order=3, is_published=True,
    introduction="Deletion removes elements by shifting remaining ones left, shrinking logical size. Skipping keeps trigger elements but removes K elements that follow each trigger. Both use the compaction pattern with read/write pointers.",
    content_html="""<h3>Deletion at a Position — Shift Left</h3>
<p>To delete element at position p: <strong>shift all elements after p one step to the left</strong> (overwriting position p), then decrease n by 1.</p>

<h3>Compaction Pattern — Two-Pointer Delete by Condition</h3>
<p><strong>Mental Model — Read head + Write head:</strong></p>
<ul>
<li><code>i</code> = read head (scans every element)</li>
<li><code>j</code> = write head (only advances when keeping an element)</li>
<li>Elements to keep get written to position j</li>
<li>Elements to delete get skipped</li>
<li>After the loop, j is the new size</li>
</ul>

<h3>Dry Run: arr = {12, 7, 18, 9}, delete evens → keep odds</h3>
<table><thead><tr><th>i</th><th>arr[i]</th><th>Keep? (odd)</th><th>j before</th><th>Action</th><th>j after</th></tr></thead>
<tbody>
<tr><td>0</td><td>12</td><td>NO (even)</td><td>0</td><td>skip</td><td>0</td></tr>
<tr><td>1</td><td>7</td><td>YES</td><td>0</td><td>arr[0]=7</td><td>1</td></tr>
<tr><td>2</td><td>18</td><td>NO (even)</td><td>1</td><td>skip</td><td>1</td></tr>
<tr><td>3</td><td>9</td><td>YES</td><td>1</td><td>arr[1]=9</td><td>2</td></tr>
</tbody></table>
<p><strong>Result: arr = {7, 9}, n = 2</strong></p>

<h3>⚠️ What "Delete" Means in C</h3>
<p>C arrays do not shrink in memory. After compaction, arr[n] through arr[old_n-1] still contain old values physically. But since n is smaller, your loops stop before reaching them. The data is <strong>logically deleted</strong>.</p>

<hr>

<h3>Skipping — Core Idea</h3>
<p>When you encounter a trigger element, set a skip counter to K. For the next K elements, skip them and decrement the counter. Normal elements pass through. <strong>The trigger element itself is kept.</strong></p>

<p><strong>Mental Model — A Red Light That Lasts K Steps:</strong> When the light turns red (trigger hit), the next K elements must wait (be skipped). After K elements, the light turns green and elements flow normally.</p>

<h3>Dry Run: arr = {5, 10, 15, 8, 20, 7}, skip 1 after mult of 5</h3>
<table><thead><tr><th>i</th><th>arr[i]</th><th>skip before</th><th>Action</th><th>skip after</th><th>Kept?</th></tr></thead>
<tbody>
<tr><td>0</td><td>5</td><td>0</td><td>Trigger! Keep 5, set skip=1</td><td>1</td><td>YES: 5</td></tr>
<tr><td>1</td><td>10</td><td>1</td><td>In skip zone, skip--</td><td>0</td><td>NO</td></tr>
<tr><td>2</td><td>15</td><td>0</td><td>Trigger! Keep 15, set skip=1</td><td>1</td><td>YES: 15</td></tr>
<tr><td>3</td><td>8</td><td>1</td><td>In skip zone, skip--</td><td>0</td><td>NO</td></tr>
<tr><td>4</td><td>20</td><td>0</td><td>Trigger! Keep 20, set skip=1</td><td>1</td><td>YES: 20</td></tr>
<tr><td>5</td><td>7</td><td>1</td><td>In skip zone, skip--</td><td>0</td><td>NO</td></tr>
</tbody></table>
<p><strong>Result: {5, 15, 20}</strong></p>""",
    code_examples="""// Delete at position pos (shift left)
for (int i = pos; i < n - 1; i++) {
    arr[i] = arr[i + 1];   // shift left
}
n--;

// Compaction: Delete all even numbers (keep odds)
int j = 0;                    // write head
for (int i = 0; i < n; i++) { // read head scans all
    if (arr[i] % 2 != 0) {    // KEEP condition: odd
        arr[j] = arr[i];
        j++;
    }
    // even: i advances, j stays — element skipped
}
n = j;   // new logical size

// Skip ONE element after every multiple of 5
int skip = 0;   // how many more to skip
int j = 0;      // write head
for (int i = 0; i < n; i++) {
    if (skip > 0) { skip--; continue; }  // in skip zone
    if (arr[i] % 5 == 0) skip = 1;       // trigger
    arr[j++] = arr[i];                    // keep element
}
n = j;""",
    logic_explanation="""DELETION at position:
1. Shift loop from i=pos to i=n-2.
2. At each step: arr[i] = arr[i+1] (shift left).
3. After loop: n-- (shrink size).
4. Last step reads arr[n-1], so loop goes to i = n-2.

COMPACTION (delete by condition):
1. j = 0 (write head).
2. Loop i from 0 to n-1 (read head).
3. If KEEP condition true: arr[j] = arr[i]; j++.
4. If DELETE condition true: do nothing (i advances, j stays).
5. After loop: n = j.
Key: KEEP condition = logical NOT of DELETE condition.

SKIPPING:
1. skip = 0, j = 0.
2. Loop i from 0 to n-1.
3. If skip > 0: skip--, continue (skip this element).
4. If trigger condition: set skip = K.
5. arr[j++] = arr[i] (keep this element, including trigger).
6. After loop: n = j.""",
    common_mistakes="""• Forgetting n-- after position deletion — loop visits old slots
• Wrong keep condition — accidentally deleting the wrong elements (keep = NOT delete)
• Setting n = j but printing with old n value
• Forgetting n = j after compaction — iterating over deleted elements
• Setting skip counter BEFORE keeping the trigger — trigger itself gets skipped
• Trigger element should be kept, not skipped (in most problems)""",
    beginner_notes="""💡 For deletion, think: "keep condition = opposite of delete condition".
💡 Compaction is just conditional traversal with a write head.
💡 After any deletion, ALWAYS update n = j.
💡 For skipping: the trigger element IS kept. The skip counter applies to elements AFTER the trigger.
💡 Draw the array on paper, mark triggers with T, cross out skipped elements, then trace your code."""
)

Concept.objects.create(topic=t3, title="Position Deletion (Shift Left)", order=1, language="c",
    explanation="Delete at specific index by shifting all subsequent elements one position left, then n--.",
    code_snippet='for (int i = pos; i < n - 1; i++)\n    arr[i] = arr[i + 1];\nn--;')
Concept.objects.create(topic=t3, title="Compaction Pattern", order=2, language="c",
    explanation="Two-pointer technique: i reads, j writes. Only elements passing the KEEP condition are written. After loop, n = j.",
    code_snippet='int j = 0;\nfor (int i = 0; i < n; i++)\n    if (keep_condition(arr[i]))\n        arr[j++] = arr[i];\nn = j;')
Concept.objects.create(topic=t3, title="Skip K After Trigger", order=3, language="c",
    explanation="When a trigger element is found, set skip counter to K. Next K elements are skipped. Trigger itself is kept.",
    code_snippet='int skip = 0, j = 0;\nfor (int i = 0; i < n; i++) {\n    if (skip > 0) { skip--; continue; }\n    if (arr[i] % 5 == 0) skip = 1;\n    arr[j++] = arr[i];\n}\nn = j;')

Problem.objects.create(topic=t3, title="Delete at Position", order=1,
    description="Delete the element at a given position and print the resulting array.",
    difficulty="easy", category="guided",
    solution_code='for (int i = pos; i < n - 1; i++)\n    arr[i] = arr[i + 1];\nn--;',
    solution_explanation="Shift left from pos to n-2. Decrement n.")
Problem.objects.create(topic=t3, title="Delete All Even Numbers", order=2,
    description="Remove all even numbers from the array using the compaction pattern.",
    difficulty="easy", category="practice",
    solution_code='int j = 0;\nfor (int i = 0; i < n; i++)\n    if (arr[i] % 2 != 0)  // keep odds\n        arr[j++] = arr[i];\nn = j;',
    solution_explanation="Keep condition = odd (NOT even). Write pointer j only advances for kept elements.")
Problem.objects.create(topic=t3, title="Delete All Multiples of 3", order=3,
    description="Remove all multiples of 3 from the array.",
    difficulty="easy", category="practice",
    solution_code='int j = 0;\nfor (int i = 0; i < n; i++)\n    if (arr[i] % 3 != 0)\n        arr[j++] = arr[i];\nn = j;',
    solution_explanation="Keep condition: arr[i] % 3 != 0 (NOT a multiple of 3).")
Problem.objects.create(topic=t3, title="Skip 2 After Every Odd Number", order=4,
    description="Keep all elements, but skip the next 2 elements after every odd number encountered. The odd number itself is kept.",
    difficulty="medium", category="challenge",
    hints="Set skip = 2 when trigger fires. Trigger: arr[i] % 2 != 0.",
    solution_code='int skip = 0, j = 0;\nfor (int i = 0; i < n; i++) {\n    if (skip > 0) { skip--; continue; }\n    if (arr[i] % 2 != 0) skip = 2;\n    arr[j++] = arr[i];\n}\nn = j;',
    solution_explanation="Same skip pattern but with K=2. The odd trigger is kept, next 2 elements are dropped.")
Problem.objects.create(topic=t3, title="Delete Lowest Element", order=5,
    description="Find the minimum element, then delete its first occurrence from the array.",
    difficulty="medium", category="practice",
    hints="Two steps: 1) Find min and its position. 2) Delete at that position using shift-left.",
    solution_code='// Step 1: find min position\nint minPos = 0;\nfor (int i = 1; i < n; i++)\n    if (arr[i] < arr[minPos]) minPos = i;\n// Step 2: delete at minPos\nfor (int i = minPos; i < n - 1; i++)\n    arr[i] = arr[i + 1];\nn--;',
    solution_explanation="First find the position of the minimum, then use position deletion. Two separate steps.")

print(f"✅ Topic 3 created.")
