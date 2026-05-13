import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 3: Deletion & Skipping ──
# Covers handbook sections 5 (Deletion) + 6 (Skipping)
t3=Topic.objects.create(
    module=m2, title="Deletion and Skipping in Array", slug="deletion-skipping-array",
    order=3, is_published=True,
    introduction="Deletion removes elements by shifting remaining ones left, shrinking logical size. Skipping keeps trigger elements but removes K elements that follow each trigger. Both use the compaction pattern with read/write pointers.",
    content_html="""<h3>Deletion at a Position — Shift Left</h3>
<p>To delete element at position p: shift all elements <strong>after p one step to the left</strong> (overwriting position p), then decrease n by 1. The element is logically gone — the physical memory is still there but n says "don't look at it."</p>

<hr>
<h3>Deleting ALL Elements Matching a Condition: The Compaction Technique</h3>

<h4>Mental Model: Two-Pointer Compaction (Write Head + Read Head)</h4>
<p>You use two indices:</p>
<ul>
<li><code>i</code> (read head — scans every element)</li>
<li><code>j</code> (write head — only advances when keeping an element)</li>
<li>Elements that should be kept get written to position j</li>
<li>Elements to delete get skipped — i advances, j stays</li>
<li>At the end, j is the new size</li>
</ul>

<h3>Dry Run: arr = {12, 7, 18, 9}, delete evens → keep odds</h3>
<table><thead><tr><th>i</th><th>arr[i]</th><th>keep? (odd)</th><th>j before</th><th>action</th><th>j after</th></tr></thead>
<tbody>
<tr><td>0</td><td>12</td><td>✗ even — skip</td><td>0</td><td>skip</td><td>0</td></tr>
<tr><td>1</td><td>7</td><td>✓ odd — keep</td><td>0</td><td>arr[0]=7</td><td>1</td></tr>
<tr><td>2</td><td>18</td><td>✗ even — skip</td><td>1</td><td>skip</td><td>1</td></tr>
<tr><td>3</td><td>9</td><td>✓ odd — keep</td><td>1</td><td>arr[1]=9</td><td>2</td></tr>
<tr><td colspan="5"><strong>Result: arr = {7, 9}, n = 2</strong></td><td><strong>2</strong></td></tr>
</tbody></table>

<h3>⚠️ Critical Insight: What "Delete" Means in C</h3>
<p>C arrays don't shrink in memory. After deletion using compaction, arr[n] through arr[original_n-1] still contain old values in memory. But since n is now smaller, your loops stop before reaching them. The data is <strong>logically deleted</strong> even if physically still there. Never access beyond index n-1.</p>

<hr>
<h3>Skipping Elements — Core Idea</h3>
<p>Skipping is like deletion but with a <strong>stateful trigger</strong>. When you encounter a "trigger" element (e.g., a multiple of 5), you mark a skip counter. For the next k elements, you skip them (don't output/keep them) and decrement the counter. Normal elements reset to no-skip state.</p>

<h4>Mental Model: A Red Light That Lasts K Steps</h4>
<p>Imagine a traffic light at certain positions (the triggers). When the light turns red, the next k cars (elements) must wait (be skipped). After k cars pass through the red light, it turns green again and cars flow normally.</p>

<h3>Dry Run: arr = {5, 10, 15, 8, 20, 7}, skip 1 after mult of 5</h3>
<table><thead><tr><th>i</th><th>arr[i]</th><th>skip before</th><th>action</th><th>skip after</th><th>kept?</th></tr></thead>
<tbody>
<tr><td>0</td><td>5</td><td>0</td><td>trigger! keep 5, set skip=1</td><td>1</td><td>✓ 5</td></tr>
<tr><td>1</td><td>10</td><td>1</td><td>in skip zone, skip--</td><td>0</td><td>✗</td></tr>
<tr><td>2</td><td>15</td><td>0</td><td>trigger! keep 15, set skip=1</td><td>1</td><td>✓ 15</td></tr>
<tr><td>3</td><td>8</td><td>1</td><td>in skip zone, skip--</td><td>0</td><td>✗</td></tr>
<tr><td>4</td><td>20</td><td>0</td><td>trigger! keep 20, set skip=1</td><td>1</td><td>✓ 20</td></tr>
<tr><td>5</td><td>7</td><td>1</td><td>in skip zone, skip--</td><td>0</td><td>✗</td></tr>
</tbody></table>
<p><strong>Result: {5, 15, 20}</strong></p>

<h3>⚠️ Important: The Trigger Element Itself is Kept</h3>
<p>The element that activates the skip is <strong>printed/kept normally</strong>. Only the elements <em>after</em> it are skipped. Make sure your skip counter is set AFTER processing (keeping) the trigger element, not before.</p>

<hr>
<h3>🔴 Think Before Coding — Assignments</h3>
<ul>
<li><strong>3.1 (delete at position):</strong> Write out the shift-left loop. It starts at i=pos and goes to i=n-2 (not n-1!). Why? Because at each step you read arr[i+1], so the last step is i=n-2 (reads arr[n-1]).</li>
<li><strong>3.2–3.6 (delete by condition):</strong> All use the compaction pattern. Identify the "keep" condition (the opposite of the delete condition). Write j=0, loop i from 0 to n-1, if keep: arr[j]=arr[i], j++. After loop: n=j.</li>
<li><strong>3.7, 3.8 (delete after trigger):</strong> Different from plain deletion. What flag or counter tells you "skip this element because a trigger was seen recently"?</li>
<li><strong>3.9 (skip 2 after every ODD):</strong> Trigger condition = arr[i]%2!=0. Set skip to 2 when triggered.</li>
<li><strong>3.10 (delete lowest element):</strong> Two-step problem — find the minimum FIRST (what traversal?), then delete at its position.</li>
<li><strong>For any skip problem:</strong> What is the trigger? How many to skip? Is trigger kept or skipped? Draw the array, mark triggers with T, cross out skipped elements, THEN code.</li>
</ul>""",
    code_examples="""// Delete element at position pos (shift left)
for (int i = pos; i < n - 1; i++) {
    arr[i] = arr[i + 1];   // shift left: overwrite with next
}
n--;                         // shrink logical size

// Compaction: Delete all even numbers — keep odds
int j = 0;  // write head
for (int i = 0; i < n; i++) {  // read head scans all
    if (arr[i] % 2 != 0) {  // keep odd numbers
        arr[j] = arr[i];
        j++;
    }
    // even numbers: i advances, j stays — element is skipped
}
n = j;  // new size = number of elements kept

// Skip ONE element after every multiple of 5
int skip = 0;          // skip counter: how many more to skip
int j = 0;             // write head (if building output array)

for (int i = 0; i < n; i++) {
    if (skip > 0) {       // currently in skip zone
        skip--;            // consume one skip
        continue;          // skip this element
    }
    // Not in skip zone — process normally
    if (arr[i] % 5 == 0) {  // trigger: multiple of 5
        skip = 1;          // next 1 element will be skipped
    }
    arr[j] = arr[i];       // keep this element
    j++;
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
    explanation="Delete at specific index by shifting all subsequent elements one position left, then n--. Loop from i=pos to i=n-2. At each step: arr[i] = arr[i+1].",
    code_snippet='for (int i = pos; i < n - 1; i++)\n    arr[i] = arr[i + 1];\nn--;')
Concept.objects.create(topic=t3, title="Compaction Pattern (Two-Pointer Delete)", order=2, language="c",
    explanation="Two-pointer technique: i (read head) reads every element, j (write head) only advances when keeping. Only elements passing the KEEP condition are written. After loop, n = j. The KEEP condition is the logical NOT of the DELETE condition.",
    code_snippet='int j = 0;\nfor (int i = 0; i < n; i++)\n    if (keep_condition(arr[i]))\n        arr[j++] = arr[i];\nn = j;')
Concept.objects.create(topic=t3, title="Skip K After Trigger (Red Light Model)", order=3, language="c",
    explanation="When a trigger element is found, set skip counter to K. Next K elements are skipped (skip--, continue). Trigger itself is kept. Mental model: red light lasting K steps — after K cars, light turns green again.",
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
Problem.objects.create(topic=t3, title="Skip 1 After Every Multiple of 5", order=4,
    description="Keep all elements, but skip the next 1 element after every multiple of 5 encountered. The multiple of 5 itself is kept.",
    difficulty="medium", category="practice",
    solution_code='int skip = 0, j = 0;\nfor (int i = 0; i < n; i++) {\n    if (skip > 0) { skip--; continue; }\n    if (arr[i] % 5 == 0) skip = 1;\n    arr[j++] = arr[i];\n}\nn = j;',
    solution_explanation="Skip pattern with K=1. Trigger: multiple of 5. Trigger element kept, next 1 element skipped.")
Problem.objects.create(topic=t3, title="Skip 2 After Every Odd Number", order=5,
    description="Keep all elements, but skip the next 2 elements after every odd number encountered. The odd number itself is kept.",
    difficulty="medium", category="challenge",
    hints="Set skip = 2 when trigger fires. Trigger: arr[i] % 2 != 0.",
    solution_code='int skip = 0, j = 0;\nfor (int i = 0; i < n; i++) {\n    if (skip > 0) { skip--; continue; }\n    if (arr[i] % 2 != 0) skip = 2;\n    arr[j++] = arr[i];\n}\nn = j;',
    solution_explanation="Same skip pattern but with K=2. The odd trigger is kept, next 2 elements are dropped.")
Problem.objects.create(topic=t3, title="Delete Lowest Element", order=6,
    description="Find the minimum element, then delete its first occurrence from the array.",
    difficulty="medium", category="practice",
    hints="Two steps: 1) Find min and its position. 2) Delete at that position using shift-left.",
    solution_code='// Step 1: find min position\nint minPos = 0;\nfor (int i = 1; i < n; i++)\n    if (arr[i] < arr[minPos]) minPos = i;\n// Step 2: delete at minPos\nfor (int i = minPos; i < n - 1; i++)\n    arr[i] = arr[i + 1];\nn--;',
    solution_explanation="First find the position of the minimum, then use position deletion. Two separate steps.")

print(f"✅ Topic 3 created with {Concept.objects.filter(topic=t3).count()} concepts and {Problem.objects.filter(topic=t3).count()} problems.")
