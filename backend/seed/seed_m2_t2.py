import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 2: Conditional Replace & Insertion ──
t2=Topic.objects.create(
    module=m2, title="Conditional Replacement and Insertion", slug="conditional-replace-insertion",
    order=2, is_published=True,
    introduction="Replacing means traversing the array, checking a condition at each element, and overwriting the value if the condition is true. The array size stays the same. Insertion means shifting elements to make room for a new value at a specific position.",
    content_html="""<h3>Replacement — Core Idea</h3>
<p>Traverse the array. At each element, check a condition. If true, <strong>overwrite that element</strong> with the new value. The array size stays the same — you are not removing or adding, just changing values.</p>

<h3>Core Conditions to Know Cold</h3>
<table><thead><tr><th>Condition</th><th>C Code</th><th>12?</th><th>15?</th></tr></thead>
<tbody>
<tr><td>Even number</td><td><code>arr[i] % 2 == 0</code></td><td>YES</td><td>no</td></tr>
<tr><td>Odd number</td><td><code>arr[i] % 2 != 0</code></td><td>no</td><td>YES</td></tr>
<tr><td>Multiple of 3</td><td><code>arr[i] % 3 == 0</code></td><td>YES</td><td>YES</td></tr>
<tr><td>Multiple of 5</td><td><code>arr[i] % 5 == 0</code></td><td>no</td><td>YES</td></tr>
<tr><td>Multiple of k</td><td><code>arr[i] % k == 0</code></td><td>generalised</td><td>—</td></tr>
</tbody></table>

<h3>⚠️ Order Matters with Two Conditions</h3>
<p>When two conditions can both be true simultaneously, handle the <strong>overlap first</strong>. Two separate <code>if</code> statements may cause the second to overwrite the first replacement.</p>

<h3>Checking for Prime Numbers</h3>
<p><strong>Mental Model — Trial Division:</strong> A number is prime if no number from 2 to n-1 divides it evenly. Test each divisor one by one. Find one that works → not prime. None work → prime.</p>
<p>Special cases: <strong>0 and 1 are NOT prime. 2 is prime (smallest).</strong></p>

<h3>Insertion — Core Idea</h3>
<p>To insert at position p: <strong>shift all elements from position p onwards one step to the right</strong> to make room, then place the new value at position p. Size increases by 1.</p>
<p><strong>Mental Model — Inserting in a line of people:</strong> Everyone from position p onwards must step one place to the right first, creating a gap. Then the new person fills that gap.</p>

<h3>⚠️ Always Shift Right→Left (from end toward insertion point)</h3>
<table><thead><tr><th></th><th>Direction</th><th>Result</th></tr></thead>
<tbody>
<tr><td>✗ WRONG</td><td>Left→Right (<code>i = pos; i &lt; n</code>)</td><td>Overwrites data before saving it</td></tr>
<tr><td>✓ CORRECT</td><td>Right→Left (<code>i = n; i &gt; pos</code>)</td><td>Move last element first, work backwards</td></tr>
</tbody></table>

<h3>Dry Run: Insert 99 at pos=2, n=5</h3>
<table><thead><tr><th>i</th><th>i &gt; 2?</th><th>Action</th><th>Array state</th></tr></thead>
<tbody>
<tr><td>5</td><td>yes</td><td>arr[5]=arr[4]=50</td><td>{10,20,30,40,50,50}</td></tr>
<tr><td>4</td><td>yes</td><td>arr[4]=arr[3]=40</td><td>{10,20,30,40,40,50}</td></tr>
<tr><td>3</td><td>yes</td><td>arr[3]=arr[2]=30</td><td>{10,20,30,30,40,50}</td></tr>
<tr><td>2</td><td>NO</td><td>arr[2]=99</td><td>{10,20,99,30,40,50} ✓</td></tr>
</tbody></table>""",
    code_examples="""// Replace all even numbers with 0
for (int i = 0; i < n; i++) {
    if (arr[i] % 2 == 0) {     // condition
        arr[i] = 0;             // replace
    }
}
// {12, 7, 18, 9, 24, 11} becomes {0, 7, 0, 9, 0, 11}

// CORRECT: handle overlap first with else-if
if (arr[i] % 3 == 0 && arr[i] % 5 == 0) arr[i] = 1;
else if (arr[i] % 3 == 0) arr[i] = 0;
else if (arr[i] % 5 == 0) arr[i] = 1;

// isPrime helper function
int isPrime(int n) {
    if (n < 2) return 0;           // 0 and 1 are not prime
    for (int j = 2; j < n; j++) {
        if (n % j == 0) return 0;  // found a divisor
    }
    return 1;                       // no divisor found: prime
}

// Insert value 99 at position pos=2
// Before: {10, 20, 30, 40, 50}, n=5
for (int i = n; i > pos; i--) {
    arr[i] = arr[i - 1];   // shift right
}
arr[pos] = 99;
n++;
// After: {10, 20, 99, 30, 40, 50}, n=6""",
    logic_explanation="""REPLACEMENT:
1. Traverse the array with a for loop.
2. At each element, check the condition.
3. If true, overwrite arr[i] with the new value.
4. Array size stays the same.

Two conditions overlap? Use if / else-if / else. Handle the overlap case FIRST.

isPrime logic:
- 0 and 1 → NOT prime (return 0)
- Loop j from 2 to n-1: if n % j == 0, found divisor → NOT prime
- If no divisor found → prime (return 1)
- Test: isPrime(0)=0, isPrime(1)=0, isPrime(2)=1, isPrime(13)=1

INSERTION:
1. Shift elements from position n down to pos+1 (right to left).
2. Place new value at arr[pos].
3. Increment n.
4. Array must have extra capacity declared.""",
    common_mistakes="""• WRONG: Two separate ifs for overlapping conditions — second if may overwrite first replacement
• CORRECT: Use else-if chain, handle overlap first
• Not returning 0 for n < 2 in isPrime — 0 and 1 wrongly marked prime
• Shifting insertion left→right (left to right) — overwrites values before saving them
• Forgetting to increment n after insertion — last element silently lost
• Declaring arr[5] but inserting into a full array — no space!""",
    beginner_notes="""💡 Replacement is simple: same loop as traversal, just add an if + overwrite.
💡 When two conditions can overlap, draw a truth table first.
💡 Write and test isPrime() separately before using it in the main loop.
💡 For insertion: think "make room first, then fill the gap".
💡 Insert at END is trivial: arr[n] = value; n++; — no shifting needed.
💡 Insert at BEGINNING (pos=0) shifts ALL elements — most costly."""
)

Concept.objects.create(topic=t2, title="Replace by Condition", order=1, language="c",
    explanation="The simplest array mutation: if condition true, overwrite. Array size unchanged.",
    code_snippet='for (int i = 0; i < n; i++)\n    if (arr[i] % 2 == 0) arr[i] = 0;')
Concept.objects.create(topic=t2, title="isPrime Helper", order=2, language="c",
    explanation="Trial division: test every number from 2 to n-1 as a potential divisor. If none divide evenly, the number is prime. Handle edge cases: 0 and 1 are NOT prime.",
    code_snippet='int isPrime(int n) {\n    if (n < 2) return 0;\n    for (int j = 2; j < n; j++)\n        if (n % j == 0) return 0;\n    return 1;\n}')
Concept.objects.create(topic=t2, title="Insert at Position (Shift Pattern)", order=3, language="c",
    explanation="To insert at position p: loop from i=n down to i=pos+1, set arr[i]=arr[i-1]. Then arr[pos]=value, n++.",
    code_snippet='// Insert value at pos\nfor (int i = n; i > pos; i--)\n    arr[i] = arr[i - 1];\narr[pos] = value;\nn++;')

Problem.objects.create(topic=t2, title="Replace Even Numbers with 0", order=1,
    description="Given an array, replace all even numbers with 0 and print the modified array.",
    difficulty="easy", category="guided",
    solution_code='for (int i = 0; i < n; i++)\n    if (arr[i] % 2 == 0) arr[i] = 0;',
    solution_explanation="Check arr[i] % 2 == 0. If true, set arr[i] = 0. Size unchanged.")
Problem.objects.create(topic=t2, title="Replace Primes with -1", order=2,
    description="Replace all prime numbers in the array with -1.",
    difficulty="medium", category="practice",
    hints="Write isPrime() helper first. Test it with 0, 1, 2, 13 before using in the main loop.",
    solution_code='int isPrime(int n) {\n    if (n < 2) return 0;\n    for (int j = 2; j < n; j++)\n        if (n % j == 0) return 0;\n    return 1;\n}\n// In main loop:\nfor (int i = 0; i < n; i++)\n    if (isPrime(arr[i])) arr[i] = -1;',
    solution_explanation="Separate the prime check into a helper function. Loop through array and replace where isPrime returns 1.")
Problem.objects.create(topic=t2, title="Insert at Beginning", order=3,
    description="Insert a new element at the beginning of the array (position 0).",
    difficulty="easy", category="guided",
    solution_code='// Shift all elements one position right\nfor (int i = n; i > 0; i--)\n    arr[i] = arr[i - 1];\narr[0] = newValue;\nn++;',
    solution_explanation="pos=0, so all elements shift right. Loop from n down to 1.")
Problem.objects.create(topic=t2, title="Insert at Given Position", order=4,
    description="Ask user for a value and position. Insert the value at that position in the array.",
    difficulty="easy", category="practice",
    solution_code='int pos, value;\nscanf("%d %d", &pos, &value);\nfor (int i = n; i > pos; i--)\n    arr[i] = arr[i - 1];\narr[pos] = value;\nn++;',
    solution_explanation="Shift loop from n down to pos+1. Place value at arr[pos]. Increment n.")
Problem.objects.create(topic=t2, title="Replace then Sum", order=5,
    description="Replace all multiples of 3 with 0, then compute and print the sum of the modified array.",
    difficulty="medium", category="challenge",
    hints="Can both steps be done in one pass? Yes — replace and accumulate sum simultaneously.",
    solution_code='int sum = 0;\nfor (int i = 0; i < n; i++) {\n    if (arr[i] % 3 == 0) arr[i] = 0;\n    sum += arr[i];\n}\nprintf("Sum = %d\\n", sum);',
    solution_explanation="Replace first, then add to sum — both in the same iteration. The zeros contribute 0 to the sum.")

print(f"✅ Topic 2 created with {Concept.objects.filter(topic=t2).count()} concepts and {Problem.objects.filter(topic=t2).count()} problems.")
