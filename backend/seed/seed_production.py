"""
Production seed — Creates Series + Modules + Topics + Problems + Concepts + Revision Notes.
Run: export DATABASE_URL="your_render_postgres_url" && python manage.py shell < seed/seed_production.py
"""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learntolever.settings")
django.setup()

from core.models import Series, Module, Topic, ContentBlock, Concept, Problem, RevisionNote

def seed():
    print("🌱 Seeding production database...")

    # ━━━ SERIES 1: Foundation Logic ━━━
    s1, _ = Series.objects.get_or_create(
        slug="foundation-logic-c",
        defaults=dict(
            title="Foundation Logic in C",
            description="Master the fundamentals of programming through C — from variables and loops to arrays and pattern printing.",
            icon="🧱", order=1, is_published=True,
        )
    )

    # ── Module 1: Basics ──
    m1, _ = Module.objects.get_or_create(
        slug="basics-programming-loops-patterns-c",
        defaults=dict(
            series=s1,
            title="Basics of Programming, Loops & Patterns in C",
            description="Variables, data types, conditional statements, loops, and pattern printing.",
            icon="🧱", order=1, is_published=True,
        )
    )

    t1, _ = Topic.objects.get_or_create(
        slug="what-is-programming",
        defaults=dict(
            module=m1, title="What is Programming?", order=1,
            status="published", is_published=True,
            introduction="Programming is the art of telling a computer what to do using a language it understands.",
            content_html="<p>A <strong>program</strong> is a set of instructions. Think of it like a recipe — each step must be clear and precise.</p><p>Computers are fast but literal: they do exactly what you tell them, nothing more.</p>",
            code_examples='#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    \n    // Variables store data\n    int age = 20;\n    char name[] = "Alice";\n    printf("Name: %s, Age: %d\\n", name, age);\n    \n    return 0;\n}',
            logic_explanation="1. The computer reads your code top to bottom.\n2. Each line is one instruction.\n3. printf() displays text on screen.\n4. Variables are like labeled boxes that hold values.",
            common_mistakes="• Forgetting semicolons at end of statements\n• Using = (assignment) instead of == (comparison)\n• Not matching braces {}",
            beginner_notes="💡 Don't memorize syntax — understand the logic. Syntax comes naturally with practice.",
        )
    )
    Concept.objects.get_or_create(topic=t1, title="Variables", defaults=dict(
        explanation="A variable is a named container for storing data. In C, you must declare the type.",
        code_snippet='int x = 10;\nfloat pi = 3.14;\nchar grade = \'A\';', language="c", order=1))
    Concept.objects.get_or_create(topic=t1, title="Data Types", defaults=dict(
        explanation="Every value has a type: int (whole numbers), float (decimals), char (single character), double (precise decimals).",
        code_snippet="int age = 25;       // integer\nfloat pi = 3.14;    // float\nchar grade = 'A';   // character\ndouble precise = 3.14159265;", language="c", order=2))

    t2, _ = Topic.objects.get_or_create(
        slug="input-and-output-in-c",
        defaults=dict(
            module=m1, title="Input and Output in C", order=2,
            status="published", is_published=True,
            introduction="Programs communicate by taking input and producing output using scanf and printf.",
            content_html="<p><code>scanf()</code> reads from the user. <code>printf()</code> writes to the screen.</p>",
            code_examples='#include <stdio.h>\n\nint main() {\n    int age;\n    printf("Enter your age: ");\n    scanf("%d", &age);\n    printf("Next year you will be %d\\n", age + 1);\n    return 0;\n}',
            logic_explanation="1. scanf() pauses and waits for user input.\n2. Use format specifiers: %d for int, %f for float, %c for char, %s for string.\n3. The & operator gives the address of a variable.\n4. printf() can display formatted output.",
            common_mistakes="• Forgetting & before variable in scanf()\n• Wrong format specifier (%d vs %f)\n• Buffer overflow with strings",
            beginner_notes="💡 Always test your program with different inputs to catch edge cases.",
        )
    )

    t3, _ = Topic.objects.get_or_create(
        slug="if-else-decisions-in-c",
        defaults=dict(
            module=m1, title="If-Else Decisions in C", order=3,
            status="published", is_published=True,
            introduction="Programs need to make choices — just like you decide what to wear based on weather.",
            content_html="<p>The <code>if</code> statement checks a condition. If it's <strong>true</strong>, the block runs.</p>",
            code_examples='#include <stdio.h>\n\nint main() {\n    int age;\n    printf("Enter age: ");\n    scanf("%d", &age);\n    \n    if (age >= 18) {\n        printf("You can vote!\\n");\n    } else if (age >= 13) {\n        printf("You are a teenager.\\n");\n    } else {\n        printf("You are a child.\\n");\n    }\n    return 0;\n}',
            logic_explanation="1. C checks conditions top-to-bottom.\n2. Only the FIRST true branch executes.\n3. else catches everything that didn't match.\n4. Braces {} define the code block.",
            common_mistakes="• Using = instead of == for comparison\n• Forgetting braces for multi-line blocks\n• Missing semicolons",
        )
    )

    t4, _ = Topic.objects.get_or_create(
        slug="loops-for-and-while-in-c",
        defaults=dict(
            module=m1, title="Loops — For and While in C", order=4,
            status="published", is_published=True,
            introduction="Loops let you repeat actions without writing the same code over and over.",
            content_html="<p><code>for</code> loops iterate a known number of times. <code>while</code> loops repeat until a condition is false.</p>",
            code_examples='#include <stdio.h>\n\nint main() {\n    // For loop\n    for (int i = 0; i < 5; i++) {\n        printf("Step %d\\n", i);\n    }\n    \n    // While loop\n    int count = 0;\n    while (count < 3) {\n        printf("Count is %d\\n", count);\n        count++;\n    }\n    return 0;\n}',
            logic_explanation="1. for loop: initialization; condition; update\n2. while loop: repeats as long as condition is true\n3. Always update the loop variable to avoid infinite loops!\n4. break exits a loop, continue skips to next iteration.",
            common_mistakes="• Infinite while loops (forgetting to update counter)\n• Off-by-one errors\n• Using = instead of < or <= in conditions",
        )
    )

    Problem.objects.get_or_create(topic=t1, title="Swap Two Variables", defaults=dict(
        description="Given two variables a=5 and b=10, swap their values using a temporary variable.",
        difficulty="easy", category="guided",
        solution_code="int a = 5, b = 10, temp;\ntemp = a;\na = b;\nb = temp;\nprintf(\"%d %d\", a, b); // 10 5",
        solution_explanation="Use a temp variable to hold one value during the swap.", order=1))
    Problem.objects.get_or_create(topic=t3, title="Grade Calculator", defaults=dict(
        description="Take a score (0-100) as input and print the grade: A (90+), B (80+), C (70+), D (60+), F (below 60).",
        difficulty="easy", category="guided",
        solution_code='if (score >= 90) printf("A");\nelse if (score >= 80) printf("B");\nelse if (score >= 70) printf("C");\nelse if (score >= 60) printf("D");\nelse printf("F");',
        solution_explanation="Use if-elif chain. Check from highest first.", order=1))
    Problem.objects.get_or_create(topic=t4, title="Sum of N Numbers", defaults=dict(
        description="Calculate sum of 1 to N using a for loop.",
        difficulty="easy", category="practice",
        solution_code='int n, total = 0;\nscanf("%d", &n);\nfor (int i = 1; i <= n; i++) total += i;\nprintf("Sum = %d", total);',
        solution_explanation="Loop from 1 to n inclusive, accumulating in total.", order=1))
    Problem.objects.get_or_create(topic=t4, title="Star Pattern", defaults=dict(
        description="Print a right triangle pattern of stars for n rows:\n*\n**\n***\n****",
        difficulty="medium", category="practice",
        solution_code='for (int i = 1; i <= n; i++) {\n    for (int j = 0; j < i; j++)\n        printf("*");\n    printf("\\n");\n}',
        solution_explanation="Outer loop for rows, inner loop prints i stars per row.", order=2))

    RevisionNote.objects.get_or_create(module=m1, title="Basics Recap", defaults=dict(
        summary="Variables store data with types. scanf reads, printf writes. if/else for decisions. for/while for loops.",
        key_points="• Variables = labeled boxes with types\n• 4 basic types: int, float, char, double\n• scanf() needs & for address\n• for = known count, while = unknown count",
        order=1))

    # ── Module 2: Arrays ──
    m2, _ = Module.objects.get_or_create(
        slug="array-processing-traversal-logical-operations-c",
        defaults=dict(
            series=s1,
            title="Array Processing & Logical Operations in C",
            description="Master 1D arrays — traversal, insertion, deletion, reversing, sorting, frequency counting, and combined operations.",
            icon="📊", order=2, is_published=True,
        )
    )

    t5, _ = Topic.objects.get_or_create(
        slug="array-fundamentals-and-traversal",
        defaults=dict(
            module=m2, title="Array Fundamentals and Traversal", order=1,
            status="published", is_published=True,
            introduction="An array stores multiple values of the same type in contiguous memory locations.",
            content_html="<p>Arrays are fixed-size, indexed collections. Access elements by index (starting at 0).</p>",
            code_examples='#include <stdio.h>\n\nint main() {\n    int arr[] = {10, 20, 30, 40, 50};\n    int n = sizeof(arr) / sizeof(arr[0]);\n    \n    // Forward traversal\n    for (int i = 0; i < n; i++) {\n        printf("arr[%d] = %d\\n", i, arr[i]);\n    }\n    \n    // Reverse traversal\n    for (int i = n - 1; i >= 0; i--) {\n        printf("%d ", arr[i]);\n    }\n    return 0;\n}',
            logic_explanation="1. Arrays use square brackets [].\n2. First element is index 0, last is n-1.\n3. sizeof(arr)/sizeof(arr[0]) gives array length.\n4. Traverse forward with i++ or backward with i--.",
            common_mistakes="• Index starts at 0, not 1\n• Accessing beyond array bounds (segfault)\n• Not initializing array elements",
            beginner_notes="💡 Think of an array as a numbered shelf. Each slot holds one item of the same type.",
        )
    )

    t6, _ = Topic.objects.get_or_create(
        slug="array-insertion-and-deletion",
        defaults=dict(
            module=m2, title="Array Insertion and Deletion", order=2,
            status="published", is_published=True,
            introduction="Learn how to insert elements at any position and delete elements from arrays.",
            content_html="<p>Since C arrays are fixed-size, insertion and deletion require shifting elements.</p>",
            code_examples='// Insert element at position pos\nvoid insert(int arr[], int *n, int pos, int val) {\n    for (int i = *n; i > pos; i--)\n        arr[i] = arr[i-1];\n    arr[pos] = val;\n    (*n)++;\n}\n\n// Delete element at position pos\nvoid delete(int arr[], int *n, int pos) {\n    for (int i = pos; i < *n - 1; i++)\n        arr[i] = arr[i+1];\n    (*n)--;\n}',
            logic_explanation="1. To INSERT: shift elements right from the end, then place new value.\n2. To DELETE: shift elements left from the position, then decrease size.\n3. Always track actual array size separately.\n4. Ensure array has enough capacity before inserting.",
            common_mistakes="• Forgetting to update the size variable\n• Shifting in wrong direction\n• Buffer overflow on insert",
        )
    )

    t7, _ = Topic.objects.get_or_create(
        slug="array-sorting-and-searching",
        defaults=dict(
            module=m2, title="Sorting and Searching in Arrays", order=3,
            status="published", is_published=True,
            introduction="Learn how to organize and find data efficiently in arrays.",
            content_html="<p>Bubble sort is the simplest sorting algorithm. Linear search checks each element one by one.</p>",
            code_examples='// Bubble Sort\nvoid bubbleSort(int arr[], int n) {\n    for (int i = 0; i < n-1; i++)\n        for (int j = 0; j < n-i-1; j++)\n            if (arr[j] > arr[j+1]) {\n                int temp = arr[j];\n                arr[j] = arr[j+1];\n                arr[j+1] = temp;\n            }\n}\n\n// Linear Search\nint linearSearch(int arr[], int n, int key) {\n    for (int i = 0; i < n; i++)\n        if (arr[i] == key) return i;\n    return -1;\n}',
            logic_explanation="1. Bubble sort: compare adjacent, swap if out of order. Repeat.\n2. Each pass pushes the largest unsorted element to its position.\n3. Linear search: check each element sequentially.\n4. Returns index if found, -1 if not.",
            common_mistakes="• Off-by-one in loop bounds\n• Not using temp for swap\n• Forgetting to return -1 for not found",
        )
    )

    t8, _ = Topic.objects.get_or_create(
        slug="array-frequency-and-duplicates",
        defaults=dict(
            module=m2, title="Frequency Counting & Duplicate Detection", order=4,
            status="published", is_published=True,
            introduction="Count occurrences, find unique elements, and detect duplicates in arrays.",
            content_html="<p>Frequency counting tracks how many times each element appears. This is the basis for many array algorithms.</p>",
            code_examples='// Count frequency of each element\nvoid frequency(int arr[], int n) {\n    int visited[100] = {0}; // assume values 0-99\n    for (int i = 0; i < n; i++) {\n        if (!visited[i]) {\n            int count = 1;\n            for (int j = i+1; j < n; j++)\n                if (arr[i] == arr[j]) {\n                    count++;\n                    visited[j] = 1;\n                }\n            printf("%d appears %d times\\n", arr[i], count);\n        }\n    }\n}',
            logic_explanation="1. Use a visited/flag array to mark counted elements.\n2. For each unvisited element, count matches in the rest.\n3. Mark duplicates as visited to avoid double-counting.\n4. Time complexity: O(n²) for this approach.",
            common_mistakes="• Not marking visited elements\n• Counting the same element multiple times\n• Array bounds for the visited array",
        )
    )

    Problem.objects.get_or_create(topic=t5, title="Find Maximum in Array", defaults=dict(
        description="Given an array of numbers, find the maximum without using any library function.",
        difficulty="easy", category="guided",
        solution_code="int max = arr[0];\nfor (int i = 1; i < n; i++)\n    if (arr[i] > max) max = arr[i];\nprintf(\"Max = %d\", max);",
        solution_explanation="Start with first element as max. Compare each element and update if larger.", order=1))
    Problem.objects.get_or_create(topic=t5, title="Reverse an Array", defaults=dict(
        description="Reverse an array in-place without using a second array.",
        difficulty="medium", category="practice",
        solution_code="for (int i = 0; i < n/2; i++) {\n    int temp = arr[i];\n    arr[i] = arr[n-1-i];\n    arr[n-1-i] = temp;\n}",
        solution_explanation="Swap elements from both ends moving towards center.", order=2))
    Problem.objects.get_or_create(topic=t7, title="Second Largest Element", defaults=dict(
        description="Find the second largest element in an array in a single pass.",
        difficulty="medium", category="challenge",
        solution_code="int first = INT_MIN, second = INT_MIN;\nfor (int i = 0; i < n; i++) {\n    if (arr[i] > first) { second = first; first = arr[i]; }\n    else if (arr[i] > second && arr[i] != first) second = arr[i];\n}",
        solution_explanation="Track both first and second largest. Update carefully on each comparison.", order=1))

    RevisionNote.objects.get_or_create(module=m2, title="Arrays Recap", defaults=dict(
        summary="Arrays are fixed-size indexed collections. Index from 0 to n-1. Insert/delete requires shifting. Bubble sort for simple sorting.",
        key_points="• Arrays: fixed-size, same type, indexed from 0\n• sizeof(arr)/sizeof(arr[0]) for length\n• Insert = shift right, Delete = shift left\n• Bubble sort: O(n²), Linear search: O(n)",
        order=1))

    # ━━━ SERIES 2: OOPs by Java ━━━
    s2, _ = Series.objects.get_or_create(
        slug="oops-by-java",
        defaults=dict(
            title="OOPs by Java",
            description="Understand Object-Oriented Programming through Java — classes, objects, inheritance, polymorphism, abstraction, and encapsulation.",
            icon="☕", order=2, is_published=True,
        )
    )

    m3, _ = Module.objects.get_or_create(
        slug="java-oop-fundamentals",
        defaults=dict(
            series=s2,
            title="Java OOP Fundamentals",
            description="Classes, objects, constructors, methods, and the foundations of object-oriented thinking.",
            icon="☕", order=1, is_published=True,
        )
    )

    Topic.objects.get_or_create(
        slug="classes-and-objects-in-java",
        defaults=dict(
            module=m3, title="Classes and Objects in Java", order=1,
            status="published", is_published=True,
            introduction="A class is a blueprint, an object is an instance of that blueprint.",
            content_html="<p>In Java, everything lives inside a class. Objects are created from classes using the <code>new</code> keyword.</p>",
            code_examples='class Student {\n    String name;\n    int age;\n    \n    void display() {\n        System.out.println(name + " is " + age + " years old.");\n    }\n}\n\npublic class Main {\n    public static void main(String[] args) {\n        Student s1 = new Student();\n        s1.name = "Alice";\n        s1.age = 20;\n        s1.display();\n    }\n}',
            logic_explanation="1. A class defines properties (fields) and behaviors (methods).\n2. new creates an object in memory.\n3. Use dot notation to access fields and methods.\n4. Each object has its own copy of instance variables.",
            common_mistakes="• Forgetting the new keyword\n• Confusing class with object\n• Not initializing fields before use",
        )
    )

    # Print summary
    print(f"✅ Seeded successfully!")
    print(f"   Series: {Series.objects.count()}")
    print(f"   Modules: {Module.objects.count()}")
    print(f"   Topics: {Topic.objects.count()}")
    print(f"   Concepts: {Concept.objects.count()}")
    print(f"   Problems: {Problem.objects.count()}")
    print(f"   Revision Notes: {RevisionNote.objects.count()}")

seed()
