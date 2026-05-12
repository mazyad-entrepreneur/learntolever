import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem,RevisionNote

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 5: Combined Operations & Array Separation ──
t5=Topic.objects.create(
    module=m2, title="Combined Operations and Array Separation",
    slug="combined-operations-array-separation", order=5, is_published=True,
    introduction="Complex problems are sequences of simpler operations. The output of one step becomes the input of the next. Separation splits one array into two based on a condition. Merging combines two arrays into one.",
    content_html="""<h3>Decomposition Framework</h3>
<ol>
<li><strong>Read completely.</strong> Underline every operation word: replace, delete, sort, find, count, reverse.</li>
<li><strong>Identify the sequence.</strong> What must happen first? What depends on the previous step?</li>
<li><strong>Does the second step use a global property?</strong> (sum, average, count) → two passes needed.</li>
<li><strong>After deletion steps, update n.</strong> Size variable must always reflect current logical size.</li>
<li><strong>Dry run on paper.</strong> Write the array state after each step before coding.</li>
</ol>

<h3>⚠️ Float vs Int Division in C</h3>
<table><thead><tr><th>Expression</th><th>Result</th><th>Why</th></tr></thead>
<tbody>
<tr><td><code>int sum=50, n=4; sum/n</code></td><td>12</td><td>Integer division — truncated!</td></tr>
<tr><td><code>(float)sum / n</code></td><td>12.5</td><td>Cast forces float division</td></tr>
</tbody></table>

<hr>
<h3>Separation: Traverse Once, Append to Two Buckets</h3>
<p>Declare two separate arrays. Traverse the source. Based on each element's property, append it to the appropriate bucket and increment that bucket's size counter.</p>

<h3>Merging: Copy arr1, Then Copy arr2</h3>
<p>Simple merge: copy all of arr1 into merged, then all of arr2. Total size = n1 + n2.</p>

<h3>Merging Without Duplicates</h3>
<p>Copy all of arr1 first. Then for each element in arr2, check if it already exists in merged before adding.</p>""",
    code_examples="""// Combined: If average > 15, delete odds; else delete evens
int sum = 0;
for (int i = 0; i < n; i++) sum += arr[i];
float avg = (float)sum / n;   // cast to float!

int j = 0;
if (avg > 15) {
    for (int i = 0; i < n; i++)
        if (arr[i] % 2 == 0) arr[j++] = arr[i];  // keep evens
} else {
    for (int i = 0; i < n; i++)
        if (arr[i] % 2 != 0) arr[j++] = arr[i];  // keep odds
}
n = j;

// Separate even and odd elements
int evens[10], odds[10];
int ec = 0, oc = 0;
for (int i = 0; i < n; i++) {
    if (arr[i] % 2 == 0)
        evens[ec++] = arr[i];
    else
        odds[oc++] = arr[i];
}

// Simple merge
int merged[20], k = 0;
for (int i = 0; i < n1; i++) merged[k++] = arr1[i];
for (int i = 0; i < n2; i++) merged[k++] = arr2[i];

// Merge without duplicates
int k = 0;
for (int i = 0; i < n1; i++) merged[k++] = arr1[i];
for (int i = 0; i < n2; i++) {
    int found = 0;
    for (int j = 0; j < k; j++)
        if (merged[j] == arr2[i]) { found = 1; break; }
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
    explanation="Compute sum/average first (cannot skip). Then branch into one of two operations based on the result.",
    code_snippet='int sum = 0;\nfor (int i = 0; i < n; i++) sum += arr[i];\nfloat avg = (float)sum / n;\nif (avg > 15) { /* operation A */ }\nelse { /* operation B */ }')
Concept.objects.create(topic=t5, title="Separate into Two Arrays", order=2, language="c",
    explanation="One pass, two output arrays with separate size counters. Each element goes to one bucket based on condition.",
    code_snippet='int evens[10], odds[10], ec=0, oc=0;\nfor (int i = 0; i < n; i++) {\n    if (arr[i]%2==0) evens[ec++] = arr[i];\n    else odds[oc++] = arr[i];\n}')
Concept.objects.create(topic=t5, title="Merge Without Duplicates", order=3, language="c",
    explanation="Copy arr1 fully. For each arr2 element, scan merged to check if it exists before adding.",
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
Problem.objects.create(topic=t5, title="Conditional Delete by Average", order=4,
    description="If the average of the array is greater than 15, delete all odd numbers. Otherwise, delete all even numbers.",
    difficulty="hard", category="challenge",
    hints="Step 1: Compute average (needs full pass). Step 2: Compaction with the chosen keep condition.",
    solution_code='int sum=0;\nfor(int i=0;i<n;i++) sum+=arr[i];\nfloat avg=(float)sum/n;\nint j=0;\nif(avg>15) {\n    for(int i=0;i<n;i++) if(arr[i]%2==0) arr[j++]=arr[i];\n} else {\n    for(int i=0;i<n;i++) if(arr[i]%2!=0) arr[j++]=arr[i];\n}\nn=j;',
    solution_explanation="Two passes: 1) compute average, 2) compact with appropriate keep condition.")
Problem.objects.create(topic=t5, title="Prime→-1, Delete Negatives, Reverse", order=5,
    description="Step 1: Replace all prime numbers with -1. Step 2: Delete all negative numbers. Step 3: Reverse the remaining array.",
    difficulty="hard", category="challenge",
    hints="Three operations in sequence. Write array state after EACH step before coding.",
    solution_code='// Step 1: Replace primes with -1\nfor(int i=0;i<n;i++) if(isPrime(arr[i])) arr[i]=-1;\n\n// Step 2: Delete negatives (keep >= 0)\nint j=0;\nfor(int i=0;i<n;i++) if(arr[i]>=0) arr[j++]=arr[i];\nn=j;\n\n// Step 3: Reverse\nint l=0,r=n-1;\nwhile(l<r){int t=arr[l];arr[l]=arr[r];arr[r]=t;l++;r--;}',
    solution_explanation="Three known patterns chained. After step 1, primes become -1. Step 2 removes them. Step 3 reverses what's left.")

print(f"✅ Topic 5 created.")
