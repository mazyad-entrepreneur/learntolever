import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 4: Reverse, Sorting, Frequency & Unique/Duplicate ──
t4=Topic.objects.create(
    module=m2, title="Reverse, Sorting, Frequency and Unique/Duplicate Operations",
    slug="reverse-sorting-frequency-unique-duplicate", order=4, is_published=True,
    introduction="Reversing swaps elements from both ends toward the center. Bubble sort repeatedly swaps adjacent out-of-order pairs. Frequency counting uses nested loops. Unique elements appear exactly once; duplicates appear more than once.",
    content_html="""<h3>Reversing: Two-Pointer Swap</h3>
<p><code>left</code> pointer at index 0, <code>right</code> pointer at index n-1. Swap. Move left forward, right backward. Stop when left &gt;= right.</p>

<h3>Trace: Reverse {5, 10, 15, 20, 25}</h3>
<table><thead><tr><th>Step</th><th>left</th><th>right</th><th>Swap</th><th>Result</th></tr></thead>
<tbody>
<tr><td>1</td><td>0 (val=5)</td><td>4 (val=25)</td><td>5 ↔ 25</td><td>{25, 10, 15, 20, 5}</td></tr>
<tr><td>2</td><td>1 (val=10)</td><td>3 (val=20)</td><td>10 ↔ 20</td><td>{25, 20, 15, 10, 5}</td></tr>
<tr><td>3</td><td>left=2, right=2</td><td>left &gt;= right</td><td>STOP</td><td>{25, 20, 15, 10, 5} ✓</td></tr>
</tbody></table>

<h3>⚠️ Why You Need a temp Variable</h3>
<table><thead><tr><th></th><th>Code</th><th>Result</th></tr></thead>
<tbody>
<tr><td>✗ WRONG</td><td><code>arr[l]=arr[r]; arr[r]=arr[l];</code></td><td>Original arr[l] lost, arr[r] copied twice</td></tr>
<tr><td>✓ CORRECT</td><td><code>int t=arr[l]; arr[l]=arr[r]; arr[r]=t;</code></td><td>Always use 3-step swap</td></tr>
</tbody></table>

<h3>Bubble Sort</h3>
<p><strong>Mental Model:</strong> In each pass, compare adjacent pairs and swap if out of order. After one pass, the largest element has bubbled to the last position. After k passes, the last k positions are sorted. Needs at most n-1 passes.</p>

<h3>Trace Pass 1: {5, 2, 8, 1}</h3>
<table><thead><tr><th>j</th><th>Compare</th><th>Swap?</th><th>Array after</th></tr></thead>
<tbody>
<tr><td>0</td><td>arr[0]=5, arr[1]=2</td><td>YES (5 &gt; 2)</td><td>{2, 5, 8, 1}</td></tr>
<tr><td>1</td><td>arr[1]=5, arr[2]=8</td><td>no</td><td>{2, 5, 8, 1}</td></tr>
<tr><td>2</td><td>arr[2]=8, arr[3]=1</td><td>YES (8 &gt; 1)</td><td>{2, 5, 1, 8} ← 8 bubbled</td></tr>
</tbody></table>

<hr>
<h3>Frequency: Nested Loop Count</h3>
<p>For each element (outer loop), count how many times it appears in the entire array (inner loop).</p>
<p><strong>Problem:</strong> prints duplicates multiple times. Fix: <strong>Visited Check</strong> — before processing arr[i], check if the same value appeared at any earlier index (arr[0..i-1]).</p>

<h3>Unique vs Duplicate</h3>
<table><thead><tr><th>Element type</th><th>Condition</th><th>Example in {10, 15, 10, 20}</th></tr></thead>
<tbody>
<tr><td>Unique</td><td>frequency == 1</td><td>15, 20</td></tr>
<tr><td>Duplicate</td><td>frequency &gt; 1</td><td>10 (appears twice)</td></tr>
</tbody></table>""",
    code_examples="""// Two-pointer reverse
int left = 0, right = n - 1;
while (left < right) {
    int temp = arr[left];
    arr[left] = arr[right];
    arr[right] = temp;
    left++;
    right--;
}

// Bubble sort — ascending order
for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - 1 - i; j++) {
        if (arr[j] > arr[j + 1]) {
            int temp = arr[j];
            arr[j] = arr[j + 1];
            arr[j + 1] = temp;
        }
    }
}
// For DESCENDING: change > to <

// Frequency with visited check
for (int i = 0; i < n; i++) {
    int already = 0;
    for (int j = 0; j < i; j++)
        if (arr[j] == arr[i]) { already = 1; break; }
    if (already) continue;

    int count = 0;
    for (int j = 0; j < n; j++)
        if (arr[j] == arr[i]) count++;
    printf("%d -> %d times\\n", arr[i], count);
}

// Print unique elements (frequency == 1)
for (int i = 0; i < n; i++) {
    int count = 0;
    for (int j = 0; j < n; j++)
        if (arr[j] == arr[i]) count++;
    if (count == 1) printf("%d ", arr[i]);
}""",
    logic_explanation="""REVERSE:
1. Two pointers: left=0, right=n-1.
2. While left < right: swap arr[left] and arr[right].
3. Move pointers inward: left++, right--.
4. For n=5: 2 swaps. Middle element stays.

BUBBLE SORT:
1. Outer loop: n-1 passes (i = 0 to n-2).
2. Inner loop: compare adjacent pairs (j = 0 to n-2-i).
3. If arr[j] > arr[j+1]: swap them.
4. After each outer pass, one more element is in its final position.
5. For descending: change > to <.

FREQUENCY:
1. Outer loop picks each element.
2. Inner loop counts all occurrences.
3. Visited check prevents duplicate output.
4. Unique = count is 1. Duplicate = count > 1.""",
    common_mistakes="""• Skipping temp variable in swap — original value lost, both positions get same value
• Using sort() returns None confusion (C has no built-in sort like Python)
• For descending sort: change > to < (NOT the other way around)
• Printing frequency info for every occurrence — use visited check
• Confusing "unique" (freq=1) with "distinct" (all different values)
• Using sort() before frequency — destroys original order (may or may not matter)""",
    beginner_notes="""💡 Always use the 3-step swap: temp → overwrite → restore.
💡 For n=5, reverse does exactly 2 swaps. Middle element doesn't move.
💡 Bubble sort: change ONE character (> to <) to switch ascending/descending.
💡 After sorting, duplicates are adjacent — makes counting easier.
💡 Visited check: scan arr[0..i-1] before processing arr[i]."""
)

Concept.objects.create(topic=t4, title="Two-Pointer Reverse", order=1, language="c",
    explanation="Swap from both ends moving inward. Stop when pointers cross.",
    code_snippet='int l = 0, r = n - 1;\nwhile (l < r) {\n    int t = arr[l]; arr[l] = arr[r]; arr[r] = t;\n    l++; r--;\n}')
Concept.objects.create(topic=t4, title="Bubble Sort", order=2, language="c",
    explanation="n-1 outer passes. Inner loop compares adjacent pairs and swaps if out of order. Sorted tail grows each pass.",
    code_snippet='for (int i = 0; i < n-1; i++)\n    for (int j = 0; j < n-1-i; j++)\n        if (arr[j] > arr[j+1]) {\n            int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t;\n        }')
Concept.objects.create(topic=t4, title="Frequency + Visited Check", order=3, language="c",
    explanation="For each element, count occurrences with inner loop. Skip if value already seen at an earlier index.",
    code_snippet='for (int i = 0; i < n; i++) {\n    int seen = 0;\n    for (int j = 0; j < i; j++)\n        if (arr[j] == arr[i]) { seen = 1; break; }\n    if (seen) continue;\n    int cnt = 0;\n    for (int j = 0; j < n; j++)\n        if (arr[j] == arr[i]) cnt++;\n    printf("%d -> %d\\n", arr[i], cnt);\n}')

Problem.objects.create(topic=t4, title="Reverse Array", order=1,
    description="Reverse the array in-place using two-pointer swap and print the result.",
    difficulty="easy", category="guided",
    solution_code='int l=0, r=n-1;\nwhile(l<r) {\n    int t=arr[l]; arr[l]=arr[r]; arr[r]=t;\n    l++; r--;\n}',
    solution_explanation="Swap from both ends. For n=5, 2 swaps needed.")
Problem.objects.create(topic=t4, title="Sort Ascending", order=2,
    description="Sort the array in ascending order using bubble sort.",
    difficulty="easy", category="guided",
    solution_code='for(int i=0;i<n-1;i++)\n    for(int j=0;j<n-1-i;j++)\n        if(arr[j]>arr[j+1]) {\n            int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t;\n        }',
    solution_explanation="Outer: n-1 passes. Inner: compare adjacent, swap if arr[j] > arr[j+1].")
Problem.objects.create(topic=t4, title="Print Frequency of Each Element", order=3,
    description="Print how many times each distinct value appears in the array (no repeats in output).",
    difficulty="medium", category="practice",
    solution_code='for(int i=0;i<n;i++) {\n    int seen=0;\n    for(int j=0;j<i;j++) if(arr[j]==arr[i]){seen=1;break;}\n    if(seen) continue;\n    int c=0;\n    for(int j=0;j<n;j++) if(arr[j]==arr[i]) c++;\n    printf("%d -> %d\\n",arr[i],c);\n}',
    solution_explanation="Visited check + frequency count. Three nested loops logically.")
Problem.objects.create(topic=t4, title="Print Unique Elements Only", order=4,
    description="Print only the elements that appear exactly once in the array.",
    difficulty="medium", category="practice",
    solution_code='for(int i=0;i<n;i++) {\n    int c=0;\n    for(int j=0;j<n;j++) if(arr[j]==arr[i]) c++;\n    if(c==1) printf("%d ",arr[i]);\n}',
    solution_explanation="Count frequency. If count == 1, it's unique. Print it.")
Problem.objects.create(topic=t4, title="Sort Then Count Unique", order=5,
    description="Sort the array, then count how many unique values it contains.",
    difficulty="medium", category="challenge",
    hints="After sorting, duplicates are adjacent. Compare arr[i] with arr[i-1] — if different, it's a new unique value.",
    solution_code='// Sort first\nfor(int i=0;i<n-1;i++)\n    for(int j=0;j<n-1-i;j++)\n        if(arr[j]>arr[j+1]) { int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t; }\n\n// Count unique\nint unique = 1; // first element is always unique\nfor(int i=1;i<n;i++)\n    if(arr[i] != arr[i-1]) unique++;\nprintf("Unique count: %d\\n", unique);',
    solution_explanation="After sorting, duplicates cluster. Just compare each element to its predecessor.")

print(f"✅ Topic 4 created.")
