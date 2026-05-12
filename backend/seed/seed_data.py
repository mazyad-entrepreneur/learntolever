"""
Seed script — populates the database with 4 foundation modules.

Run:  python manage.py shell < seed/seed_data.py
"""

import os, sys, django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learntolever.settings")
django.setup()

from core.models import Module, Topic, Concept, Problem, RevisionNote

# ── Helper ──
def seed():
    # Clear old data
    Module.objects.all().delete()

    # ━━━ MODULE 1: Basics of Programming ━━━
    m1 = Module.objects.create(
        title="Basics of Programming",
        description="Learn the fundamental building blocks — variables, data types, input/output, and your first programs.",
        icon="🧱",
        order=1,
        is_published=True,
    )

    t1 = Topic.objects.create(
        module=m1, title="What is Programming?", order=1, is_published=True,
        introduction="Programming is the art of telling a computer what to do using a language it understands.",
        content_html="<p>A <strong>program</strong> is a set of instructions. Think of it like a recipe — each step must be clear and precise.</p><p>Computers are fast but literal: they do exactly what you tell them, nothing more.</p>",
        code_examples='# Your very first program\nprint("Hello, World!")\n\n# Variables store data\nname = "Alice"\nage = 20\nprint(f"My name is {name} and I am {age} years old.")',
        logic_explanation="1. The computer reads your code top to bottom.\n2. Each line is one instruction.\n3. `print()` displays text on screen.\n4. Variables are like labeled boxes that hold values.",
        common_mistakes="• Forgetting quotes around text strings\n• Using = (assignment) instead of == (comparison)\n• Not matching parentheses",
        beginner_notes="💡 Don't memorize syntax — understand the logic. Syntax comes naturally with practice.",
    )
    Concept.objects.create(topic=t1, title="Variables", explanation="A variable is a named container for storing data. Think of it as a labeled box.", code_snippet='x = 10\nname = "Bob"', language="python", order=1)
    Concept.objects.create(topic=t1, title="Data Types", explanation="Every value has a type: integers (whole numbers), floats (decimals), strings (text), booleans (True/False).", code_snippet="age = 25        # int\npi = 3.14       # float\nname = 'Alice'  # str\nis_student = True  # bool", language="python", order=2)

    t2 = Topic.objects.create(
        module=m1, title="Input and Output", order=2, is_published=True,
        introduction="Programs communicate by taking input and producing output.",
        content_html="<p><code>input()</code> reads from the user. <code>print()</code> writes to the screen.</p>",
        code_examples='name = input("What is your name? ")\nprint(f"Hello, {name}!")\n\n# Converting input to number\nage = int(input("Enter your age: "))\nprint(f"Next year you will be {age + 1}")',
        logic_explanation="1. `input()` pauses the program and waits for the user.\n2. Input is always a string — convert it with `int()` or `float()` for math.\n3. `print()` can display multiple values.",
        common_mistakes="• Forgetting to convert input to int for calculations\n• Missing the prompt message in input()",
        beginner_notes="💡 Always test your program with different inputs to catch edge cases.",
    )

    Problem.objects.create(topic=t1, title="Swap Two Variables", description="Given two variables a=5 and b=10, swap their values without using a third variable.", difficulty="easy", category="guided", solution_code="a = 5\nb = 10\na, b = b, a\nprint(a, b)  # 10 5", solution_explanation="Python allows tuple unpacking to swap in one line.", order=1)
    Problem.objects.create(topic=t2, title="Temperature Converter", description="Ask the user for a temperature in Celsius and convert it to Fahrenheit.", difficulty="easy", category="practice", solution_code='c = float(input("Enter Celsius: "))\nf = (c * 9/5) + 32\nprint(f"{c}°C = {f}°F")', solution_explanation="Formula: F = C × 9/5 + 32. Remember to convert input to float.", order=1)

    RevisionNote.objects.create(module=m1, title="Basics Recap", summary="Variables store data. Data types define what kind of data. Input reads, print writes. Always convert input types for math.", key_points="• Variables = labeled boxes\n• 4 basic types: int, float, str, bool\n• input() → always string\n• print() → displays output", order=1)

    # ━━━ MODULE 2: Control Flow ━━━
    m2 = Module.objects.create(
        title="Control Flow",
        description="Master if-else decisions, loops, and program flow to write smart, responsive programs.",
        icon="🔀",
        order=2,
        is_published=True,
    )

    t3 = Topic.objects.create(
        module=m2, title="If-Else Decisions", order=1, is_published=True,
        introduction="Programs need to make choices — just like you decide what to wear based on weather.",
        content_html="<p>The <code>if</code> statement checks a condition. If it's <strong>True</strong>, the indented block runs.</p>",
        code_examples='age = int(input("Enter age: "))\n\nif age >= 18:\n    print("You can vote!")\nelif age >= 13:\n    print("You are a teenager.")\nelse:\n    print("You are a child.")',
        logic_explanation="1. Python checks conditions top-to-bottom.\n2. Only the FIRST true branch executes.\n3. `else` catches everything that didn't match.\n4. Indentation defines the code block.",
        common_mistakes="• Wrong indentation (Python is strict!)\n• Using = instead of ==\n• Forgetting the colon after conditions",
        beginner_notes="💡 Draw a flowchart before coding. It makes the logic visual.",
    )

    t4 = Topic.objects.create(
        module=m2, title="Loops — For and While", order=2, is_published=True,
        introduction="Loops let you repeat actions without writing the same code over and over.",
        content_html="<p><code>for</code> loops iterate over sequences. <code>while</code> loops repeat until a condition is false.</p>",
        code_examples='# For loop\nfor i in range(5):\n    print(f"Step {i}")\n\n# While loop\ncount = 0\nwhile count < 3:\n    print(f"Count is {count}")\n    count += 1',
        logic_explanation="1. `for` loop: knows how many times to repeat.\n2. `while` loop: repeats as long as condition is True.\n3. `range(5)` gives numbers 0, 1, 2, 3, 4.\n4. Always update the while condition to avoid infinite loops!",
        common_mistakes="• Infinite while loops (forgetting to update counter)\n• Off-by-one errors with range()\n• Modifying a list while looping over it",
        beginner_notes="💡 Use `for` when you know the count. Use `while` when you don't.",
    )

    Problem.objects.create(topic=t3, title="Grade Calculator", description="Take a score (0-100) as input and print the grade: A (90+), B (80+), C (70+), D (60+), F (below 60).", difficulty="easy", category="guided", solution_code='score = int(input("Enter score: "))\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelif score >= 70:\n    print("C")\nelif score >= 60:\n    print("D")\nelse:\n    print("F")', solution_explanation="Use elif chain. Check from highest first so each condition catches the right range.", order=1)
    Problem.objects.create(topic=t4, title="Sum of N Numbers", description="Ask user for N, then calculate sum of 1 to N using a loop.", difficulty="easy", category="practice", solution_code='n = int(input("Enter N: "))\ntotal = 0\nfor i in range(1, n + 1):\n    total += i\nprint(f"Sum = {total}")', solution_explanation="range(1, n+1) gives 1 to n inclusive. Accumulate in total variable.", order=1)

    RevisionNote.objects.create(module=m2, title="Control Flow Recap", summary="if/elif/else for decisions. for loops for known iterations. while loops for condition-based repetition.", key_points="• if checks conditions top-down\n• Only first True branch runs\n• for = known count, while = unknown count\n• Always avoid infinite loops", order=1)

    # ━━━ MODULE 3: Arrays (Lists) ━━━
    m3 = Module.objects.create(
        title="Arrays and Lists",
        description="Store and manipulate collections of data — searching, sorting, filtering, and transforming.",
        icon="📊",
        order=3,
        is_published=True,
    )

    t5 = Topic.objects.create(
        module=m3, title="Array Fundamentals and Traversal", order=1, is_published=True,
        introduction="An array (list in Python) stores multiple values in a single variable.",
        content_html="<p>Lists are ordered, mutable collections. Access elements by index (starting at 0).</p>",
        code_examples='fruits = ["apple", "banana", "cherry"]\n\n# Access by index\nprint(fruits[0])  # apple\n\n# Traverse with for loop\nfor fruit in fruits:\n    print(fruit)\n\n# Traverse with index\nfor i in range(len(fruits)):\n    print(f"Index {i}: {fruits[i]}")',
        logic_explanation="1. Lists use square brackets [].\n2. First element is index 0.\n3. len() gives the number of elements.\n4. You can loop by value or by index.",
        common_mistakes="• Index starts at 0, not 1\n• IndexError: accessing beyond list length\n• Confusing append() with extend()",
        beginner_notes="💡 Think of a list as a numbered shelf. Each slot holds one item.",
    )

    t6 = Topic.objects.create(
        module=m3, title="Sorting and Searching", order=2, is_published=True,
        introduction="Learn how to organize and find data efficiently in lists.",
        content_html="<p>Python provides built-in sorting. Understanding the logic behind it builds problem-solving skills.</p>",
        code_examples='numbers = [64, 34, 25, 12, 22, 11, 90]\n\n# Built-in sort\nnumbers.sort()\nprint(numbers)  # [11, 12, 22, 25, 34, 64, 90]\n\n# Linear search\ndef find(arr, target):\n    for i, val in enumerate(arr):\n        if val == target:\n            return i\n    return -1\n\nprint(find(numbers, 25))  # 2',
        logic_explanation="1. .sort() modifies the list in place.\n2. sorted() returns a new sorted list.\n3. Linear search checks each element one by one.\n4. Binary search is faster but needs a sorted list.",
        common_mistakes="• Using sort() on mixed types (int + str)\n• Forgetting sort() returns None\n• Off-by-one in manual search",
        beginner_notes="💡 Master linear search first. Binary search builds on it.",
    )

    Problem.objects.create(topic=t5, title="Find Maximum", description="Given a list of numbers, find the maximum without using the built-in max() function.", difficulty="easy", category="guided", solution_code="nums = [3, 7, 2, 9, 1]\nmax_val = nums[0]\nfor n in nums:\n    if n > max_val:\n        max_val = n\nprint(max_val)  # 9", solution_explanation="Start with first element as max. Compare each element and update if larger.", order=1)
    Problem.objects.create(topic=t5, title="Reverse a List", description="Reverse a list without using the built-in reverse() method or slicing.", difficulty="medium", category="practice", solution_code="nums = [1, 2, 3, 4, 5]\nfor i in range(len(nums) // 2):\n    nums[i], nums[-(i+1)] = nums[-(i+1)], nums[i]\nprint(nums)", solution_explanation="Swap elements from both ends moving towards the center.", order=2)

    RevisionNote.objects.create(module=m3, title="Arrays Recap", summary="Lists store ordered collections. Index from 0. Traverse with for loops. sort() and sorted() for ordering.", key_points="• Lists: ordered, mutable, indexed from 0\n• len() for size, append() to add\n• Linear search: O(n)\n• sort() modifies in-place, sorted() returns new", order=1)

    # ━━━ MODULE 4: Functions ━━━
    m4 = Module.objects.create(
        title="Functions",
        description="Break complex problems into reusable, testable pieces with functions.",
        icon="⚙️",
        order=4,
        is_published=True,
    )

    t7 = Topic.objects.create(
        module=m4, title="Defining and Calling Functions", order=1, is_published=True,
        introduction="Functions let you write code once and reuse it anywhere.",
        content_html="<p>A function is a named block of code that performs a specific task. Use <code>def</code> to define one.</p>",
        code_examples='def greet(name):\n    """Say hello to someone."""\n    return f"Hello, {name}!"\n\n# Call the function\nmessage = greet("Alice")\nprint(message)  # Hello, Alice!\n\n# Function with default parameter\ndef power(base, exp=2):\n    return base ** exp\n\nprint(power(3))     # 9\nprint(power(3, 3))  # 27',
        logic_explanation="1. `def` keyword starts a function definition.\n2. Parameters go inside parentheses.\n3. `return` sends a value back to the caller.\n4. A function without return gives None.",
        common_mistakes="• Forgetting return (function returns None)\n• Calling a function before defining it\n• Mutable default arguments (use None instead of [])",
        beginner_notes="💡 If you write the same code twice, make it a function!",
    )

    t8 = Topic.objects.create(
        module=m4, title="Scope and Recursion", order=2, is_published=True,
        introduction="Understand where variables live and how functions can call themselves.",
        content_html="<p><strong>Scope</strong> determines where a variable is accessible. <strong>Recursion</strong> is when a function calls itself.</p>",
        code_examples='# Scope example\nx = "global"\n\ndef my_func():\n    x = "local"\n    print(x)  # local\n\nmy_func()\nprint(x)  # global\n\n# Recursion: factorial\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))  # 120',
        logic_explanation="1. Variables inside a function are LOCAL.\n2. Global variables are accessible everywhere but shouldn't be modified inside functions.\n3. Recursion needs a BASE CASE to stop.\n4. Each recursive call adds to the call stack.",
        common_mistakes="• Infinite recursion (missing base case)\n• Modifying global variables accidentally\n• Stack overflow from deep recursion",
        beginner_notes="💡 Recursion is elegant but loops are often simpler. Use recursion when the problem is naturally recursive (trees, factorials).",
    )

    Problem.objects.create(topic=t7, title="Calculator Function", description="Create a function calc(a, b, op) that takes two numbers and an operation (+, -, *, /) and returns the result.", difficulty="easy", category="guided", solution_code='def calc(a, b, op):\n    if op == "+":\n        return a + b\n    elif op == "-":\n        return a - b\n    elif op == "*":\n        return a * b\n    elif op == "/":\n        return a / b if b != 0 else "Error: division by zero"\n\nprint(calc(10, 3, "+"))  # 13', solution_explanation="Use if-elif to match the operator. Handle division by zero!", order=1)
    Problem.objects.create(topic=t8, title="Fibonacci Recursive", description="Write a recursive function to return the nth Fibonacci number.", difficulty="medium", category="practice", solution_code="def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)\n\nfor i in range(10):\n    print(fib(i), end=' ')  # 0 1 1 2 3 5 8 13 21 34", solution_explanation="Base cases: fib(0)=0, fib(1)=1. Each call branches into two smaller calls.", order=1)

    RevisionNote.objects.create(module=m4, title="Functions Recap", summary="Functions encapsulate reusable logic. Parameters pass data in, return sends data out. Scope controls variable visibility.", key_points="• def to define, return to send back\n• Parameters vs arguments\n• Local scope inside function\n• Recursion needs a base case", order=1)

    print(f"✅ Seeded {Module.objects.count()} modules, {Topic.objects.count()} topics, {Concept.objects.count()} concepts, {Problem.objects.count()} problems, {RevisionNote.objects.count()} revision notes.")

seed()
