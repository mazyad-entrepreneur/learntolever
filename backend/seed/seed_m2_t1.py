import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 1: Array Fundamentals + Traversal ──
t1=Topic.objects.create(
    module=m2, title="Array Fundamentals and Traversal", slug="array-fundamentals-traversal",
    order=1, is_published=True,
    introduction="An array is a named, fixed-size sequence of values of the same type, stored in contiguous memory (back-to-back bytes). It lets you work with many related values under one name instead of declaring 100 separate variables.",
    content_html="""<h3>Mental Model: Apartment Mailboxes</h3>
<p>Imagine a row of numbered mailboxes in an apartment building:</p>
<ul>
<li>All boxes are the <strong>same size</strong> (because the type is fixed: int, float, char...)</li>
<li>Each box has a <strong>numbered slot starting from 0</strong>, not 1</li>
<li>You can reach any box <strong>instantly</strong> if you know its number (O(1) access)</li>
<li>The <strong>building has a fixed number of boxes</strong> — you cannot add more later</li>
</ul>

<h3>Declaration &amp; Memory</h3>
<p>How it looks in memory:</p>
<table><thead><tr><th>Index</th><th>arr[0]</th><th>arr[1]</th><th>arr[2]</th><th>arr[3]</th><th>arr[4]</th></tr></thead>
<tbody><tr><td>Value</td><td>10</td><td>20</td><td>30</td><td>40</td><td>50</td></tr>
<tr><td>Address</td><td>1000</td><td>1004</td><td>1008</td><td>1012</td><td>1016</td></tr></tbody></table>

<h3>Why Indexing Starts at 0</h3>
<p>In C, <code>arr[i]</code> is computed as <code>*(arr + i)</code> — go to the address of arr, jump i steps forward. Starting at 0 makes the arithmetic clean with zero overhead.</p>

<h3>Traversal Patterns</h3>
<table><thead><tr><th>Pattern</th><th>Loop Setup</th><th>Visits</th></tr></thead>
<tbody>
<tr><td>Forward (default)</td><td><code>i=0; i&lt;n; i++</code></td><td>0, 1, 2, ..., n-1</td></tr>
<tr><td>Backward</td><td><code>i=n-1; i&gt;=0; i--</code></td><td>n-1, n-2, ..., 0</td></tr>
<tr><td>Even indices only</td><td><code>i=0; i&lt;n; i+=2</code></td><td>0, 2, 4, 6...</td></tr>
<tr><td>Odd indices only</td><td><code>i=1; i&lt;n; i+=2</code></td><td>1, 3, 5, 7...</td></tr>
</tbody></table>

<h3>Conditional Traversal — Security Checkpoint Model</h3>
<p>Every element tries to "pass through" the loop body. The <code>if</code> condition is the checkpoint. Elements that meet the condition are processed. Others are skipped silently. The loop visits every element but only acts on some.</p>

<h3>Dry Run: arr = {5, 12, 18, 7, 25}, n = 5</h3>
<table><thead><tr><th>i</th><th>i &lt; 5?</th><th>arr[i]</th><th>Action</th></tr></thead>
<tbody>
<tr><td>0</td><td>true</td><td>5</td><td>print 5</td></tr>
<tr><td>1</td><td>true</td><td>12</td><td>print 12</td></tr>
<tr><td>2</td><td>true</td><td>18</td><td>print 18</td></tr>
<tr><td>3</td><td>true</td><td>7</td><td>print 7</td></tr>
<tr><td>4</td><td>true</td><td>25</td><td>print 25</td></tr>
<tr><td>5</td><td>FALSE</td><td>—</td><td>loop ends</td></tr>
</tbody></table>""",
    code_examples="""// Declaration & Initialization
int arr[5] = {10, 20, 30, 40, 50};
// arr  = name
// 5    = fixed size
// int  = each element is 4 bytes
// Total memory = 5 x 4 = 20 bytes

// Accessing & Modifying
int x = arr[2];    // x = 30  (THIRD element = index 2, not 3!)
arr[0] = 99;       // arr is now {99, 20, 30, 40, 50}

// Forward Traversal
for (int i = 0; i < n; i++) {
    printf("%d ", arr[i]);
}

// Conditional Traversal — Print only elements > 20
for (int i = 0; i < n; i++) {
    if (arr[i] > 20) {
        printf("%d\\n", arr[i]);
    }
}""",
    logic_explanation="""Golden Rule: For an array of size n, valid indices are 0 to n-1.
Index n does NOT exist — accessing it is undefined behaviour.

Traversal = using loop variable i as the index, starting from 0, incrementing until you reach n. At each step, you do something with arr[i].

Key insight: i (the index) and arr[i] (the value) are DIFFERENT things.
- i % 2 == 0 means EVEN INDEX
- arr[i] % 2 == 0 means EVEN VALUE
Confusing these is one of the most common beginner mistakes.""",
    common_mistakes="""• Using i <= n instead of i < n — accesses arr[n] which does NOT exist
• "Third element" = index 3 — WRONG! It is index 2 (0-based)
• Starting from index 1 in a forward loop — misses arr[0]
• Confusing value vs index: arr[i] % 2 == 0 (even value) vs i % 2 == 0 (even index)""",
    beginner_notes="""💡 Think of a 1D array as a numbered shelf — each slot holds one item, starting from slot 0.
💡 Always use i < n (strict less-than) in your loops.
💡 When a problem says "third element", translate it to index 2 immediately.
💡 For max/min problems: initialize with arr[0], then loop from i=1.
💡 For search: use a 'found' flag variable to signal success after the loop.""",
    visual_explanation="""Array in memory (contiguous):
┌──────┬──────┬──────┬──────┬──────┐
│  10  │  20  │  30  │  40  │  50  │
└──────┴──────┴──────┴──────┴──────┘
 [0]    [1]    [2]    [3]    [4]
 ↑ first                     ↑ last = n-1"""
)

# Concepts for Topic 1
Concept.objects.create(topic=t1, title="Declaration & Memory Layout", order=1, language="c",
    explanation="An array of size n occupies n × sizeof(type) contiguous bytes. int arr[5] uses 20 bytes (5 × 4). Elements are accessed by index starting from 0.",
    code_snippet='int arr[5] = {10, 20, 30, 40, 50};\n// Total memory = 5 * 4 = 20 bytes\n// Valid indices: 0, 1, 2, 3, 4')
Concept.objects.create(topic=t1, title="Forward Traversal", order=2, language="c",
    explanation="Visit every element from index 0 to n-1 using a for loop. This is the most common array operation — nearly every problem starts with this pattern.",
    code_snippet='for (int i = 0; i < n; i++) {\n    printf("%d ", arr[i]);\n}')
Concept.objects.create(topic=t1, title="Conditional Traversal", order=3, language="c",
    explanation="Same traversal loop, but add an if condition inside. Only elements passing the check are processed. Others are silently skipped.",
    code_snippet='// Print only even numbers\nfor (int i = 0; i < n; i++) {\n    if (arr[i] % 2 == 0) {\n        printf("%d ", arr[i]);\n    }\n}')
Concept.objects.create(topic=t1, title="Finding Max / Min", order=4, language="c",
    explanation="Initialize max/min with arr[0]. Loop from i=1. Compare each element and update if larger/smaller. After the loop, you have the answer.",
    code_snippet='int max = arr[0];\nfor (int i = 1; i < n; i++) {\n    if (arr[i] > max) max = arr[i];\n}\n// For min: change > to <')

# Problems for Topic 1
Problem.objects.create(topic=t1, title="Declare, Initialize, and Print", order=1,
    description="Declare an integer array of 5 elements, initialize it with values, and print each value using a loop.",
    difficulty="easy", category="guided", is_assignment=False,
    solution_code='#include <stdio.h>\nint main() {\n    int arr[5] = {10, 20, 30, 40, 50};\n    for (int i = 0; i < 5; i++) {\n        printf("arr[%d] = %d\\n", i, arr[i]);\n    }\n    return 0;\n}',
    solution_explanation="Declare with int arr[5], use a for loop from 0 to 4 (i < 5). Access each element with arr[i].")
Problem.objects.create(topic=t1, title="Sum of All Elements", order=2,
    description="Read n elements into an array and print their sum.",
    difficulty="easy", category="guided",
    hints="Use a variable 'sum' initialized to 0. Add arr[i] to sum at each step.",
    solution_code='int sum = 0;\nfor (int i = 0; i < n; i++) {\n    sum += arr[i];\n}\nprintf("Sum = %d\\n", sum);',
    solution_explanation="Running total pattern: start sum at 0, accumulate arr[i] each iteration.")
Problem.objects.create(topic=t1, title="Print Only Even Values", order=3,
    description="Given an array, print only the elements that are even numbers.",
    difficulty="easy", category="practice",
    solution_code='for (int i = 0; i < n; i++) {\n    if (arr[i] % 2 == 0) {\n        printf("%d ", arr[i]);\n    }\n}',
    solution_explanation="Conditional traversal: arr[i] % 2 == 0 checks if the VALUE is even.")
Problem.objects.create(topic=t1, title="Find Maximum and Minimum", order=4,
    description="Find and print the largest and smallest elements in an array.",
    difficulty="easy", category="practice",
    solution_code='int max = arr[0], min = arr[0];\nfor (int i = 1; i < n; i++) {\n    if (arr[i] > max) max = arr[i];\n    if (arr[i] < min) min = arr[i];\n}\nprintf("Max=%d, Min=%d\\n", max, min);',
    solution_explanation="Initialize both with arr[0]. Start loop from i=1 (arr[0] already checked). Update on each comparison.")
Problem.objects.create(topic=t1, title="Linear Search", order=5,
    description="Search for a target value in the array. Print its index if found, or 'Not found' otherwise.",
    difficulty="easy", category="practice",
    solution_code='int target = 25, found = -1;\nfor (int i = 0; i < n; i++) {\n    if (arr[i] == target) {\n        found = i;\n        break;\n    }\n}\nif (found != -1) printf("Found at index %d\\n", found);\nelse printf("Not found\\n");',
    solution_explanation="Use a found variable initialized to -1. When match found, store index and break. After loop, check found.")
Problem.objects.create(topic=t1, title="Elements Above Average", order=6,
    description="Compute the average of all elements, then print only those above the average. (Requires TWO passes through the array.)",
    difficulty="medium", category="challenge",
    hints="First pass: compute sum and average. Second pass: print elements where arr[i] > avg. Use float for average!",
    solution_code='// Pass 1: compute average\nint sum = 0;\nfor (int i = 0; i < n; i++) sum += arr[i];\nfloat avg = (float)sum / n;\n\n// Pass 2: print above average\nfor (int i = 0; i < n; i++) {\n    if (arr[i] > avg) printf("%d ", arr[i]);\n}',
    solution_explanation="Cannot be done in one pass — you need to know the average before you can compare. Cast sum to float for correct division.")

print(f"✅ Topic 1 created with {Concept.objects.filter(topic=t1).count()} concepts and {Problem.objects.filter(topic=t1).count()} problems.")
