import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 1: Array Fundamentals + Traversal ──
# Covers handbook sections 0 (Overview), 1 (Introduction), 2 (Traversal)
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
<p>When you write <code>int arr[5] = {10, 20, 30, 40, 50};</code>, here is what happens:</p>
<ul>
<li><code>arr</code> is the name</li>
<li><code>5</code> is the fixed size</li>
<li><code>int</code> means each element is 4 bytes (on most systems)</li>
<li>Total memory used: 5 × 4 = <strong>20 bytes</strong></li>
</ul>

<p>How it looks in memory (addresses are hypothetical):</p>
<table><thead><tr><th>Address</th><th>1000</th><th>1004</th><th>1008</th><th>1012</th><th>1016</th></tr></thead>
<tbody>
<tr><td><strong>Index</strong></td><td>arr[0]</td><td>arr[1]</td><td>arr[2]</td><td>arr[3]</td><td>arr[4]</td></tr>
<tr><td><strong>Value</strong></td><td>10</td><td>20</td><td>30</td><td>40</td><td>50</td></tr>
</tbody></table>

<h3>⚠️ Golden Rule</h3>
<p>For an array of size <strong>n</strong>, valid indices are <code>0</code> to <code>n-1</code>. Index <code>n</code> does <strong>NOT</strong> exist and accessing it is undefined behavior (a common bug).</p>

<h3>Why Indexing Starts at 0, Not 1</h3>
<p>In C, the array name is a pointer to the first element. <code>arr[i]</code> is computed as <code>*(arr + i)</code> — meaning "go to the address of arr, then jump i steps forward." If indexing started at 1, every access would require a subtraction. Starting at 0 makes the math clean and fast.</p>

<h3>Accessing &amp; Modifying Elements</h3>
<table><thead><tr><th>Operation</th><th>Code</th><th>Result</th></tr></thead>
<tbody>
<tr><td>Read (access by index)</td><td><code>int x = arr[2];</code></td><td>x = 30 (third element)</td></tr>
<tr><td>Write (modify by index)</td><td><code>arr[0] = 99;</code></td><td>arr is now {99, 20, 30, 40, 50}</td></tr>
</tbody></table>
<p><strong>Critical:</strong> "Third element" = index 2 (not 3!). Always translate ordinal words to 0-based indices immediately.</p>

<hr>
<h3>Array Traversal</h3>
<p><strong>Core idea:</strong> Traversal = using a loop variable <code>i</code> as the index, starting from 0, incrementing until you reach n. At each step, you do something with <code>arr[i]</code>.</p>

<h3>Dry Run: arr = {5, 12, 18, 7, 25}, n = 5</h3>
<table><thead><tr><th>i</th><th>condition (i &lt; 5)</th><th>arr[i]</th><th>action</th></tr></thead>
<tbody>
<tr><td><strong>0</strong></td><td>✓ true</td><td>5</td><td>print 5</td></tr>
<tr><td><strong>1</strong></td><td>✓ true</td><td>12</td><td>print 12</td></tr>
<tr><td><strong>2</strong></td><td>✓ true</td><td>18</td><td>print 18</td></tr>
<tr><td><strong>3</strong></td><td>✓ true</td><td>7</td><td>print 7</td></tr>
<tr><td><strong>4</strong></td><td>✓ true</td><td>25</td><td>print 25</td></tr>
<tr><td>5</td><td>✗ FALSE — loop ends</td><td>—</td><td>—</td></tr>
</tbody></table>

<h3>All Traversal Patterns You Need</h3>
<table><thead><tr><th>Pattern</th><th>Loop Setup</th><th>Visits</th></tr></thead>
<tbody>
<tr><td>Forward (default)</td><td><code>i = 0; i &lt; n; i++</code></td><td>0, 1, 2, 3, ... n-1</td></tr>
<tr><td>Backward</td><td><code>i = n-1; i &gt;= 0; i--</code></td><td>n-1, n-2, ... 1, 0</td></tr>
<tr><td>Even indices only</td><td><code>i = 0; i &lt; n; i += 2</code></td><td>0, 2, 4, 6...</td></tr>
<tr><td>Odd indices only</td><td><code>i = 1; i &lt; n; i += 2</code></td><td>1, 3, 5, 7...</td></tr>
</tbody></table>

<h3>Conditional Traversal — Security Checkpoint Model</h3>
<p>Every element tries to "pass through" the loop body. The <code>if</code> condition is the checkpoint. Elements that meet the condition pass and get processed. Others are skipped silently. The loop itself never stops — it visits everyone, but only acts on some.</p>

<h3>⚠️ The Most Common Traversal Bug</h3>
<table>
<tr><td>✗ WRONG</td><td><code>i &lt;= n</code> — accesses arr[n] which doesn't exist. Reads garbage memory or crashes.</td></tr>
<tr><td>✓ CORRECT</td><td><code>i &lt; n</code> — last valid access is arr[n-1]. Correct always.</td></tr>
</table>

<hr>
<h3>🔴 Think Before Coding — Assignments</h3>
<p>For each concept, answer these thinking prompts BEFORE writing code:</p>
<ul>
<li><strong>1.1 (Declare, Init, Print):</strong> How do you declare an array and give it values at the same time? What syntax does C use? How do you print each value — one at a time, using what loop?</li>
<li><strong>1.2 (Access third element):</strong> "Third element" — what index is that? First = index 0, second = index 1, third = index ?</li>
<li><strong>1.3 (Sum of elements):</strong> You need a running total. What variable stores it? Initial value? What do you do at each loop step?</li>
<li><strong>1.4–1.9 (Conditional traversal):</strong> What is the condition? What is the action? Even vs odd number check — arr[i] % 2 gives what for even? For odd?</li>
<li><strong>1.7 (Even indices):</strong> Are you checking the <em>value</em> or the <em>index</em>? i vs arr[i] — these are different things!</li>
<li><strong>1.10–1.11 (Max/Min):</strong> How do you "remember" the largest value seen so far? What variable? What initial value?</li>
<li><strong>1.13 (Search):</strong> What when found? What after loop if never found? How to communicate "found" vs "not found"?</li>
<li><strong>1.14 (Above average):</strong> Requires TWO passes. First pass calculates what? Second pass uses what? Can you do it in one pass?</li>
</ul>""",
    code_examples="""// Declaration & Initialization
int arr[5] = {10, 20, 30, 40, 50};
// arr  = name
// 5    = fixed size
// int  = each element is 4 bytes
// Total memory = 5 x 4 = 20 bytes

// Accessing & Modifying
int x = arr[2];    // x = 30  (THIRD element = index 2, not 3!)
arr[0] = 99;       // arr is now {99, 20, 30, 40, 50}

// Standard Forward Traversal Pattern
for (int i = 0; i < n; i++) {
    // do something with arr[i]
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
Confusing these is one of the most common beginner mistakes.

Before writing code, always answer three questions:
1. What is the input?
2. What transformation do I need to apply?
3. What is the expected output?
Draw the array on paper first. Trace manually. Then code.""",
    common_mistakes="""• Using i <= n instead of i < n — accesses arr[n] which does NOT exist
• "Third element" = index 3 — WRONG! It is index 2 (0-based)
• Starting from index 1 in a forward loop — misses arr[0]
• Confusing value vs index: arr[i] % 2 == 0 (even value) vs i % 2 == 0 (even index)""",
    beginner_notes="""💡 Think of a 1D array as a numbered shelf — each slot holds one item, starting from slot 0.
💡 Always use i < n (strict less-than) in your loops.
💡 When a problem says "third element", translate it to index 2 immediately.
💡 For max/min problems: initialize with arr[0], then loop from i=1.
💡 For search: use a 'found' flag variable to signal success after the loop.
💡 Read each section in order. Understand the mental model first, then study the code pattern, then trace the dry run manually on paper, then attempt the assignments.""",
    visual_explanation="""Array in memory (contiguous):
┌──────┬──────┬──────┬──────┬──────┐
│  10  │  20  │  30  │  40  │  50  │
└──────┴──────┴──────┴──────┴──────┘
 [0]    [1]    [2]    [3]    [4]
 ↑ first                     ↑ last = n-1"""
)

# Concepts for Topic 1
Concept.objects.create(topic=t1, title="Declaration & Memory Layout", order=1, language="c",
    explanation="An array of size n occupies n × sizeof(type) contiguous bytes. int arr[5] uses 20 bytes (5 × 4). Elements are accessed by index starting from 0. The array name is a pointer to the first element — arr[i] is computed as *(arr + i).",
    code_snippet='int arr[5] = {10, 20, 30, 40, 50};\n// Total memory = 5 * 4 = 20 bytes\n// Valid indices: 0, 1, 2, 3, 4\n// arr[5] does NOT exist!')
Concept.objects.create(topic=t1, title="Forward Traversal", order=2, language="c",
    explanation="Visit every element from index 0 to n-1 using a for loop. This is the most common array operation — nearly every problem starts with this pattern. Use i < n (strict less-than), never i <= n.",
    code_snippet='for (int i = 0; i < n; i++) {\n    printf("%d ", arr[i]);\n}')
Concept.objects.create(topic=t1, title="Conditional Traversal (Security Checkpoint Model)", order=3, language="c",
    explanation="Same traversal loop, but add an if condition inside. Every element 'passes through' the loop. The if condition is the checkpoint — only elements meeting the condition are processed. Others are silently skipped. The loop visits everyone but only acts on some.",
    code_snippet='// Print only even numbers\nfor (int i = 0; i < n; i++) {\n    if (arr[i] % 2 == 0) {\n        printf("%d ", arr[i]);\n    }\n}')
Concept.objects.create(topic=t1, title="Finding Max / Min", order=4, language="c",
    explanation="You can't see all elements at once. Walk through them one by one, 'remembering' the largest/smallest seen so far. Initialize max/min with arr[0]. Loop from i=1. Compare each element and update if larger/smaller. After the loop, you have the answer.",
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
