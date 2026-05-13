import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 5: Combined Operations & Array Separation ──
# Covers handbook sections 9 (Combined Ops) + 10 (Separate & Merge)
t5=Topic.objects.create(
    module=m2, title="Combined Operations and Array Separation",
    slug="combined-operations-array-separation", order=5, is_published=True,
    introduction="Complex problems are sequences of simpler operations. The output of one step becomes the input of the next. Separation splits one array into two based on a condition. Merging combines two arrays into one. The key skill is identifying the exact sequence and the dependencies between steps.",
    content_html="""<h3>Core Idea: Operations Compose</h3>
<p>Complex problems are just <strong>sequences of simpler operations</strong>. The output of one operation becomes the input of the next. The key skill is identifying the exact sequence and the dependencies between steps.</p>

<h3>Decomposition Framework</h3>
<ol>
<li><strong>Read the problem statement completely.</strong> Underline every operation word: replace, delete, sort, find, count, reverse.</li>
<li><strong>Identify the sequence.</strong> What must happen first? What depends on the result of the previous step?</li>
<li><strong>Does the second step use a global property?</strong> (sum, average, count) Then you need two passes: one to compute the property, one to apply the operation.</li>
<li><strong>After deletion steps, update n.</strong> The size variable must always reflect the current logical size.</li>
<li><strong>Dry run on paper.</strong> Write the array state after each step before coding.</li>
</ol>

<h3>Pattern: Conditional Decision Based on Sum/Average</h3>
<p>Some problems require computing a global property (sum, average) first, then using that to decide which operation to perform. This inherently requires <strong>two passes</strong> — you cannot compute the average and make a decision in one pass.</p>

<h3>⚠️ Float vs Int Division in C</h3>
<table><thead><tr><th>Expression</th><th>Result</th><th>Why</th></tr></thead>
<tbody>
<tr><td><code>int sum=50, n=4; sum/n</code></td><td>12</td><td>Integer division — truncated!</td></tr>
<tr><td><code>(float)sum / n</code></td><td>12.5</td><td>Cast forces float division</td></tr>
</tbody></table>
<p>If both sum and n are integers, <code>sum / n</code> performs integer division (truncates decimals). Cast to float: <code>(float)sum / n</code> to get the true average. This matters when comparing against a non-integer threshold.</p>

<hr>
<h3>Separation: Traverse Once, Append to Two Buckets</h3>
<p>Declare two separate arrays. Traverse the source. Based on the element's property, append it to the appropriate bucket array and increment that bucket's size counter.</p>

<hr>
<h3>Merging: Copy arr1, Then Copy arr2 Into a Third Array</h3>
<p>Simple merge: copy all of arr1 into merged, then all of arr2. Total size = n1 + n2.</p>

<h3>Merging Without Duplicates</h3>
<p>Copy all of arr1 first. Then for each element in arr2, check if it already exists in merged before adding. If found, skip it. If not found, add it.</p>

<hr>
<h3>🔴 Think Before Coding — Assignments</h3>
<ul>
<li><strong>5.1 (replace then sum):</strong> Step 1 = replace multiples of 3 with 0 (in-place, size unchanged). Step 2 = find sum. Can both steps be done in one pass?</li>
<li><strong>5.4 (reverse then delete):</strong> Order matters. Reverse first, THEN delete. Does reversing before deleting give a different result than deleting first?</li>
<li><strong>5.5 (replace primes→-1, then delete negatives):</strong> After step 1, some elements are -1. Step 2 deletes all elements < 0. What is the "keep" condition for compaction?</li>
<li><strong>5.6 (sum-conditional decision):</strong> Compute sum first (cannot skip this step). Based on sum > 100 or not, decide which elements to delete. Write both branches before coding.</li>
<li><strong>5.7 (separate even/odd):</strong> Two additional arrays and two counters. Initial sizes? Initial count values? After the loop, how to print each?</li>
<li><strong>5.9 (merge two arrays):</strong> How large must the merged array be? What's the index where arr2's content starts?</li>
<li><strong>5.10 (merge without duplicates):</strong> When can duplicates exist? Does arr1 itself have duplicates? Adjust logic accordingly.</li>
<li><strong>5.11 (delete repeating elements):</strong> Keep only the first occurrence of each value. For each element, check if it appeared in any earlier index. If yes, skip it (compaction).</li>
<li><strong>6.3 (prime→-1, delete negatives, reverse):</strong> Three operations. Trace the array state after each one.</li>
<li><strong>6.6 (print larger array after separation):</strong> After separating, compare ec and oc. Print the larger array. What if equal?</li>
<li><strong>6.7 (replace even at ODD positions with 0):</strong> TWO conditions: i must be odd (i%2!=0) AND arr[i] must be even (arr[i]%2==0). This is a replace, not a delete.</li>
</ul>""",
    code_examples="""// Pattern: if average > 15, delete odds; else delete evens
// Step 1: compute average (full pass)
int sum = 0;
for (int i = 0; i < n; i++) sum += arr[i];
float avg = (float)sum / n;   // cast to float!

// Step 2: decide which operation based on avg
int j = 0;
if (avg > 15) {
    // delete odds: keep evens
    for (int i = 0; i < n; i++)
        if (arr[i] % 2 == 0) { arr[j] = arr[i]; j++; }
} else {
    // delete evens: keep odds
    for (int i = 0; i < n; i++)
        if (arr[i] % 2 != 0) { arr[j] = arr[i]; j++; }
}
n = j;

// Separate even and odd elements
int evens[10], odds[10];
int ec = 0, oc = 0;  // even count, odd count
for (int i = 0; i < n; i++) {
    if (arr[i] % 2 == 0)
        evens[ec++] = arr[i];  // append to evens
    else
        odds[oc++] = arr[i];   // append to odds
}
// evens has ec elements, odds has oc elements

// Simple merge: arr1 (n1 elements) + arr2 (n2 elements)
int merged[20], k = 0;
for (int i = 0; i < n1; i++) merged[k++] = arr1[i];
for (int i = 0; i < n2; i++) merged[k++] = arr2[i];
// merged has k = n1 + n2 elements

// Merge WITHOUT duplicates
int k = 0;
// First: copy all of arr1
for (int i = 0; i < n1; i++) merged[k++] = arr1[i];
// Second: copy arr2 elements only if not already in merged
for (int i = 0; i < n2; i++) {
    int found = 0;
    for (int j = 0; j < k; j++) {
        if (merged[j] == arr2[i]) { found = 1; break; }
    }
    if (!found) merged[k++] = arr2[i];
}""",
    logic_explanation="""COMBINED OPERATIONS:
1. Read the problem. List every operation in order.
2. Some operations need global info (sum, average) — compute FIRST.
3. Execute operations in sequence. Update n after each deletion.
4. Dry run: write array state after each step.

SEPARATION:
1. Two empty arrays + two size counters (both start at 0).
2. One pass through source: if condition → bucket A, else → bucket B.
3. After loop: ec elements in evens, oc elements in odds.

MERGING:
1. Copy all of arr1 into merged[0..n1-1].
2. Copy all of arr2 into merged[n1..n1+n2-1].
3. Without duplicates: check each arr2 element against merged before adding.""",
    common_mistakes="""• Integer division when you need float: sum/n truncates! Use (float)sum/n.
• Forgetting to update n after a deletion step — next step uses wrong size.
• Doing operations in wrong order — result changes.
• Merged array not declared large enough — must hold n1 + n2 elements.
• For separation: forgetting to use separate counters (ec, oc) for each bucket.""",
    beginner_notes="""💡 Break complex problems into simple steps. Each step is a pattern you already know.
💡 Always cast to float when computing averages: (float)sum / n.
💡 After every deletion step, n must be updated before the next step.
💡 Separation is just conditional traversal writing to two arrays instead of printing.
💡 For merge without duplicates: always copy arr1 fully first, then filter arr2."""
)

Concept.objects.create(topic=t5, title="Conditional Decision Based on Sum/Average", order=1, language="c",
    explanation="Compute sum/average first (cannot skip — requires full pass). Then branch into one of two operations based on the result. Inherently a two-pass problem.",
    code_snippet='int sum = 0;\nfor (int i = 0; i < n; i++) sum += arr[i];\nfloat avg = (float)sum / n;\nif (avg > 15) { /* operation A */ }\nelse { /* operation B */ }')
Concept.objects.create(topic=t5, title="Separate into Two Arrays (Two Buckets)", order=2, language="c",
    explanation="One pass, two output arrays with separate size counters. Each element goes to one bucket based on condition. Like conditional traversal but writing to two arrays instead of printing.",
    code_snippet='int evens[10], odds[10], ec=0, oc=0;\nfor (int i = 0; i < n; i++) {\n    if (arr[i]%2==0) evens[ec++] = arr[i];\n    else odds[oc++] = arr[i];\n}')
Concept.objects.create(topic=t5, title="Merge Without Duplicates", order=3, language="c",
    explanation="Copy arr1 fully first. For each arr2 element, scan merged to check if it already exists before adding. If found → skip. If not found → add.",
    code_snippet='int k=0;\nfor(int i=0;i<n1;i++) merged[k++]=arr1[i];\nfor(int i=0;i<n2;i++) {\n    int found=0;\n    for(int j=0;j<k;j++) if(merged[j]==arr2[i]){found=1;break;}\n    if(!found) merged[k++]=arr2[i];\n}')

Problem.objects.create(topic=t5, title="Replace then Sum", order=1,
    description="Replace all multiples of 3 with 0, then compute the sum of the modified array.",
    difficulty="easy", category="guided",
    solution_code='int sum=0;\nfor(int i=0;i<n;i++) {\n    if(arr[i]%3==0) arr[i]=0;\n    sum += arr[i];\n}\nprintf("Sum=%d\\n",sum);',
    solution_explanation="Both steps in one pass. Replace first, then add to sum. Zeros contribute 0.")
Problem.objects.create(topic=t5, title="Separate Even and Odd", order=2,
    description="Split the array into two arrays: one containing even elements and one containing odd elements. Print both.",
    difficulty="easy", category="practice",
    solution_code='int evens[10],odds[10],ec=0,oc=0;\nfor(int i=0;i<n;i++) {\n    if(arr[i]%2==0) evens[ec++]=arr[i];\n    else odds[oc++]=arr[i];\n}',
    solution_explanation="One traversal, two buckets. Each element goes to exactly one array.")
Problem.objects.create(topic=t5, title="Merge Two Arrays", order=3,
    description="Given two arrays, merge them into a single array and print the result.",
    difficulty="easy", category="practice",
    solution_code='int merged[20],k=0;\nfor(int i=0;i<n1;i++) merged[k++]=arr1[i];\nfor(int i=0;i<n2;i++) merged[k++]=arr2[i];',
    solution_explanation="Copy arr1 first, then arr2. Total size = n1 + n2.")
Problem.objects.create(topic=t5, title="Merge Without Duplicates", order=4,
    description="Given two arrays, merge them into a single array without any duplicate values.",
    difficulty="medium", category="practice",
    hints="Copy arr1 fully. For each arr2 element, scan merged to check existence before adding.",
    solution_code='int k=0;\nfor(int i=0;i<n1;i++) merged[k++]=arr1[i];\nfor(int i=0;i<n2;i++) {\n    int found=0;\n    for(int j=0;j<k;j++) if(merged[j]==arr2[i]){found=1;break;}\n    if(!found) merged[k++]=arr2[i];\n}',
    solution_explanation="Copy arr1 fully. For each arr2 element, check if already exists in merged before adding.")
Problem.objects.create(topic=t5, title="Conditional Delete by Average", order=5,
    description="If the average of the array is greater than 15, delete all odd numbers. Otherwise, delete all even numbers.",
    difficulty="hard", category="challenge",
    hints="Step 1: Compute average (needs full pass). Step 2: Compaction with the chosen keep condition.",
    solution_code='int sum=0;\nfor(int i=0;i<n;i++) sum+=arr[i];\nfloat avg=(float)sum/n;\nint j=0;\nif(avg>15) {\n    for(int i=0;i<n;i++) if(arr[i]%2==0) arr[j++]=arr[i];\n} else {\n    for(int i=0;i<n;i++) if(arr[i]%2!=0) arr[j++]=arr[i];\n}\nn=j;',
    solution_explanation="Two passes: 1) compute average, 2) compact with appropriate keep condition.")
Problem.objects.create(topic=t5, title="Prime→-1, Delete Negatives, Reverse", order=6,
    description="Step 1: Replace all prime numbers with -1. Step 2: Delete all negative numbers. Step 3: Reverse the remaining array.",
    difficulty="hard", category="challenge",
    hints="Three operations in sequence. Write array state after EACH step before coding.",
    solution_code='// Step 1: Replace primes with -1\nfor(int i=0;i<n;i++) if(isPrime(arr[i])) arr[i]=-1;\n\n// Step 2: Delete negatives (keep >= 0)\nint j=0;\nfor(int i=0;i<n;i++) if(arr[i]>=0) arr[j++]=arr[i];\nn=j;\n\n// Step 3: Reverse\nint l=0,r=n-1;\nwhile(l<r){int t=arr[l];arr[l]=arr[r];arr[r]=t;l++;r--;}',
    solution_explanation="Three known patterns chained. After step 1, primes become -1. Step 2 removes them. Step 3 reverses what's left.")

print(f"✅ Topic 5 created with {Concept.objects.filter(topic=t5).count()} concepts and {Problem.objects.filter(topic=t5).count()} problems.")
