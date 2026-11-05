# Alpha-Beta Pruning — How I Would Actually Write This Code

> This document is NOT a top-to-bottom code explanation.  
> It simulates **how a real developer thinks** while building this program from scratch — the false starts, the "wait I also need", the gradual discovery of what's needed. Read it like a developer's internal monologue.

---

## Stage 1: Understanding What I'm Building (Before Writing a Single Line)

### What problem am I solving?

Before I write a single character of code, I need to understand what I'm actually building. Let me think about this properly.

I'm building an **AI game-tree search algorithm** — specifically **Alpha-Beta Pruning**, which is an optimization over the classic **Minimax** algorithm.

**The scenario:** Imagine a two-player game (like chess, tic-tac-toe, etc.). There's a **MAX player** (trying to maximize their score) and a **MIN player** (trying to minimize MAX's score). The game tree represents all possible moves. At the bottom of the tree (the leaves) are scores — positive means good for MAX, negative or low means bad.

### Let me draw this out with a concrete example

Say I have a game tree with depth = 2 and 4 leaf values: `[3, 5, 2, 9]`

```
         A (MAX)          ← Root: MAX wants the highest value
        /       \
    B (MIN)    C (MIN)    ← Depth 1: MIN wants the lowest value
    /   \      /   \
   D     E    F     G     ← Depth 0: Leaves (actual scores)
   3     5    2     9
```

### What does pure Minimax do?

Minimax exhaustively evaluates **every single leaf**:

- Node B (MIN) sees children D=3 and E=5 → picks MIN → **B = 3**
- Node C (MIN) sees children F=2 and G=9 → picks MIN → **C = 2**
- Node A (MAX) sees children B=3 and C=2 → picks MAX → **A = 3**

Minimax visits all 4 leaves. That's fine for small trees, but for a tree with depth 10, there could be **2^10 = 1024 leaves**. At depth 20? Over a million. This gets expensive fast.

### What does Alpha-Beta do differently?

Alpha-Beta prunes **branches that can't possibly affect the result**. Watch this:

```
         A (MAX, α=-∞, β=+∞)
        /       \
    B (MIN)    C (MIN)
    /   \      /   \
   D     E    F     G
   3     5    2     9
```

**Step 1:** Call alphaBeta(A). A is MAX. Start: alpha = -∞, beta = +∞

**Step 2:** Recurse into B (MIN). B evaluates D=3. Now B's best = 3. Update beta = min(beta, 3) = 3.  
Back at A: alpha = max(-∞, 3) = 3.

**Step 3:** Recurse into C (MIN). C evaluates F=2. Now C's best = 2. Update beta = min(+∞, 2) = 2.  
**Now check: alpha(3) >= beta(2)?  YES! → PRUNE G!**

We never need to look at G=9. Why? Because C will return at most 2 (it already found 2, and MIN will only go lower). But A already has 3 from B. A (MAX) will never choose C over B. So G is irrelevant.

**Final result:** Optimal value = 3

### What output do I want from this program?

Let me define exactly what my program should produce:

**Input:**
```
Enter depth: 2
Enter 4 values:
3 5 2 9
```

**Output:**
```
Game Tree:
Root A (max) : 3
|-- B(min): 3
|   |-- D : 3 (leaf)
|   '-- E : 5 (leaf)
'-- C(min): 2
    |-- F : 2 (leaf)
    '-- G (pruned)

Optimal Value: 3

Optimal Path:
A -> B -> D
```

Now I know what I'm building. Let me start writing code.

---

## Stage 2: Planning the Data Structure — "I Need a Node"

### Thinking it through

"Okay, I need to represent a game tree. The fundamental building block is a **Node**. Let me think about what each node must *know* in order for my algorithm to work."

Let me list everything a node needs:

1. **`depth`** — I need to know if this is a leaf node. A leaf has depth = 0. This drives the base case of my recursion.

2. **`value`** — This is the minimax value of the node. For leaves, I set it directly from input. For internal nodes, it gets computed by alpha-beta. I need it stored so I can display it and trace the path later.

3. **`isMax`** — Is this a MAX node or a MIN node? This determines whether I take max or min of children. I need to know this at every node.

4. **`pruned`** — Did this node get pruned? If yes, I should display it differently in the tree and NOT recurse into it during display or path tracing.

5. **`left`, `right`** — The two children. This is a binary tree (each internal node has exactly 2 children).

6. **`name`** — A letter (A, B, C...) to identify the node in the display. This makes the tree readable.

### Writing the Node class — fields first

Let me write the fields first. I'll worry about the constructor in a second.

```java
static class Node {
    int depth, value;
    boolean isMax, pruned = false;
    Node left, right;
    char name;
}
```

Wait — why `static class`? Because my outer class `practice` doesn't have an instance. Everything is static. An inner non-static class would need an instance of the outer class to exist. Since all my methods are static, I need `static class Node` so I can use it from static contexts.

Notice I'm defaulting `pruned = false` right in the declaration. That's intentional — every node starts as NOT pruned. Only alpha-beta can mark a node pruned.

### Now the constructor

"What do I need to provide when creating a node? Let me think..."

- `depth` — I know this at creation time (I start at the root depth and decrement)
- `isMax` — I know this at creation time (root is MAX, alternates going down)
- `value` — I don't know this yet. Leaves get it from input. Internal nodes get it from alpha-beta. So I'll leave it uninitialized.
- `left`, `right` — These get assigned recursively after creation. Don't need them in constructor.
- `name` — I'll assign from a global counter right after creation. Don't need it in constructor.
- `pruned` — Already defaulted to false.

So the constructor only needs `depth` and `isMax`:

```java
Node(int depth, boolean isMax) {
    this.depth = depth;
    this.isMax = isMax;
}
```

### The complete Node class

```java
static class Node {
    int depth, value;
    boolean isMax, pruned = false;
    Node left, right;
    char name;

    Node(int depth, boolean isMax) {
        this.depth = depth;
        this.isMax = isMax;
    }
}
```

This is complete for now. I'll come back to it if I realize I need more.

### Wait — I need to name nodes A, B, C...

"How do I assign names A, B, C... to nodes as I create them?"

I need a **global counter** that increments each time I create a node. In Java, I can use a `static` class-level variable:

```java
static char counter = 'A';
```

Then when building a node:
```java
node.name = counter++;
```

The `counter++` uses the current value and then increments. So the first node gets 'A', next gets 'B', etc.

**But wait** — I need to be careful. What if the user runs the program multiple times (or what if I call buildTree again)? I'll need to **reset counter to 'A'** before each run. I'll handle that in `main()`.

---

## Stage 3: Building the Tree — "I Need to Create Nodes from My Leaf Values"

### Thinking about buildTree

"Now I need a function that takes my leaf values and assembles the entire tree. What does this function need to know?"

Let me think about the parameters:
- `depth` — The depth of the **current node** being created. Root starts at `depth` (the user's input), leaves are at depth 0.
- `leaves[]` — The array of leaf values.
- `index` — Which part of the leaves array does this subtree cover?
- `isMax` — Is this node a MAX or MIN node?

### The indexing trick — how do I map leaves to tree positions?

Let me draw this carefully for depth=2, leaves=[3,5,2,9]:

```
When building with buildTree(depth=2, leaves, index=0, isMax=true):
  → Creates ROOT node (A)
  → Calls buildTree(depth=1, leaves, index=0*2=0, isMax=false)  ← LEFT child (B)
      → Calls buildTree(depth=0, leaves, index=0*2=0, isMax=true)  ← LEFT leaf = leaves[0] = 3 (D)
      → Calls buildTree(depth=0, leaves, index=0*2+1=1, isMax=true)  ← RIGHT leaf = leaves[1] = 5 (E)
  → Calls buildTree(depth=1, leaves, index=0*2+1=1, isMax=false)  ← RIGHT child (C)
      → Calls buildTree(depth=0, leaves, index=1*2=2, isMax=true)  ← LEFT leaf = leaves[2] = 2 (F)
      → Calls buildTree(depth=0, leaves, index=1*2+1=3, isMax=true)  ← RIGHT leaf = leaves[3] = 9 (G)
```

The key insight: **the `index` acts like a heap index**. At each level, the left child's index is `index*2` and the right child's is `index*2+1`. By the time we reach depth=0, the index directly maps to the position in the leaves array.

Let me verify: depth=3, 8 leaves [a,b,c,d,e,f,g,h]
- Root (depth=3, index=0)
  - Left (depth=2, index=0)
    - Left (depth=1, index=0)
      - Left leaf: index=0 → leaves[0] = a ✓
      - Right leaf: index=1 → leaves[1] = b ✓
    - Right (depth=1, index=1)
      - Left leaf: index=2 → leaves[2] = c ✓
      - Right leaf: index=3 → leaves[3] = d ✓
  - Right (depth=2, index=1)
    - Left (depth=1, index=2)
      - Left leaf: index=4 → leaves[4] = e ✓
      - Right leaf: index=5 → leaves[5] = f ✓
    - Right (depth=1, index=3)
      - Left leaf: index=6 → leaves[6] = g ✓
      - Right leaf: index=7 → leaves[7] = h ✓

The indexing works perfectly.

### Writing buildTree step by step

**Step 1: Create the node and name it**

```java
static Node buildTree(int depth, int[] leaves, int index, boolean isMax) {
    Node node = new Node(depth, isMax);
    node.name = counter++;
    // ...
}
```

**Step 2: Base case — if depth is 0, it's a leaf**

```java
if (depth == 0) {
    node.value = leaves[index];
    return node;
}
```

At depth=0, `index` directly points to the right leaf value. Assign it and return.

**Step 3: Recursive case — build left and right children**

```java
node.left = buildTree(depth - 1, leaves, index * 2, !isMax);
node.right = buildTree(depth - 1, leaves, index * 2 + 1, !isMax);
return node;
```

Note the `!isMax` — children alternate between MAX and MIN.

### The complete buildTree

```java
static Node buildTree(int depth, int[] leaves, int index, boolean isMax) {
    Node node = new Node(depth, isMax);
    node.name = counter++;

    if (depth == 0) {
        node.value = leaves[index];
        return node;
    }

    node.left = buildTree(depth - 1, leaves, index * 2, !isMax);
    node.right = buildTree(depth - 1, leaves, index * 2 + 1, !isMax);

    return node;
}
```

### Tracing buildTree for depth=1, leaves=[3,5]

```
buildTree(1, [3,5], 0, true)
  → node A (depth=1, isMax=true), counter becomes 'B'
  → depth != 0, so:
  → node.left = buildTree(0, [3,5], 0, false)
      → node B (depth=0, isMax=false), counter becomes 'C'
      → depth == 0, so node.value = leaves[0] = 3
      → return B
  → node.right = buildTree(0, [3,5], 1, false)
      → node C (depth=0, isMax=false), counter becomes 'D'
      → depth == 0, so node.value = leaves[1] = 5
      → return C
  → return A (with A.left=B, A.right=C)
```

Tree produced:
```
   A (MAX, depth=1)
  / \
 B   C
 3   5
```

Looks right.

---

## Stage 4: Writing the Core Algorithm — "Now I Need Alpha-Beta"

### Thinking it through before writing

"This is the heart of the program. Let me make sure I understand it before writing a single line."

**Alpha and beta — what are they?**

Think of it this way:
- **Alpha** = the best score MAX has guaranteed so far (on the path from root to current node). MAX will NEVER accept anything below alpha.
- **Beta** = the best score MIN has guaranteed so far. MIN will NEVER allow anything above beta.

We start with alpha = -∞ (MAX has no guarantee yet) and beta = +∞ (MIN has no limit set yet).

**When do we prune?**

If `alpha >= beta`, we can prune. Why?

- MAX knows it can get at least `alpha`.
- MIN knows it can force at most `beta`.
- If `alpha >= beta`, MIN will never let this path happen (because it leads to something ≥ alpha which is ≥ beta, which is already worse for MIN than what MIN has elsewhere).

So we stop exploring and mark the remaining children as pruned.

### Writing alphaBeta — skeleton first

```java
static int alphaBeta(Node node, int alpha, int beta) {
    // Base case: leaf node
    if (node.depth == 0) {
        return node.value;
    }

    if (node.isMax) {
        // MAX logic
    } else {
        // MIN logic
    }
}
```

### MAX block — step by step thinking

"For a MAX node, I want to maximize. Let me think..."

1. Start with the worst possible value for MAX: `Integer.MIN_VALUE` (the most negative int)
2. Evaluate the LEFT child first
3. Update my best: `best = Math.max(best, alphaBeta(node.left, alpha, beta))`
4. Update alpha: `alpha = Math.max(alpha, best)` — alpha rises as MAX finds better values
5. Check pruning: if `alpha >= beta`, mark right child as pruned and DON'T recurse into it
6. Otherwise, evaluate right child too
7. Store the final value in `node.value` (for display and path tracing later)

```java
if (node.isMax) {
    int best = Integer.MIN_VALUE;
    best = Math.max(best, alphaBeta(node.left, alpha, beta));
    alpha = Math.max(alpha, best);

    if (alpha >= beta) {
        node.right.pruned = true;
    } else {
        best = Math.max(best, alphaBeta(node.right, alpha, beta));
    }

    node.value = best;
    return best;
}
```

### MIN block — mirrored thinking

"MIN is the mirror image of MAX. I want to minimize."

1. Start with the worst possible value for MIN: `Integer.MAX_VALUE` (the most positive int)
2. Evaluate the LEFT child
3. Update my best: `best = Math.min(best, alphaBeta(node.left, alpha, beta))`
4. Update beta: `beta = Math.min(best, beta)` — beta falls as MIN finds lower values
5. Check pruning: if `alpha >= beta`, mark right child as pruned
6. Otherwise, evaluate right child too

```java
} else {
    int best = Integer.MAX_VALUE;
    best = Math.min(best, alphaBeta(node.left, alpha, beta));
    beta = Math.min(best, beta);

    if (alpha >= beta) {
        node.right.pruned = true;
    } else {
        best = Math.min(best, alphaBeta(node.right, alpha, beta));
    }

    node.value = best;
    return best;
}
```

### The complete alphaBeta

```java
static int alphaBeta(Node node, int alpha, int beta) {
    if (node.depth == 0) {
        return node.value;
    }

    if (node.isMax) {
        int best = Integer.MIN_VALUE;
        best = Math.max(best, alphaBeta(node.left, alpha, beta));
        alpha = Math.max(alpha, best);

        if (alpha >= beta) {
            node.right.pruned = true;
        } else {
            best = Math.max(best, alphaBeta(node.right, alpha, beta));
        }

        node.value = best;
        return best;

    } else {
        int best = Integer.MAX_VALUE;
        best = Math.min(best, alphaBeta(node.left, alpha, beta));
        beta = Math.min(best, beta);

        if (alpha >= beta) {
            node.right.pruned = true;
        } else {
            best = Math.min(best, alphaBeta(node.right, alpha, beta));
        }

        node.value = best;
        return best;
    }
}
```

### Tracing alphaBeta for depth=2, leaves=[3,5,2,9]

Tree (before alpha-beta runs):
```
         A (MAX)
        /       \
    B (MIN)    C (MIN)
    /   \      /   \
   D     E    F     G
   3     5    2     9
```

**Call stack trace:**

```
alphaBeta(A, α=-∞, β=+∞)
  A is MAX. best = Integer.MIN_VALUE

  → alphaBeta(B, α=-∞, β=+∞)
      B is MIN. best = Integer.MAX_VALUE

      → alphaBeta(D, α=-∞, β=+∞)
          D is leaf. return 3

      best = min(MAX_VAL, 3) = 3
      beta = min(3, +∞) = 3
      Check: α(-∞) >= β(3)? NO → continue

      → alphaBeta(E, α=-∞, β=3)
          E is leaf. return 5

      best = min(3, 5) = 3
      B.value = 3
      return 3

  back at A: best = max(MIN_VAL, 3) = 3
  alpha = max(-∞, 3) = 3
  Check: α(3) >= β(+∞)? NO → continue

  → alphaBeta(C, α=3, β=+∞)
      C is MIN. best = Integer.MAX_VALUE

      → alphaBeta(F, α=3, β=+∞)
          F is leaf. return 2

      best = min(MAX_VAL, 2) = 2
      beta = min(2, +∞) = 2
      Check: α(3) >= β(2)? YES! → PRUNE!
      G.pruned = true

      C.value = 2
      return 2

  back at A: best = max(3, 2) = 3
  A.value = 3
  return 3
```

**Result: 3. G was pruned. ✓**

The pruning happened because:
- MAX found a guaranteed path giving 3 (through B)
- When exploring C, MIN immediately found 2 (through F)
- Since 2 < 3 (the alpha), MIN would bring this path to 2 or lower
- MAX already has 3, so MAX would never choose C's path anyway
- G is irrelevant — we prune it

---

## Stage 5: "I Need to Display the Tree" — Writing display()

### Thinking about what I want to print

"Let me write out exactly the format I want, then figure out how to produce it."

Target output:
```
Root A (max) : 3
|-- B(min): 3
|   |-- D : 3 (leaf)
|   '-- E : 5 (leaf)
'-- C(min): 2
    |-- F : 2 (leaf)
    '-- G (pruned)
```

"Okay, let me analyze this format carefully..."

1. Root gets special treatment — prints "Root X (max) : value" with no indent
2. Non-root nodes get a branch prefix: `|-- ` for non-last children, `'-- ` for last child
3. After printing a node, its children are indented:
   - If the node was NOT the last child (`|-- `): add `|   ` to prefix (continuing the vertical line)
   - If the node WAS the last child (`'-- `): add `    ` (4 spaces, no more vertical line)
4. Pruned nodes print "(pruned)" and stop — no children printed
5. Leaf nodes show "(leaf)" after their value
6. Internal nodes show "(max)" or "(min)" type

### Designing the function signature

I need:
- `node` — the current node
- `prefix` — the accumulated indent string
- `isLast` — is this the last child of its parent?
- `root` — is this the root node?

```java
static void display(Node node, String prefix, boolean isLast, boolean root)
```

### Building it incrementally

**Step 1: Handle pruned nodes first — early return**

```java
if (node.pruned) {
    String branch = isLast ? "'-- " : "|-- ";
    System.out.println(prefix + branch + node.name + " (pruned) ");
    return;
}
```

Early return is key — we don't recurse into pruned nodes (they weren't evaluated).

**Step 2: Handle the root node (special case)**

```java
if (root) {
    System.out.println("Root " + node.name + " (max) : " + node.value);
}
```

Root always has isMax=true, so I hardcode "(max)". Root has no branch prefix.

**Step 3: Handle non-root nodes**

```java
else {
    String branch = isLast ? "'-- " : "|-- ";

    if (node.depth == 0) {
        // Leaf
        System.out.println(prefix + branch + node.name + " : " + node.value + " (leaf)");
    } else {
        // Internal
        String type = node.isMax ? "max" : "min";
        System.out.println(prefix + branch + node.name + "(" + type + ")" + ": " + node.value);
    }
}
```

**Step 4: Recurse into children if this node has children**

```java
if (node.depth > 0) {
    String newPrefix;

    if (root) {
        newPrefix = "";
    } else {
        newPrefix = prefix + (isLast ? "    " : "|   ");
    }

    display(node.left, newPrefix, false, false);
    display(node.right, newPrefix, true, false);
}
```

Why `root` gets empty prefix for children? Because root itself has no leading `|-- ` or `'-- `, so its children start fresh.

Why `isLast ? "    " : "|   "`?
- If current node was `'-- ` (last child): its children are indented with spaces only, no vertical bar
- If current node was `|-- ` (not last): its children are indented with `|   ` (continuing the vertical bar downward)

The left child passes `isLast=false`, right child passes `isLast=true`.

### The complete display function

```java
static void display(Node node, String prefix, boolean isLast, boolean root) {

    if (node.pruned) {
        String branch = isLast ? "'-- " : "|-- ";
        System.out.println(prefix + branch + node.name + " (pruned) ");
        return;
    }

    if (root) {
        System.out.println("Root " + node.name + " (max) : " + node.value);
    } else {
        String branch = isLast ? "'-- " : "|-- ";

        if (node.depth == 0) {
            System.out.println(prefix + branch + node.name + " : " + node.value + " (leaf)");
        } else {
            String type = node.isMax ? "max" : "min";
            System.out.println(prefix + branch + node.name + "(" + type + ")" + ": " + node.value);
        }
    }

    if (node.depth > 0) {
        String newPrefix;

        if (root) {
            newPrefix = "";
        } else {
            newPrefix = prefix + (isLast ? "    " : "|   ");
        }

        display(node.left, newPrefix, false, false);
        display(node.right, newPrefix, true, false);
    }
}
```

### Tracing display for our example

Call: `display(A, "", true, true)`

```
node=A, pruned=false, root=true
→ print "Root A (max) : 3"
→ depth>0, root=true so newPrefix=""
→ display(B, "", false, false)   ← isLast=false
→ display(C, "", true, false)    ← isLast=true
```

Inside `display(B, "", false, false)`:
```
node=B, pruned=false, root=false, isLast=false
→ branch = "|-- "
→ depth=1 (not leaf), type="min"
→ print "|-- B(min): 3"
→ depth>0, not root, isLast=false → newPrefix = "" + "|   " = "|   "
→ display(D, "|   ", false, false)
→ display(E, "|   ", true, false)
```

Inside `display(D, "|   ", false, false)`:
```
node=D, pruned=false, root=false, isLast=false
→ branch = "|-- "
→ depth=0 (leaf)
→ print "|   |-- D : 3 (leaf)"
→ depth==0, don't recurse
```

Inside `display(E, "|   ", true, false)`:
```
node=E, pruned=false, root=false, isLast=true
→ branch = "'-- "
→ depth=0 (leaf)
→ print "|   '-- E : 5 (leaf)"
```

Inside `display(C, "", true, false)`:
```
node=C, pruned=false, root=false, isLast=true
→ branch = "'-- "
→ depth=1 (not leaf), type="min"
→ print "'-- C(min): 2"
→ depth>0, not root, isLast=true → newPrefix = "" + "    " = "    "
→ display(F, "    ", false, false)
→ display(G, "    ", true, false)
```

Inside `display(G, "    ", true, false)`:
```
node=G, pruned=true
→ branch = "'-- " (isLast=true)
→ print "    '-- G (pruned) "
→ return (early exit)
```

**Final output:**
```
Root A (max) : 3
|-- B(min): 3
|   |-- D : 3 (leaf)
|   '-- E : 5 (leaf)
'-- C(min): 2
    |-- F : 2 (leaf)
    '-- G (pruned)
```

---

## Stage 6: "I Need to Show the Optimal Path" — Writing printPath()

### What do I want?

"I want to print the sequence of nodes from root to the optimal leaf. Something like: `A -> B -> D`"

"How do I decide which child to follow at each step?"

At each node, the optimal value propagated UP came from one of the children. I follow the child whose value **equals the current node's value**.

But wait — what if the left child was pruned? Then I can't compare its value (it was never computed). So I need to check `!node.left.pruned` before checking its value.

**Logic:**
```
If left child is NOT pruned AND left child's value == current node's value:
    → go left
Else:
    → go right
```

"Actually, I need to be careful. What if BOTH children have the same value? That could happen (e.g., two paths both give value 5). The program just picks left in that case. That's fine — any optimal path is valid."

### Why `System.out.print` (not `println`) for non-leaf nodes?

"I want everything on one line: `A -> B -> D`"

- Non-leaf: `System.out.print(name + " -> ")` — prints without newline, leaves cursor on same line
- Leaf (base case): `System.out.println(name)` — prints name and newline, ending the output

### Writing printPath

```java
static void printPath(Node node) {
    if (node.depth == 0) {
        System.out.println(node.name);
        return;
    }

    System.out.print(node.name + " -> ");

    Node next;
    if (!node.left.pruned && node.left.value == node.value) {
        next = node.left;
    } else {
        next = node.right;
    }

    printPath(next);
}
```

### Tracing printPath for our example

```
printPath(A)
  A.depth=1 > 0
  print "A -> "
  A.left=B, B.pruned=false, B.value=3, A.value=3 → match! next=B

printPath(B)
  B.depth=1 > 0
  print "B -> "
  B.left=D, D.pruned=false, D.value=3, B.value=3 → match! next=D

printPath(D)
  D.depth=0
  println "D"
  return
```

**Output:** `A -> B -> D` ✓

---

## Stage 7: Writing main() — "Connecting Everything"

### Thinking about main

"Now I just need to wire everything together. Let me think about the order of operations."

1. Create a Scanner for user input
2. Ask for depth
3. Calculate number of leaves: 2^depth
4. Ask user for that many leaf values
5. **Reset counter to 'A'** — this is critical!
6. Build the tree
7. Run alpha-beta
8. Display the tree
9. Print optimal value
10. Print optimal path
11. Close the scanner

### About step 5 — why reset the counter?

"Ah, this is subtle. The `counter` variable is `static` — it's shared across the class. When `buildTree` runs, it increments `counter` for each node. If I didn't reset it, the counter would be at 'I' (or wherever it stopped) from a previous run. By resetting to 'A' right before `buildTree`, I guarantee nodes are named A, B, C... consistently."

### About step 3 — why 2^depth leaves?

"A perfect binary tree of depth `d` has exactly 2^d leaves. This is because:
- Depth 0: 1 leaf (just the root = leaf)
- Depth 1: 2 leaves
- Depth 2: 4 leaves
- Depth d: 2^d leaves

In Java: `(int) Math.pow(2, depth)`. Note the explicit cast to `int` — `Math.pow` returns `double`, and I need an `int` for my array size."

### The complete main

```java
public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);

    System.out.print("Enter depth : ");
    int depth = sc.nextInt();

    int size = (int) Math.pow(2, depth);  // 2^depth leaves in a perfect binary tree

    System.out.println("Enter " + size + " values:");

    int[] leaves = new int[size];
    for (int i = 0; i < size; i++) {
        leaves[i] = sc.nextInt();
    }

    counter = 'A';   // IMPORTANT: reset before building
    Node root = buildTree(depth, leaves, 0, true);

    int result = alphaBeta(root, Integer.MIN_VALUE, Integer.MAX_VALUE);

    System.out.println("\nGame Tree:");
    display(root, "", true, true);

    System.out.println("\nOptimal Value: " + result);

    System.out.println("\nOptimal Path:");
    printPath(root);

    sc.close();
}
```

The initial call to `alphaBeta` passes `Integer.MIN_VALUE` for alpha (MAX has no guarantee yet) and `Integer.MAX_VALUE` for beta (MIN has no cap yet).

The initial call to `display` passes:
- `prefix = ""` (nothing accumulated yet)
- `isLast = true` (root is effectively "last" — its parent concept doesn't exist)
- `root = true` (this is the root)

---

## Stage 8: Looking Back — What I Wrote and Why It Works

| What I Wrote | Why I Wrote It | Key Decision |
|---|---|---|
| `static char counter` | Give every node a unique letter name during construction | Static so accessible from static methods; char because A, B, C... |
| `static class Node` | Blueprint for each game tree node | Static inner class — no outer instance needed |
| `buildTree()` | Construct the tree recursively from leaf values | index*2 and index*2+1 maps perfectly to heap-like indexing |
| `alphaBeta()` | Run the minimax with alpha-beta pruning algorithm | Integer.MIN_VALUE / MAX_VALUE as worst-case starting points |
| `display()` | Show the tree visually with ASCII art | prefix+branch+newPrefix pattern for recursive tree printing |
| `printPath()` | Trace and print the optimal decision path | Follow child whose value matches node's value |
| `main()` | Entry point, user input, orchestrates everything | Must reset counter before buildTree; must close scanner |

### Why this design is correct

- **buildTree creates the structure** — every node gets name, depth, isMax, and (for leaves) value
- **alphaBeta fills in the values** — propagates values from leaves upward, marks pruned nodes
- **display reads the completed tree** — by the time display runs, every reachable node has its value set
- **printPath traces the optimal** — because values are set, it can follow the optimal path correctly
- The order matters: build → alpha-beta → display → path. Can't display before alpha-beta runs.

---

## Stage 9: How to Write This in an Exam in 30 Minutes

### Step-by-step checklist

Work in this EXACT order. Each step builds on the previous.

---

**Step 1: Write the class shell and imports (30 seconds)**

```java
import java.util.*;

public class practice {
    static char counter = 'A';

    // ... rest goes here

    public static void main(String[] args) { }
}
```

**Memory trigger:** *"Scanner needs `java.util.*`. Counter starts at A."*

---

**Step 2: Write the Node class (2 minutes)**

Ask yourself: *"What does each node KNOW?"*
- Depth (am I a leaf?)
- Value (what's my minimax score?)
- isMax (am I MAX or MIN?)
- pruned (was I cut off?)
- left, right (my children)
- name (my letter label)

Constructor: *only depth and isMax* (rest assigned later)

```java
static class Node {
    int depth, value;
    boolean isMax, pruned = false;
    Node left, right;
    char name;

    Node(int depth, boolean isMax) {
        this.depth = depth;
        this.isMax = isMax;
    }
}
```

**Memory trigger:** *"d-v-i-p-l-r-n: depth, value, isMax, pruned, left, right, name. Constructor only needs depth and isMax."*

---

**Step 3: Write buildTree (4 minutes)**

Signature: `static Node buildTree(int depth, int[] leaves, int index, boolean isMax)`

1. Create node, assign name from counter
2. If depth == 0: assign value from `leaves[index]`, return
3. Recurse: left = `buildTree(depth-1, leaves, index*2, !isMax)`, right = `index*2+1`
4. Return node

```java
static Node buildTree(int depth, int[] leaves, int index, boolean isMax) {
    Node node = new Node(depth, isMax);
    node.name = counter++;
    if (depth == 0) {
        node.value = leaves[index];
        return node;
    }
    node.left = buildTree(depth - 1, leaves, index * 2, !isMax);
    node.right = buildTree(depth - 1, leaves, index * 2 + 1, !isMax);
    return node;
}
```

**Memory trigger:** *"Create → Name → Leaf check → Left (×2) → Right (×2+1) → Return."*

---

**Step 4: Write alphaBeta (8 minutes)**

Signature: `static int alphaBeta(Node node, int alpha, int beta)`

Structure:
1. If leaf → return value
2. If MAX: best = MIN_VALUE, eval left, update alpha, prune or eval right, store+return best
3. If MIN: best = MAX_VALUE, eval left, update beta, prune or eval right, store+return best

```java
static int alphaBeta(Node node, int alpha, int beta) {
    if (node.depth == 0) return node.value;

    if (node.isMax) {
        int best = Integer.MIN_VALUE;
        best = Math.max(best, alphaBeta(node.left, alpha, beta));
        alpha = Math.max(alpha, best);
        if (alpha >= beta) { node.right.pruned = true; }
        else { best = Math.max(best, alphaBeta(node.right, alpha, beta)); }
        node.value = best;
        return best;
    } else {
        int best = Integer.MAX_VALUE;
        best = Math.min(best, alphaBeta(node.left, alpha, beta));
        beta = Math.min(best, beta);
        if (alpha >= beta) { node.right.pruned = true; }
        else { best = Math.min(best, alphaBeta(node.right, alpha, beta)); }
        node.value = best;
        return best;
    }
}
```

**Memory trigger:** *"Leaf → return. MAX uses MIN_VALUE+max+alpha. MIN uses MAX_VALUE+min+beta. Both: prune-or-eval, store, return."*

---

**Step 5: Write display (8 minutes)**

Signature: `static void display(Node node, String prefix, boolean isLast, boolean root)`

Structure:
1. If pruned → print pruned + return
2. If root → print "Root X (max) : value"
3. Else → pick branch (`'--` or `|--`), print leaf or internal
4. If has children → compute newPrefix, recurse left (isLast=false) and right (isLast=true)

**Memory trigger:** *"Pruned first. Root special. Branch depends on isLast. Prefix grows: last→spaces, not-last→pipe."*

---

**Step 6: Write printPath (3 minutes)**

Signature: `static void printPath(Node node)`

Structure:
1. If depth==0 → println(name), return
2. print(name + " -> ")
3. If left is not pruned and left.value == node.value → next = left, else next = right
4. Recurse into next

**Memory trigger:** *"Leaf → println+return. Non-leaf → print+arrow, follow matching-value child."*

---

**Step 7: Write main (4 minutes)**

Order: Scanner → depth → size (2^depth, cast int) → fill leaves → reset counter → buildTree → alphaBeta → display → printOptimal → printPath → close scanner

**Memory trigger:** *"Input → reset counter → build → alpha-beta → display → value → path → close."*

---

### Time budget for exam

| Step | Task | Time |
|---|---|---|
| 1 | Class shell + counter | 30s |
| 2 | Node class | 2 min |
| 3 | buildTree | 4 min |
| 4 | alphaBeta | 8 min |
| 5 | display | 8 min |
| 6 | printPath | 3 min |
| 7 | main | 4 min |
| — | **Total** | **~30 min** |

---

## Stage 10: Tracing Through a Full Example

### Setup: depth=2, leaves=[3, 5, 2, 9]

**Input:**
```
Enter depth : 2
Enter 4 values:
3 5 2 9
```

### Step 1: buildTree constructs the following tree

```
counter starts at 'A'

buildTree(2, [3,5,2,9], 0, true)
  → Node A (depth=2, isMax=true), counter='B'
  → left = buildTree(1, [3,5,2,9], 0, false)
      → Node B (depth=1, isMax=false), counter='C'
      → left = buildTree(0, [3,5,2,9], 0, true)
          → Node C (depth=0, isMax=true), counter='D'
          → value = leaves[0] = 3
          → return C
      → right = buildTree(0, [3,5,2,9], 1, true)
          → Node D (depth=0, isMax=true), counter='E'
          → value = leaves[1] = 5
          → return D
      → return B (B.left=C, B.right=D)
  → right = buildTree(1, [3,5,2,9], 1, false)
      → Node E (depth=1, isMax=false), counter='F'
      → left = buildTree(0, [3,5,2,9], 2, true)
          → Node F (depth=0, isMax=true), counter='G'
          → value = leaves[2] = 2
          → return F
      → right = buildTree(0, [3,5,2,9], 3, true)
          → Node G (depth=0, isMax=true), counter='H'
          → value = leaves[3] = 9
          → return G
      → return E (E.left=F, E.right=G)
  → return A (A.left=B, A.right=E)
```

**Tree structure:**
```
           A (MAX, depth=2)
          /                \
    B (MIN, depth=1)    E (MIN, depth=1)
       /      \             /       \
  C (depth=0) D (depth=0) F (depth=0) G (depth=0)
      3            5           2           9
```

### Step 2: alphaBeta runs

```
alphaBeta(A, α=MIN_INT, β=MAX_INT)
─────────────────────────────────────────────────────────────────
  A is MAX. best = MIN_INT

  Call alphaBeta(B, α=MIN_INT, β=MAX_INT)
  ─────────────────────────────────────────────────────────────
    B is MIN. best = MAX_INT

    Call alphaBeta(C, α=MIN_INT, β=MAX_INT)
    ──────────────────────────────────────
      C is leaf. return 3
    ──────────────────────────────────────

    best = min(MAX_INT, 3) = 3
    beta = min(3, MAX_INT) = 3
    α(MIN_INT) >= β(3)? NO → continue to right child

    Call alphaBeta(D, α=MIN_INT, β=3)
    ──────────────────────────────────────
      D is leaf. return 5
    ──────────────────────────────────────

    best = min(3, 5) = 3   (5 is worse for MIN, so best stays 3)
    B.value = 3
    return 3
  ─────────────────────────────────────────────────────────────

  best = max(MIN_INT, 3) = 3
  alpha = max(MIN_INT, 3) = 3
  α(3) >= β(MAX_INT)? NO → continue to right child

  Call alphaBeta(E, α=3, β=MAX_INT)
  ─────────────────────────────────────────────────────────────
    E is MIN. best = MAX_INT

    Call alphaBeta(F, α=3, β=MAX_INT)
    ──────────────────────────────────────
      F is leaf. return 2
    ──────────────────────────────────────

    best = min(MAX_INT, 2) = 2
    beta = min(2, MAX_INT) = 2
    α(3) >= β(2)? YES → PRUNE! G.pruned = true

    E.value = 2
    return 2
  ─────────────────────────────────────────────────────────────

  best = max(3, 2) = 3   (E returned 2, but MAX's best stays 3)
  A.value = 3
  return 3
─────────────────────────────────────────────────────────────────
```

### Pruning visualized

```
           A (MAX) ← value=3
          /                \
    B (MIN) ← value=3    E (MIN) ← value=2
       /      \             /       \
      C         D          F         G
      3         5          2       [PRUNED]
                                (never evaluated)
```

### Step 3: display is called

```
display(A, "", true, true)
  → root=true: print "Root A (max) : 3"
  → depth>0, root → newPrefix=""
  → display(B, "", false, false)
      → branch="|-- " (isLast=false)
      → depth=1, type="min"
      → print "|-- B(min): 3"
      → newPrefix="" + "|   " = "|   "
      → display(C, "|   ", false, false)
          → branch="|-- " (isLast=false)
          → depth=0: print "|   |-- C : 3 (leaf)"
      → display(D, "|   ", true, false)
          → branch="'-- " (isLast=true)
          → depth=0: print "|   '-- D : 5 (leaf)"
  → display(E, "", true, false)
      → branch="'-- " (isLast=true)
      → depth=1, type="min"
      → print "'-- E(min): 2"
      → newPrefix="" + "    " = "    "
      → display(F, "    ", false, false)
          → branch="|-- " (isLast=false)
          → depth=0: print "    |-- F : 2 (leaf)"
      → display(G, "    ", true, false)
          → G.pruned=true!
          → branch="'-- " (isLast=true)
          → print "    '-- G (pruned) "
          → return (early exit)
```

**Game Tree output:**
```
Root A (max) : 3
|-- B(min): 3
|   |-- C : 3 (leaf)
|   '-- D : 5 (leaf)
'-- E(min): 2
    |-- F : 2 (leaf)
    '-- G (pruned)
```

> **Note:** The naming here (C,D,E,F,G for internal/leaf nodes) matches the counter assignment order: buildTree visits A→B→C→D→E→F→G in DFS order (root, then left subtree depth-first, then right subtree).

### Step 4: printPath is called

```
printPath(A)
  depth=2 > 0
  print "A -> "
  A.left=B, B.pruned=false, B.value=3, A.value=3 → match → next=B

printPath(B)
  depth=1 > 0
  print "B -> "
  B.left=C, C.pruned=false, C.value=3, B.value=3 → match → next=C

printPath(C)
  depth=0
  println "C"
  return
```

**Optimal Path output:** `A -> B -> C`

### Final complete output

```
Enter depth : 2
Enter 4 values:
3 5 2 9

Game Tree:
Root A (max) : 3
|-- B(min): 3
|   |-- C : 3 (leaf)
|   '-- D : 5 (leaf)
'-- E(min): 2
    |-- F : 2 (leaf)
    '-- G (pruned)

Optimal Value: 3

Optimal Path:
A -> B -> C
```

---

## Appendix: Complete Code For Reference

```java
import java.util.*;

public class practice {
    static char counter = 'A';

    static class Node {
        int depth, value;
        boolean isMax, pruned = false;
        Node left, right;
        char name;

        Node(int depth, boolean isMax) {
            this.depth = depth;
            this.isMax = isMax;
        }
    }

    static Node buildTree(int depth, int[] leaves, int index, boolean isMax) {
        Node node = new Node(depth, isMax);
        node.name = counter++;

        if (depth == 0) {
            node.value = leaves[index];
            return node;
        }

        node.left = buildTree(depth - 1, leaves, index * 2, !isMax);
        node.right = buildTree(depth - 1, leaves, index * 2 + 1, !isMax);

        return node;
    }

    static int alphaBeta(Node node, int alpha, int beta) {
        if (node.depth == 0) {
            return node.value;
        }

        if (node.isMax) {
            int best = Integer.MIN_VALUE;
            best = Math.max(best, alphaBeta(node.left, alpha, beta));
            alpha = Math.max(alpha, best);

            if (alpha >= beta) {
                node.right.pruned = true;
            } else {
                best = Math.max(best, alphaBeta(node.right, alpha, beta));
            }

            node.value = best;
            return best;

        } else {
            int best = Integer.MAX_VALUE;
            best = Math.min(best, alphaBeta(node.left, alpha, beta));
            beta = Math.min(best, beta);

            if (alpha >= beta) {
                node.right.pruned = true;
            } else {
                best = Math.min(best, alphaBeta(node.right, alpha, beta));
            }

            node.value = best;
            return best;
        }
    }

    static void display(Node node, String prefix, boolean isLast, boolean root) {

        if (node.pruned) {
            String branch = isLast ? "'-- " : "|-- ";
            System.out.println(prefix + branch + node.name + " (pruned) ");
            return;
        }

        if (root) {
            System.out.println("Root " + node.name + " (max) : " + node.value);
        } else {
            String branch = isLast ? "'-- " : "|-- ";

            if (node.depth == 0) {
                System.out.println(prefix + branch + node.name + " : " + node.value + " (leaf)");
            } else {
                String type = node.isMax ? "max" : "min";
                System.out.println(prefix + branch + node.name + "(" + type + ")" + ": " + node.value);
            }
        }

        if (node.depth > 0) {
            String newPrefix;

            if (root) {
                newPrefix = "";
            } else {
                newPrefix = prefix + (isLast ? "    " : "|   ");
            }

            display(node.left, newPrefix, false, false);
            display(node.right, newPrefix, true, false);
        }
    }

    static void printPath(Node node) {
        if (node.depth == 0) {
            System.out.println(node.name);
            return;
        }
        System.out.print(node.name + " -> ");
        Node next;

        if (!node.left.pruned && node.left.value == node.value) {
            next = node.left;
        } else {
            next = node.right;
        }

        printPath(next);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter depth : ");
        int depth = sc.nextInt();

        int size = (int) Math.pow(2, depth);  // type casting

        System.out.println("Enter " + size + " values:");

        int[] leaves = new int[size];
        for (int i = 0; i < size; i++) {
            leaves[i] = sc.nextInt();
        }

        counter = 'A';
        Node root = buildTree(depth, leaves, 0, true);

        int result = alphaBeta(root, Integer.MIN_VALUE, Integer.MAX_VALUE);

        System.out.println("\nGame Tree:");

        display(root, "", true, true);

        System.out.println("\nOptimal Value: " + result);

        System.out.println("\nOptimal Path:");
        printPath(root);

        sc.close();
    }
}
```

---

## Quick-Reference Cheat Sheet (Print This)

```
╔══════════════════════════════════════════════════════════════════════╗
║              ALPHA-BETA PRUNING — EXAM QUICK REFERENCE              ║
╠══════════════════════════════════════════════════════════════════════╣
║ STRUCTURE ORDER:                                                     ║
║   counter → Node class → buildTree → alphaBeta → display            ║
║   → printPath → main                                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║ NODE FIELDS: depth, value, isMax, pruned=false, left, right, name   ║
║ CONSTRUCTOR: Node(int depth, boolean isMax) { ... }                  ║
╠══════════════════════════════════════════════════════════════════════╣
║ BUILDTREE:                                                           ║
║   create → name (counter++) → if depth==0: value=leaves[idx],return ║
║   left = buildTree(depth-1, leaves, idx*2, !isMax)                  ║
║   right = buildTree(depth-1, leaves, idx*2+1, !isMax)               ║
╠══════════════════════════════════════════════════════════════════════╣
║ ALPHA-BETA:                                                          ║
║   if leaf → return value                                             ║
║   MAX: best=MIN_VAL, eval left, alpha=max(alpha,best)               ║
║        if α≥β → right.pruned=true ELSE eval right                   ║
║   MIN: best=MAX_VAL, eval left, beta=min(best,beta)                 ║
║        if α≥β → right.pruned=true ELSE eval right                   ║
║   both: node.value=best; return best                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║ DISPLAY: (node, prefix, isLast, root)                                ║
║   pruned → print+return | root → "Root X (max) : val"               ║
║   else → branch=(isLast?"'-- ":"|-- ") + leaf or internal print     ║
║   newPrefix = prefix + (isLast ? "    " : "|   ")                   ║
║   recurse left(isLast=false), right(isLast=true)                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ PRINTPATH: (node)                                                    ║
║   depth==0 → println(name); return                                  ║
║   print(name + " -> ")                                               ║
║   if !left.pruned && left.value==node.value → next=left             ║
║   else → next=right; recurse printPath(next)                        ║
╠══════════════════════════════════════════════════════════════════════╣
║ MAIN ORDER:                                                          ║
║   depth → size=(int)pow(2,depth) → fill leaves                      ║
║   counter='A' → buildTree → alphaBeta → display → value → path     ║
╚══════════════════════════════════════════════════════════════════════╝
```
