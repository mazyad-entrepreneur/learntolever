import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem,RevisionNote

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 6: Exam Simulation & Practice (Pattern Library + Common Mistakes) ──
t6=Topic.objects.create(
    module=m2, title="Exam Simulation and Practice",
    slug="exam-simulation-practice", order=6, is_published=True,
    introduction="This topic is your exam preparation toolkit. It contains the 10 core patterns you need to solve ANY array problem, plus a comprehensive mistake checklist and a pre-submission debugging ritual.",
    content_html="""<h3>The 10 Core Patterns</h3>
<p>Every array problem you will encounter is a combination of these 10 patterns. Master them individually, then learn to compose them.</p>

<table><thead><tr><th>#</th><th>Pattern</th><th>Key Idea</th></tr></thead>
<tbody>
<tr><td>1</td><td>Forward Traversal</td><td><code>for(i=0; i&lt;n; i++)</code> — visit every element</td></tr>
<tr><td>2</td><td>Find Max/Min</td><td>Initialize with arr[0], compare from i=1</td></tr>
<tr><td>3</td><td>Replace by Condition</td><td>if(condition) arr[i] = new_value</td></tr>
<tr><td>4</td><td>Compaction (Delete)</td><td>j=0, if(keep) arr[j++]=arr[i], n=j</td></tr>
<tr><td>5</td><td>Skip K After Trigger</td><td>skip counter + continue</td></tr>
<tr><td>6</td><td>Two-Pointer Reverse</td><td>l=0, r=n-1, swap and move inward</td></tr>
<tr><td>7</td><td>Bubble Sort</td><td>Adjacent compare-swap, n-1 passes</td></tr>
<tr><td>8</td><td>Frequency + Visited</td><td>Nested loops + already-seen check</td></tr>
<tr><td>9</td><td>isPrime Helper</td><td>Trial division from 2 to n-1</td></tr>
<tr><td>10</td><td>Insert at Position</td><td>Shift right→left, place value, n++</td></tr>
</tbody></table>

<hr>
<h3>Common Mistake Checklist</h3>

<h4>⚠️ Indexing & Bounds</h4>
<table>
<tr><td>✗</td><td><code>i &lt;= n</code> — accesses arr[n] which is out of bounds</td></tr>
<tr><td>✗</td><td>"Third element" = index 3 — it is index 2</td></tr>
<tr><td>✗</td><td>Starting from index 1 — misses arr[0]</td></tr>
<tr><td>✓</td><td>Always: <code>i &lt; n</code>, indices from 0 to n-1</td></tr>
</table>

<h4>⚠️ Swapping</h4>
<table>
<tr><td>✗</td><td><code>arr[l]=arr[r]; arr[r]=arr[l];</code> — original arr[l] lost</td></tr>
<tr><td>✓</td><td><code>int t=arr[l]; arr[l]=arr[r]; arr[r]=t;</code> — always 3-step</td></tr>
</table>

<h4>⚠️ Integer Division</h4>
<table>
<tr><td>✗</td><td><code>int avg = sum/n;</code> — truncates: 7/2 = 3</td></tr>
<tr><td>✓</td><td><code>float avg = (float)sum/n;</code> — correct: 7/2 = 3.5</td></tr>
</table>

<h4>⚠️ Size Management</h4>
<table>
<tr><td>✗</td><td>Forgetting n-- after deletion or n=j after compaction</td></tr>
<tr><td>✗</td><td>Forgetting n++ after insertion</td></tr>
<tr><td>✓</td><td>Always update n immediately after any size change</td></tr>
</table>

<h4>⚠️ Conditions</h4>
<table>
<tr><td>✗</td><td>Confusing arr[i]%2==0 (even VALUE) with i%2==0 (even INDEX)</td></tr>
<tr><td>✗</td><td>Not handling overlap in two-condition replacement</td></tr>
<tr><td>✗</td><td>Not returning 0 for n&lt;2 in isPrime</td></tr>
<tr><td>✓</td><td>Test isPrime(0), isPrime(1), isPrime(2) separately</td></tr>
</table>

<hr>
<h3>✅ Pre-Submission Debugging Ritual</h3>
<ol>
<li><strong>Trace manually</strong> with 3–4 elements. Write every variable value at every step.</li>
<li><strong>Test edge cases:</strong> n=0, n=1, all match, none match.</li>
<li><strong>Check every loop bound:</strong> should it be <code>i &lt; n</code> or <code>i &lt; n-1</code>?</li>
<li><strong>After any deletion:</strong> is n updated?</li>
<li><strong>Global property (sum, avg):</strong> computed BEFORE the conditional operation?</li>
</ol>""",
    code_examples="""// Pattern 1: Forward Traversal
for (int i = 0; i < n; i++) { /* use arr[i] */ }

// Pattern 2: Find Max / Min
int max = arr[0];
for (int i = 1; i < n; i++)
    if (arr[i] > max) max = arr[i];

// Pattern 3: Replace by Condition
for (int i = 0; i < n; i++)
    if (condition(arr[i])) arr[i] = new_value;

// Pattern 4: Compaction (Delete by Condition)
int j = 0;
for (int i = 0; i < n; i++)
    if (keep_condition(arr[i])) arr[j++] = arr[i];
n = j;

// Pattern 5: Skip K After Trigger
int skip = 0, j = 0;
for (int i = 0; i < n; i++) {
    if (skip > 0) { skip--; continue; }
    if (trigger(arr[i])) skip = K;
    arr[j++] = arr[i];
}
n = j;

// Pattern 6: Two-Pointer Reverse
int l = 0, r = n - 1;
while (l < r) {
    int t = arr[l]; arr[l] = arr[r]; arr[r] = t;
    l++; r--;
}

// Pattern 7: Bubble Sort
for (int i = 0; i < n-1; i++)
    for (int j = 0; j < n-1-i; j++)
        if (arr[j] > arr[j+1]) {
            int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t;
        }

// Pattern 8: Frequency + Visited
for (int i = 0; i < n; i++) {
    int seen = 0;
    for (int j = 0; j < i; j++)
        if (arr[j] == arr[i]) { seen = 1; break; }
    if (seen) continue;
    int cnt = 0;
    for (int j = 0; j < n; j++)
        if (arr[j] == arr[i]) cnt++;
    printf("%d -> %d\\n", arr[i], cnt);
}

// Pattern 9: isPrime
int isPrime(int n) {
    if (n < 2) return 0;
    for (int i = 2; i < n; i++)
        if (n % i == 0) return 0;
    return 1;
}

// Pattern 10: Insert at Position
for (int i = n; i > pos; i--) arr[i] = arr[i-1];
arr[pos] = value;
n++;""",
    logic_explanation="""Every array problem is built from these 10 patterns.

When facing a complex problem:
1. Identify which patterns apply.
2. Determine the ORDER of execution.
3. Check dependencies (does step 2 need data from step 1?).
4. Execute each step, updating n as needed.
5. Dry run with a small example.

Key principle: COMPOSE, don't re-invent. If you know the 10 patterns, you can solve any combination.""",
    common_mistakes="""This topic IS the mistake checklist. Review the content section above before every exam.

Top 5 exam mistakes:
1. i <= n instead of i < n (off-by-one)
2. Forgetting temp in swap (data corruption)
3. Integer division instead of float (wrong average)
4. Not updating n after deletion (accessing deleted data)
5. Confusing value (arr[i]) with index (i) in conditions""",
    beginner_notes="""💡 Print this pattern library. Tape it to your wall. Reference it while practicing.
💡 Before every exam, run through the mistake checklist once.
💡 The debugging ritual takes 2 minutes but catches 90% of bugs.
💡 When stuck on a complex problem: decompose it into patterns you recognize.
💡 Practice composing 2-3 patterns together — that's what exam questions test."""
)

# ── Revision Notes for Module 2 ──
RevisionNote.objects.create(module=m2, title="Array Fundamentals", order=1,
    summary="Arrays are fixed-size, contiguous memory blocks. Index from 0 to n-1. Declared with type name[size]. Access with arr[i]. Traversal uses for(i=0; i<n; i++).",
    key_points="• Array indices: 0 to n-1 (NEVER n)\n• Contiguous memory: arr[i] = *(arr + i)\n• Forward: i=0; i<n; i++\n• Backward: i=n-1; i>=0; i--\n• Conditional: add if inside loop\n• Max/Min: init with arr[0], loop from 1")
RevisionNote.objects.create(module=m2, title="Operations Summary", order=2,
    summary="Replace: overwrite in-place, size unchanged. Insert: shift right→left, place value, n++. Delete: shift left or compact with j pointer, n=j. Skip: trigger sets counter, next K elements dropped.",
    key_points="• Replace: if(cond) arr[i] = new_val\n• Insert: shift from n to pos+1 backward, arr[pos]=val, n++\n• Delete at pos: shift from pos to n-2 forward, n--\n• Compact: j=0, if(keep) arr[j++]=arr[i], n=j\n• Skip: skip counter + continue pattern\n• Always update n after size changes")
RevisionNote.objects.create(module=m2, title="Advanced Operations", order=3,
    summary="Reverse uses two-pointer swap. Bubble sort uses adjacent compare-swap in n-1 passes. Frequency uses nested loops with visited check. Separation writes to two buckets. Merge copies sequentially.",
    key_points="• Reverse: l=0, r=n-1, 3-step swap\n• Sort: outer i 0→n-2, inner j 0→n-2-i\n• Ascending: arr[j]>arr[j+1] → swap\n• Descending: change > to <\n• Frequency: nested loops + visited check\n• Unique: freq==1; Duplicate: freq>1\n• Separate: two arrays, two counters\n• Merge: copy arr1, then arr2")

print(f"✅ Topic 6 + Revision Notes created.")
print(f"📊 Module 2 totals: {Topic.objects.filter(module=m2).count()} topics, {Concept.objects.filter(topic__module=m2).count()} concepts, {Problem.objects.filter(topic__module=m2).count()} problems, {RevisionNote.objects.filter(module=m2).count()} revision notes.")
