import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 4: Reverse, Sorting, Frequency & Unique/Duplicate ──
# Covers handbook sections 7 (Reverse & Sort) + 8 (Freq, Unique, Dups)
t4=Topic.objects.create(
    module=m2, title="Reverse, Sorting, Frequency and Unique/Duplicate Operations",
    slug="reverse-sorting-frequency-unique-duplicate", order=4, is_published=True,
    introduction="Reversing swaps elements from both ends toward the center using the two-pointer technique. Bubble sort repeatedly swaps adjacent out-of-order pairs. Frequency counting uses nested loops. Unique elements appear exactly once; duplicates appear more than once.",
    content_html="""<h3>Reversing: Swap from Both Ends, Meet in Middle</h3>
<p>Use two pointers: <code>left</code> starting at index 0, <code>right</code> starting at index n-1. Swap arr[left] and arr[right]. Move left forward, right backward. Stop when left >= right.</p>

<h3>Trace: Reverse {5, 10, 15, 20, 25}</h3>
<table><thead><tr><th>step</th><th>left</th><th>right</th><th>swap</th><th>result</th></tr></thead>
<tbody>
<tr><td>1</td><td>0 (val=5)</td><td>4 (val=25)</td><td>5 ↔ 25</td><td>{25, 10, 15, 20, 5}</td></tr>
<tr><td>2</td><td>1 (val=10)</td><td>3 (val=20)</td><td>10 ↔ 20</td><td>{25, 20, 15, 10, 5}</td></tr>
<tr><td>3</td><td colspan="2">left=2, right=2, left >= right → stop</td><td colspan="2">{25, 20, 15, 10, 5} ✓</td></tr>
</tbody></table>

<h3>⚠️ Why You Need a temp Variable for Swapping</h3>
<table>
<tr><td>✗ WRONG</td><td><code>arr[left] = arr[right]; arr[right] = arr[left];</code> — original arr[left] is LOST, copies arr[right] twice!</td></tr>
<tr><td>✓ CORRECT</td><td><code>int temp = arr[left]; arr[left] = arr[right]; arr[right] = temp;</code> — save first, then overwrite. Always 3-step swap.</td></tr>
</table>

<hr>
<h3>Bubble Sort: Bubbling the Largest Element to the End Each Pass</h3>

<h4>Mental Model: Heavy Bubbles Rising</h4>
<p>In each pass, you compare adjacent pairs. The larger of each pair swaps to the right. After one complete pass, the largest element has "bubbled" all the way to the last position. After k passes, the last k positions are sorted. You need at most n-1 passes.</p>

<p>For <strong>descending</strong> sort: change <code>arr[j] > arr[j+1]</code> to <code>arr[j] < arr[j+1]</code>.</p>

<h3>Trace Pass 1: {5, 2, 8, 1}</h3>
<table><thead><tr><th>j</th><th>compare</th><th>swap?</th><th>array after</th></tr></thead>
<tbody>
<tr><td>0</td><td>arr[0]=5 vs arr[1]=2</td><td>YES (5>2)</td><td>{2, 5, 8, 1}</td></tr>
<tr><td>1</td><td>arr[1]=5 vs arr[2]=8</td><td>no</td><td>{2, 5, 8, 1}</td></tr>
<tr><td>2</td><td>arr[2]=8 vs arr[3]=1</td><td>YES (8>1)</td><td>{2, 5, 1, 8} ← 8 bubbled to end</td></tr>
</tbody></table>

<hr>
<h3>Frequency Counting: Nested Loop Approach</h3>
<p>For each element (outer loop), count how many times it appears in the entire array (inner loop). The count is the frequency of that element.</p>

<h3>⚠️ Avoiding Repeated Output for Duplicates</h3>
<p>When you print frequency for every element, you print the same value's frequency multiple times. Solution: use a <strong>"visited" check</strong> — before processing arr[i], verify it hasn't been processed before by checking if arr[j] == arr[i] for any j < i.</p>

<h3>Unique vs Duplicate: Decision Based on Count</h3>
<table><thead><tr><th>Element type</th><th>Condition</th><th>Example in {10,15,10,20}</th></tr></thead>
<tbody>
<tr><td>Unique</td><td>frequency == 1</td><td>15, 20</td></tr>
<tr><td>Duplicate</td><td>frequency > 1</td><td>10 (appears twice)</td></tr>
</tbody></table>

<hr>
<h3>🔴 Think Before Coding — Assignments</h3>
<ul>
<li><strong>4.1 (reverse with for):</strong> How many swaps for n=5? Do you swap 5 times or 2 times? When does left overtake right?</li>
<li><strong>4.2 (reverse with while):</strong> Same logic, different loop syntax. What is the while condition?</li>
<li><strong>4.3 (ascending sort):</strong> Implement bubble sort. Trace one complete pass manually before coding.</li>
<li><strong>4.4 (descending sort):</strong> What single character changes in the inner if-condition compared to ascending?</li>
<li><strong>4.5 (sort then count unique):</strong> After sorting, duplicates are adjacent. Compare arr[i] with arr[i-1] — if different, it's a new unique value.</li>
<li><strong>4.6 (unique elements):</strong> For each element, count frequency. If count == 1, print it. Simple.</li>
<li><strong>4.7 (duplicate elements):</strong> If count > 1, it's duplicate. But how to print each duplicate only once?</li>
<li><strong>4.8 (frequency of ODD numbers only):</strong> Add outer condition: only do frequency check if element is odd.</li>
<li><strong>4.9 (replace duplicates with -1):</strong> If element appeared before (at earlier index), replace with -1. First occurrence kept.</li>
<li><strong>4.10 (check if all unique):</strong> Flag starts "all unique = true." Any pair of equals → set false, stop.</li>
<li><strong>4.11 (average of unique elements):</strong> Sum only freq==1 elements. Count them. Divide. Edge case: what if none?</li>
<li><strong>4.12 (delete unique elements):</strong> Keep only freq > 1. Compaction pattern + frequency checking.</li>
</ul>""",
    code_examples="""// Two-pointer reverse — ALWAYS use temp!
int left = 0, right = n - 1;
while (left < right) {
    int temp = arr[left];  // 3-variable swap — NEVER skip temp!
    arr[left] = arr[right];
    arr[right] = temp;
    left++;
    right--;
}

// Bubble sort — ascending order
for (int i = 0; i < n - 1; i++) {        // n-1 passes
    for (int j = 0; j < n - 1 - i; j++) { // last i elements already sorted
        if (arr[j] > arr[j + 1]) {          // out of order?
            int temp = arr[j];               // swap
            arr[j] = arr[j + 1];
            arr[j + 1] = temp;
        }
    }
}
// For DESCENDING: change > to <

// Frequency with visited check (no duplicate output)
for (int i = 0; i < n; i++) {
    // Has this value already been printed?
    int already = 0;
    for (int j = 0; j < i; j++) {
        if (arr[j] == arr[i]) { already = 1; break; }
    }
    if (already) continue;  // skip: already handled
    
    // Count and print
    int count = 0;
    for (int j = 0; j < n; j++)
        if (arr[j] == arr[i]) count++;
    printf("%d → %d times\\n", arr[i], count);
}

// Print unique elements (appear exactly once)
for (int i = 0; i < n; i++) {
    int count = 0;
    for (int j = 0; j < n; j++)
        if (arr[j] == arr[i]) count++;
    if (count == 1) printf("%d ", arr[i]);
}""",
    logic_explanation="""REVERSE:
1. Two pointers: left=0, right=n-1.
2. While left < right: swap arr[left] and arr[right] using temp.
3. Move pointers inward: left++, right--.
4. For n=5: exactly 2 swaps. Middle element stays in place.
5. NEVER skip the temp variable — direct swap destroys data.

BUBBLE SORT:
1. Outer loop: n-1 passes (i = 0 to n-2).
2. Inner loop: compare adjacent pairs (j = 0 to n-2-i).
3. If arr[j] > arr[j+1]: swap them (3-step swap).
4. After each outer pass, one more element is in its final position.
5. For descending: change > to <.

FREQUENCY:
1. Outer loop picks each element.
2. Inner loop counts all occurrences.
3. Visited check (scan arr[0..i-1]) prevents duplicate output.
4. Unique = count is exactly 1. Duplicate = count > 1.""",
    common_mistakes="""• Skipping temp variable in swap — original value lost, both positions get same value
• For descending sort: change > to < (NOT the other way around)
• Printing frequency info for every occurrence — use visited check to print each value only once
• Confusing "unique" (freq=1) with "distinct" (all different values appearing in the array)
• Not handling the "already seen" check — printing {10: twice, 10: twice} for {10,10}""",
    beginner_notes="""💡 Always use the 3-step swap: temp → overwrite → restore. NEVER skip temp.
💡 For n=5, reverse does exactly 2 swaps. Middle element doesn't move.
💡 Bubble sort: change ONE character (> to <) to switch ascending/descending.
💡 After sorting, duplicates are adjacent — makes counting easier.
💡 Visited check: scan arr[0..i-1] before processing arr[i]."""
)

Concept.objects.create(topic=t4, title="Two-Pointer Reverse", order=1, language="c",
    explanation="Swap from both ends moving inward. Stop when pointers cross. For n=5, exactly 2 swaps. Always use 3-step swap with temp variable.",
    code_snippet='int l = 0, r = n - 1;\nwhile (l < r) {\n    int t = arr[l]; arr[l] = arr[r]; arr[r] = t;\n    l++; r--;\n}')
Concept.objects.create(topic=t4, title="Bubble Sort (Heavy Bubbles Rising)", order=2, language="c",
    explanation="n-1 outer passes. Inner loop compares adjacent pairs and swaps if out of order. After each pass, the largest unsorted element 'bubbles' to its final position. Sorted tail grows each pass. For descending: change > to <.",
    code_snippet='for (int i = 0; i < n-1; i++)\n    for (int j = 0; j < n-1-i; j++)\n        if (arr[j] > arr[j+1]) {\n            int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t;\n        }')
Concept.objects.create(topic=t4, title="Frequency + Visited Check", order=3, language="c",
    explanation="For each element, count occurrences with inner loop. Skip if value already seen at an earlier index (visited check prevents duplicate output). Unique: count==1, Duplicate: count>1.",
    code_snippet='for (int i = 0; i < n; i++) {\n    int seen = 0;\n    for (int j = 0; j < i; j++)\n        if (arr[j] == arr[i]) { seen = 1; break; }\n    if (seen) continue;\n    int cnt = 0;\n    for (int j = 0; j < n; j++)\n        if (arr[j] == arr[i]) cnt++;\n    printf("%d -> %d\\n", arr[i], cnt);\n}')

Problem.objects.create(topic=t4, title="Reverse Array", order=1,
    description="Reverse the array in-place using two-pointer swap and print the result.",
    difficulty="easy", category="guided",
    solution_code='int l=0, r=n-1;\nwhile(l<r) {\n    int t=arr[l]; arr[l]=arr[r]; arr[r]=t;\n    l++; r--;\n}',
    solution_explanation="Swap from both ends. For n=5, 2 swaps needed. Middle element stays.")
Problem.objects.create(topic=t4, title="Sort Ascending (Bubble Sort)", order=2,
    description="Sort the array in ascending order using bubble sort.",
    difficulty="easy", category="guided",
    solution_code='for(int i=0;i<n-1;i++)\n    for(int j=0;j<n-1-i;j++)\n        if(arr[j]>arr[j+1]) {\n            int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t;\n        }',
    solution_explanation="Outer: n-1 passes. Inner: compare adjacent, swap if arr[j] > arr[j+1].")
Problem.objects.create(topic=t4, title="Sort Descending", order=3,
    description="Sort the array in descending order using bubble sort.",
    difficulty="easy", category="practice",
    solution_code='for(int i=0;i<n-1;i++)\n    for(int j=0;j<n-1-i;j++)\n        if(arr[j]<arr[j+1]) {\n            int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t;\n        }',
    solution_explanation="Same as ascending but change > to <. One character difference.")
Problem.objects.create(topic=t4, title="Print Frequency of Each Element", order=4,
    description="Print how many times each distinct value appears in the array (no repeats in output).",
    difficulty="medium", category="practice",
    solution_code='for(int i=0;i<n;i++) {\n    int seen=0;\n    for(int j=0;j<i;j++) if(arr[j]==arr[i]){seen=1;break;}\n    if(seen) continue;\n    int c=0;\n    for(int j=0;j<n;j++) if(arr[j]==arr[i]) c++;\n    printf("%d -> %d\\n",arr[i],c);\n}',
    solution_explanation="Visited check + frequency count. Three nested loops logically.")
Problem.objects.create(topic=t4, title="Print Unique Elements Only", order=5,
    description="Print only the elements that appear exactly once in the array.",
    difficulty="medium", category="practice",
    solution_code='for(int i=0;i<n;i++) {\n    int c=0;\n    for(int j=0;j<n;j++) if(arr[j]==arr[i]) c++;\n    if(c==1) printf("%d ",arr[i]);\n}',
    solution_explanation="Count frequency. If count == 1, it's unique. Print it.")
Problem.objects.create(topic=t4, title="Sort Then Count Unique", order=6,
    description="Sort the array, then count how many unique values it contains.",
    difficulty="medium", category="challenge",
    hints="After sorting, duplicates are adjacent. Compare arr[i] with arr[i-1] — if different, it's a new unique value.",
    solution_code='// Sort first\nfor(int i=0;i<n-1;i++)\n    for(int j=0;j<n-1-i;j++)\n        if(arr[j]>arr[j+1]) { int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t; }\n\n// Count unique\nint unique = 1; // first element is always unique\nfor(int i=1;i<n;i++)\n    if(arr[i] != arr[i-1]) unique++;\nprintf("Unique count: %d\\n", unique);',
    solution_explanation="After sorting, duplicates cluster. Just compare each element to its predecessor.")

print(f"✅ Topic 4 created with {Concept.objects.filter(topic=t4).count()} concepts and {Problem.objects.filter(topic=t4).count()} problems.")
