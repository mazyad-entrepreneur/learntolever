import os,sys,django
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","learntolever.settings")
django.setup()
from core.models import Module,Topic,Concept,Problem

m2=Module.objects.get(slug="array-processing-traversal-logical-operations-c")

# ── Topic 2: Conditional Replace & Insertion ──
# Covers handbook sections 3 (Conditional Replace) + 4 (Insertion)
t2=Topic.objects.create(
    module=m2, title="Conditional Replacement and Insertion", slug="conditional-replace-insertion",
    order=2, is_published=True,
    introduction="Replacing means traversing the array, checking a condition at each element, and overwriting the value if the condition is true. The array size stays the same. Insertion means shifting elements to make room for a new value at a specific position.",
    content_html="""<h3>Replacement — Core Idea</h3>
<p>Traverse the array. At each element, check a condition. If true, <strong>overwrite that element</strong> with the new value. The array size stays the same — you are not removing or adding, just changing values.</p>

<h3>Core Conditions to Know Cold</h3>
<table><thead><tr><th>Condition</th><th>Check in C</th><th>Example: 12</th><th>Example: 15</th></tr></thead>
<tbody>
<tr><td>Even number</td><td><code>arr[i] % 2 == 0</code></td><td>✓ true</td><td>✗ false</td></tr>
<tr><td>Odd number</td><td><code>arr[i] % 2 != 0</code></td><td>✗ false</td><td>✓ true</td></tr>
<tr><td>Multiple of 3</td><td><code>arr[i] % 3 == 0</code></td><td>✓ true</td><td>✓ true</td></tr>
<tr><td>Multiple of 5</td><td><code>arr[i] % 5 == 0</code></td><td>✗ false</td><td>✓ true</td></tr>
<tr><td>Multiple of k</td><td><code>arr[i] % k == 0</code></td><td colspan="2">generalized</td></tr>
</tbody></table>

<h3>⚠️ Priority When TWO Conditions Overlap</h3>
<p>When a problem says "replace multiples of 3 with 0 AND multiples of 5 with 1, and if both then use 1" — you must handle the <strong>overlapping case (both conditions true) first</strong>, or use else-if so only one replacement applies.</p>
<table>
<tr><td>✗ WRONG</td><td>Two separate <code>if</code> statements — second if might overwrite the first replacement!</td></tr>
<tr><td>✓ CORRECT</td><td>Handle overlap first with <code>if / else-if</code> chain</td></tr>
</table>

<hr>
<h3>How to Check for a Prime Number</h3>
<p><strong>Mental Model — Trial Division:</strong> A number is prime if <strong>no number from 2 to n-1 divides it evenly</strong>. You test each divisor one by one. The moment you find one that works, it's not prime. If you test all and none work, it's prime.</p>
<p>Special cases: <strong>0 and 1 are NOT prime. 2 is prime (smallest). Negative numbers are not prime.</strong></p>
<p>Trace for n=13 (prime): tests j=2,3,4,...,12. None divide 13. Returns 1 (prime).<br>
Trace for n=12 (not prime): tests j=2. 12%2=0. Returns 0 immediately.</p>

<hr>
<h3>Insertion — Core Idea</h3>
<p>An array has fixed memory. To insert at position <strong>p</strong>, you must <strong>shift all elements from position p onwards one step to the right</strong> to make room, then place the new value at position p. The size increases by 1.</p>
<p><strong>Critical requirement:</strong> Your array must be declared with extra capacity (e.g. <code>int arr[10]</code> but only 5 elements used) to accommodate the new element.</p>

<h3>Mental Model: Inserting in a Line of People</h3>
<p>Imagine 5 people standing in positions 0-4. Someone new wants to join at position 2. Everyone from position 2 onwards must <strong>step one place to the right</strong> first, creating a gap at position 2. Then the new person fills that gap.</p>

<h3>⚠️ The Shift Direction Matters Critically</h3>
<table>
<tr><td>✗ WRONG</td><td><strong>Shifting left→right:</strong> <code>for(i=pos; i&lt;n; i++) arr[i+1]=arr[i]</code> — This overwrites values! When you copy arr[2] to arr[3], then try to copy arr[3] to arr[4], you're copying the already-overwritten value.</td></tr>
<tr><td>✓ CORRECT</td><td><strong>Shifting right→left:</strong> <code>for(i=n; i&gt;pos; i--) arr[i]=arr[i-1]</code> — You move the last element first, then second-last, working backwards to the insertion point. Nothing gets overwritten.</td></tr>
</table>

<h3>Dry Run: Insert 99 at pos=2, n=5</h3>
<table><thead><tr><th>i</th><th>condition (i &gt; 2)</th><th>action</th><th>arr state</th></tr></thead>
<tbody>
<tr><td><strong>5</strong></td><td>✓</td><td>arr[5] = arr[4] = 50</td><td>{10,20,30,40,50,50}</td></tr>
<tr><td><strong>4</strong></td><td>✓</td><td>arr[4] = arr[3] = 40</td><td>{10,20,30,40,40,50}</td></tr>
<tr><td><strong>3</strong></td><td>✓</td><td>arr[3] = arr[2] = 30</td><td>{10,20,30,30,40,50}</td></tr>
<tr><td>2</td><td>✗ stop</td><td>—</td><td>gap at index 2</td></tr>
<tr><td colspan="2">arr[2] = 99</td><td colspan="2"><strong>{10,20,99,30,40,50}</strong> ✓</td></tr>
</tbody></table>

<h3>Special Cases</h3>
<table><thead><tr><th>Case</th><th>Code</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Insert at END</td><td><code>arr[n] = value; n++;</code></td><td>No shifting needed — just place at position n.</td></tr>
<tr><td>Insert at BEGINNING</td><td>pos = 0, use shift loop</td><td>Most expensive — moves every element.</td></tr>
</tbody></table>

<hr>
<h3>🔴 Think Before Coding — Assignments</h3>
<ul>
<li><strong>2.1–2.7 (Replace by condition):</strong> Identify the trigger condition (even? odd? multiple of k? prime?). What is the replacement value (0? -1? 1?)?</li>
<li><strong>2.8, 2.10 (Two conditions):</strong> Which takes priority? Draw a truth table: what happens when both conditions are true simultaneously?</li>
<li><strong>2.9, 2.10 (Prime):</strong> You need a helper function. Write isPrime() first and test it on isPrime(0)=0, isPrime(1)=0, isPrime(2)=1 before using it in your main loop.</li>
<li><strong>2.11, 2.12 (Replace then sum):</strong> The replacement changes the array first. Then traverse again for sum. Or can you do it in one pass? Think carefully.</li>
<li><strong>2.13 (Replace then count zeros):</strong> After replacing odd numbers with 0, how do you count zeros? New traversal, or track during replacement?</li>
<li><strong>Insert at beginning (pos=0):</strong> Before writing to arr[0], what must happen to ALL existing elements?</li>
<li><strong>Insert at end:</strong> If array has n elements, what's the index after the last? Is shifting needed?</li>
<li><strong>Insert at position:</strong> Shift from end backwards. Loop starts at i=n, goes down to i=pos+1. After loop, write to arr[pos].</li>
</ul>""",
    code_examples="""// Pattern: Replace all even numbers with 0
for (int i = 0; i < n; i++) {
    if (arr[i] % 2 == 0) {     // condition
        arr[i] = 0;             // replace
    }
}
// arr changes from {12,7,18,9,24,11} to {0,7,0,9,0,11}

// WRONG: might apply both replacements
if (arr[i] % 3 == 0) arr[i] = 0;
if (arr[i] % 5 == 0) arr[i] = 1;  // might overwrite the 0!

// CORRECT: handle overlap first with else-if
if (arr[i] % 3 == 0 && arr[i] % 5 == 0) arr[i] = 1;
else if (arr[i] % 3 == 0) arr[i] = 0;
else if (arr[i] % 5 == 0) arr[i] = 1;

// isPrime helper function pattern
int isPrime(int n) {
    if (n < 2) return 0;            // 0 and 1 are not prime
    for (int j = 2; j < n; j++) {   // test all divisors 2..n-1
        if (n % j == 0) return 0;   // found a divisor: not prime
    }
    return 1;                        // no divisor found: prime
}

// Insert value 99 at position pos=2
// Before: {10, 20, 30, 40, 50}, n=5
for (int i = n; i > pos; i--) {  // shift rightward, start from end
    arr[i] = arr[i - 1];
}
arr[pos] = 99;                   // place new element
n++;                             // update size
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
4. Array must have extra capacity declared.

Special cases:
- Insert at END: arr[n] = value; n++; (no shifting)
- Insert at BEGINNING: pos=0, shifts ALL elements (most expensive)""",
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
    explanation="The simplest array mutation: traverse, check condition, overwrite if true. Array size unchanged. When two conditions can overlap, use else-if chain and handle overlap case first.",
    code_snippet='for (int i = 0; i < n; i++)\n    if (arr[i] % 2 == 0) arr[i] = 0;\n\n// For two conditions with overlap:\nif (arr[i]%3==0 && arr[i]%5==0) arr[i] = 1;\nelse if (arr[i]%3==0) arr[i] = 0;\nelse if (arr[i]%5==0) arr[i] = 1;')
Concept.objects.create(topic=t2, title="isPrime Helper", order=2, language="c",
    explanation="Trial division: test every number from 2 to n-1 as a potential divisor. If none divide evenly, the number is prime. Handle edge cases: 0 and 1 are NOT prime. 2 is prime (smallest).",
    code_snippet='int isPrime(int n) {\n    if (n < 2) return 0;\n    for (int j = 2; j < n; j++)\n        if (n % j == 0) return 0;\n    return 1;\n}')
Concept.objects.create(topic=t2, title="Insert at Position (Shift Pattern)", order=3, language="c",
    explanation="To insert at position p: loop from i=n down to i=pos+1, set arr[i]=arr[i-1]. Then arr[pos]=value, n++. Always shift right→left (from end toward insertion point). Never shift left→right — it overwrites data!",
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
