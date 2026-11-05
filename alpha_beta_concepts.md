# Alpha-Beta Pruning — Complete Code Walkthrough

> This document explains every line, every keyword, every decision in the Java Alpha-Beta Pruning program — in the exact order the code is written. Read it top-to-bottom and you will be able to reproduce this program from memory in an exam hall.

---

## Table of Contents
1. [The Big Picture: What Problem Are We Solving?](#1-the-big-picture)
2. [`import java.util.*` — Why This Line Is First](#2-import-javautilstar)
3. [`public class practice` — The Outer Shell](#3-public-class-practice)
4. [`static char counter = 'A'` — The Global Name Giver](#4-static-char-counter)
5. [`static class Node` — The Blueprint of Every Tree Node](#5-static-class-node)
6. [`static Node buildTree(...)` — Constructing the Game Tree Recursively](#6-static-node-buildtree)
7. [`static int alphaBeta(...)` — The Heart of the Algorithm](#7-static-int-alphabeta)
8. [`static void display(...)` — Pretty-Printing the Tree](#8-static-void-display)
9. [`static void printPath(...)` — Tracing the Optimal Move](#9-static-void-printpath)
10. [`public static void main(...)` — The Entry Point](#10-public-static-void-main)
11. [Key Java Concepts — Quick Reference Table](#11-key-java-concepts)
12. [How the Whole Thing Connects — Flow Diagram](#12-flow-diagram)
13. [Common Exam Mistakes to Avoid](#13-common-exam-mistakes)

---

## 1. The Big Picture: What Problem Are We Solving?

### What Is a Game Tree?

Imagine you are playing **Tic-Tac-Toe** or **Chess**. At every point in the game, you (the player) must choose a move. Each move leads to a new board state, and from that state, your opponent makes a move, and so on. We can model this as a **tree**:

```
                  [Your Turn: Pick a move]
                 /           |           \
          [Move A]       [Move B]      [Move C]
          /     \         /    \        /    \
    [Opp:A1] [Opp:A2] [B1]  [B2]  [C1]  [C2]
```

- **Root node**: The current game state.
- **Internal nodes**: Intermediate game states after some moves.
- **Leaf nodes**: Terminal states — the game is over, and we can assign a **score** (positive if YOU win, negative if opponent wins, 0 for draw).

### What Is Minimax?

In a two-player zero-sum game:
- **YOU** (the **MAX** player) want to **maximize** your score.
- **YOUR OPPONENT** (the **MIN** player) wants to **minimize** your score.

The **Minimax** algorithm works like this:
- At **MAX nodes** (your turn): pick the child with the **highest** value.
- At **MIN nodes** (opponent's turn): pick the child with the **lowest** value.

The values propagate bottom-up from the leaves:

```
         MAX:  3
        /     \
    MIN:3    MIN:5
    /   \    /   \
   3     5  2     5
```

- MIN on the left picks `min(3,5) = 3`.
- MIN on the right picks `min(2,5) = 2`.
- MAX at root picks `max(3,2) = 3`. → Optimal value is **3**.

### Why Does Minimax Get Expensive?

If the game has a depth of `d` and each node has `b` children (branching factor), the total number of nodes to evaluate is **b^d**.

| Game    | Branching Factor | Depth | Nodes         |
|---------|-----------------|-------|---------------|
| Chess   | ~35             | ~80   | Astronomical  |
| Go      | ~250            | ~150  | Beyond compute|
| Tic-Tac-Toe | ~9        | 9     | ~362,880      |

Even Tic-Tac-Toe has ~362,880 terminal states. Chess is effectively **infinite** for brute-force search. We need something smarter.

### What Is Alpha-Beta Pruning?

**Alpha-Beta Pruning** is an optimization of Minimax. It **skips evaluating branches** that can **never** affect the final decision — branches that a rational opponent would never allow you to reach.

**The key insight:**
> If you already found a move that guarantees you a score of X, and while exploring another branch your opponent can force a score WORSE than X — stop exploring that branch. It doesn't matter.

#### Concrete Example:

```
         MAX: ?
        /       \
    MIN: 3      MIN: ?
    /   \        /   \
   3     5      2    [???]
```

1. Explore left subtree of MIN-left: see `3`.
2. Explore right subtree of MIN-left: see `5`.
3. MIN-left picks `min(3,5) = 3`. MAX now knows it can get **at least 3**.
4. Start exploring MIN-right. First child is `2`.
5. MIN-right so far: `min(2, ???)` ≤ 2. Since MAX already has 3, and MIN-right will return **at most 2**, MAX will never choose MIN-right.
6. **Prune [???]** — we never need to look at it!

This is the beauty of Alpha-Beta Pruning. In the **best case**, it reduces the search from O(b^d) to O(b^(d/2)) — effectively **doubling the searchable depth** for the same computation budget.

### The Two Variables: Alpha and Beta

| Variable | Maintained by | Meaning |
|----------|--------------|---------|
| `alpha`  | MAX player   | The **best** (highest) value MAX is **guaranteed** so far on the current path from root |
| `beta`   | MIN player   | The **best** (lowest) value MIN is **guaranteed** so far on the current path from root |

**Pruning rule:**
- If `alpha >= beta` at any node → **prune**. The current branch will never be chosen by a rational player.

---

## 2. `import java.util.*` — Why This Line Is First

```java
import java.util.*;
```

### What Does This Line Do?

Java organizes its built-in classes into **packages** — think of them as folders of related functionality. The `java.util` package contains utility classes like:

| Class / Interface | Purpose |
|------------------|---------|
| `Scanner`        | Read input from the user (keyboard) |
| `ArrayList`      | Dynamic array |
| `LinkedList`     | Doubly-linked list |
| `HashMap`        | Key-value store |
| `Arrays`         | Utility methods for arrays |
| `Collections`    | Sorting, shuffling, etc. |

### Why `*` (Wildcard)?

The `*` is a **wildcard** that means "import everything from this package." Instead of writing:

```java
import java.util.Scanner;
import java.util.ArrayList;
// ...etc
```

You write one line:

```java
import java.util.*;
```

In this program, the **only** class actually used from `java.util` is `Scanner`. But using `*` is a common convenience practice, especially in exam settings. It does **not** slow down your program — Java only loads what it actually uses.

### Why Is `import` Always First?

Java syntax rules require that `import` statements come **before** any class declarations. The structure of every Java file is:

```
1. package declaration (optional)
2. import statements
3. class declaration
```

---

## 3. `public class practice` — The Outer Shell

```java
public class practice {
```

### Breaking It Down Word by Word

#### `public`

`public` is an **access modifier**. It controls who can see and use this class.

| Modifier    | Who can access it? |
|------------|-------------------|
| `public`   | Everyone, from anywhere |
| `private`  | Only within this class |
| `protected`| This class + subclasses |
| *(none)*   | Only within the same package |

In Java, **exactly one class per file** must be `public`, and its name must match the filename. Since our class is `practice`, the file must be named `practice.java`.

#### `class`

This keyword tells Java: "Everything inside the `{}` is a blueprint — a new data type called `practice`." A class can contain:
- **Fields** (variables)
- **Methods** (functions)
- **Inner classes** (classes inside classes)
- **Constructors** (special methods to create objects)

#### `practice`

This is the **name** of the class. In Java convention, class names should start with a capital letter (`Practice`), but this code uses `practice` — a minor style violation that still compiles perfectly.

#### Why Must the Filename Match?

Java's compiler (`javac`) identifies the public class in a file by its name. When you run:
```
javac practice.java
```
The compiler looks for a `public class practice` inside `practice.java`. If the names don't match, you get a compilation error.

---

## 4. `static char counter = 'A'` — The Global Name Giver

```java
static char counter = 'A';
```

### What Is `static`?

`static` means this variable **belongs to the class itself**, not to any specific object. There is **exactly one copy** of `counter`, shared by all methods in `practice`.

Without `static`, every object of `practice` would have its own `counter`. But since `practice` is never instantiated (we only call static methods), we **need** static fields.

Think of it like a **global counter on the whiteboard** — everyone in the room (every method call) can see it and update it.

### What Is `char`?

`char` (character) is a Java primitive data type that stores a **single Unicode character** in 2 bytes. Characters are written with **single quotes**: `'A'`, `'B'`, `'Z'`.

Crucially, in Java, **chars are numbers underneath**. Every character has a numeric ASCII/Unicode value:

| Character | ASCII/Unicode Value |
|-----------|-------------------|
| `'A'`     | 65                |
| `'B'`     | 66                |
| `'C'`     | 67                |
| `'Z'`     | 90                |
| `'a'`     | 97                |

### Why `'A'`?

We want to **name each node** in the tree with a unique letter: `A`, `B`, `C`, `D`, ... The counter starts at `'A'` and increments each time a new node is created.

### How Does `counter++` Work with Chars?

When you write `counter++`, Java:
1. Uses the **current value** of `counter` (e.g., `'A'`).
2. Increments `counter` by 1 (e.g., `counter` becomes `'B'`).
3. Returns the **original** value (`'A'`).

This is the **post-increment** operator. So:

```java
node.name = counter++;  // node.name gets 'A', counter becomes 'B'
node.name = counter++;  // node.name gets 'B', counter becomes 'C'
```

Each node gets a unique letter label automatically!

### Why Reset It in `main`?

```java
counter = 'A';  // in main, before buildTree
```

If the program were to run `buildTree` multiple times (e.g., in a loop), `counter` would continue from where it left off. Resetting ensures we always start labeling from `'A'` for a fresh tree.

---

## 5. `static class Node` — The Blueprint of Every Tree Node

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

### What Is an Inner Class?

A class defined **inside another class** is called an **inner class** (or **nested class**). Here, `Node` is defined inside `practice`.

#### Why `static`?

A `static` inner class **does not** need a reference to the outer class (`practice`) to exist. A non-static inner class (called an **inner class**) would implicitly hold a reference to its enclosing `practice` object — which is wasteful here since `practice` is never instantiated.

The rule of thumb: **if the inner class doesn't need to access instance fields of the outer class, make it static.**

### Every Field Explained

#### `int depth`

Stores how deep in the tree this node is. The **root** has the maximum depth (e.g., 3 for a depth-3 tree). **Leaf nodes** have `depth == 0`.

```
depth=3    [ROOT]
            /    \
depth=2   [ ]    [ ]
          / \    / \
depth=1  [ ][ ] [ ][ ]
         /\ /\  /\ /\
depth=0 Leaves (8 of them)
```

Why store depth in the node? Because the algorithm needs to know: "Am I at a leaf?" Answer: `node.depth == 0`.

#### `int value`

The **computed game value** of this node:
- For **leaf nodes**: set directly from the `leaves[]` array (user input).
- For **internal nodes**: computed by the alpha-beta algorithm as the best achievable score from this node downward.

After `alphaBeta()` runs, every non-pruned node has a meaningful `value`.

#### `boolean isMax`

`true` if this is a **MAX node** (the maximizing player's turn), `false` if it is a **MIN node** (the minimizing player's turn).

This alternates as you go down the tree:
```
Root      → isMax = true  (MAX turn)
Depth-1   → isMax = false (MIN turn)
Depth-2   → isMax = true  (MAX turn)
Depth-0   → isMax = false (MIN turn) [leaves don't really matter]
```

#### `boolean pruned = false`

A **flag** that marks whether this node was **pruned** (skipped) by the alpha-beta algorithm. Default is `false` (not pruned).

Notice: `pruned = false` is an **inline initialization** — it gives the field a default value right where it is declared. This means we don't need to set it in the constructor for every node.

When `alphaBeta()` determines that a right child's branch is useless, it sets:
```java
node.right.pruned = true;
```

The `display()` and `printPath()` methods then use this flag to show pruned nodes differently.

#### `Node left`, `Node right`

These are **references** to the left and right child nodes. Since `Node` is a class (a reference type), these variables don't store the nodes themselves — they store **memory addresses** pointing to child `Node` objects.

Initially, both are `null` (Java's default for reference types). They get assigned in `buildTree()`.

For **leaf nodes**, `left` and `right` remain `null` (leaves have no children).

#### `char name`

A single character label (`'A'`, `'B'`, `'C'`...) assigned by the `counter++` mechanism. Used purely for **display purposes** — to help the user identify which node is which in the printed tree.

### The Constructor: `Node(int depth, boolean isMax)`

```java
Node(int depth, boolean isMax) {
    this.depth = depth;
    this.isMax = isMax;
}
```

A **constructor** is a special method that runs **automatically** when you create a new object with `new`. It has:
- **No return type** (not even `void`).
- The **same name** as the class.

#### Why Only Two Parameters?

The constructor only takes `depth` and `isMax` because these are the **two things we know at node creation time**:
- We know how deep the node is.
- We know whose turn it is.

The other fields are set **later**:
- `name` is set right after creation (`node.name = counter++`).
- `value` is set either during `buildTree` (for leaves) or during `alphaBeta` (for internal nodes).
- `left` and `right` are set recursively in `buildTree`.
- `pruned` defaults to `false`.

#### What Is `this`?

Inside a constructor or method, `this` refers to the **current object being worked on**. It disambiguates between the parameter name and the field name when they are the same:

```java
this.depth = depth;
//  ^field    ^parameter
```

Without `this.depth = depth`, Java would be confused — it would think you are assigning the parameter to itself.

---

## 6. `static Node buildTree(...)` — Constructing the Game Tree Recursively

```java
static Node buildTree(int depth, int[] leaves, int index, boolean isMax) {
    Node node = new Node(depth, isMax);
    node.name = counter++;

    if (depth == 0) {
        node.value = leaves[index];
        return node;
    }

    node.left  = buildTree(depth - 1, leaves, index * 2,     !isMax);
    node.right = buildTree(depth - 1, leaves, index * 2 + 1, !isMax);

    return node;
}
```

### Why `static`?

Like all methods in this program, `buildTree` is `static` because we call it directly from `main` (which is also static) without creating a `practice` object. Static methods can only call other static methods directly.

### Why Return Type `Node`?

`buildTree` **creates** a node and returns it so the caller can store the reference:
```java
Node root = buildTree(depth, leaves, 0, true);
```
The `Node` return type tells Java: "This method hands you back a `Node` object."

### All 4 Parameters Explained

| Parameter    | Type    | Meaning |
|-------------|---------|---------|
| `depth`     | `int`   | How many levels below this node are there? 0 = leaf |
| `leaves`    | `int[]` | The array of leaf values provided by the user |
| `index`     | `int`   | The **position** of this node within the conceptual array-based binary tree |
| `isMax`     | `boolean`| Is this a MAX node (`true`) or MIN node (`false`)? |

### Line-by-Line Breakdown

#### Creating the Node

```java
Node node = new Node(depth, isMax);
```

- `new Node(depth, isMax)` calls the constructor, allocating memory for a new Node object.
- The local variable `node` holds a reference (pointer) to that memory.

#### Assigning a Name

```java
node.name = counter++;
```

- `counter++` returns the **current** value of `counter` and then increments it.
- First call: `node.name = 'A'`, `counter` becomes `'B'`.
- Second call: `node.name = 'B'`, `counter` becomes `'C'`.
- And so on.

Since `buildTree` uses **pre-order traversal** (process the node before its children), the root gets `'A'`, its left child gets `'B'`, etc.

#### The Base Case

```java
if (depth == 0) {
    node.value = leaves[index];
    return node;
}
```

**Recursion always needs a base case** — a condition where it stops calling itself and returns directly.

Here: if `depth == 0`, we are at a **leaf node**. Leaf nodes:
- Have no children (we don't recurse further).
- Have a **fixed value** from the user's input: `leaves[index]`.
- Are returned immediately with `return node`.

#### The Recursive Case and Binary Tree Indexing

```java
node.left  = buildTree(depth - 1, leaves, index * 2,     !isMax);
node.right = buildTree(depth - 1, leaves, index * 2 + 1, !isMax);
```

This is the most intellectually rich part of `buildTree`. Let's unpack it:

##### `depth - 1`
Each level down the tree, the depth decreases by 1. So if the root has `depth=3`, its children have `depth=2`, their children `depth=1`, and leaves have `depth=0`.

##### `!isMax`
The player alternates at each level. If the current node is MAX (`isMax=true`), its children are MIN (`!isMax = false`), and vice versa. The `!` operator flips a boolean.

##### The Index Formula: `index * 2` and `index * 2 + 1`

This is the **heap (array-based binary tree) indexing trick**. Imagine laying out the entire binary tree into an array, level by level:

```
Level 0 (root):   index = 1
Level 1:          indices = 2, 3
Level 2:          indices = 4, 5, 6, 7
Level 3 (leaves): indices = 8, 9, 10, 11, 12, 13, 14, 15
```

But our code starts from `index = 0` at the root:

```
index=0 is the root
  left child  = index * 2     = 0
  right child = index * 2 + 1 = 1

index=0's left child (index=0 at depth-1):
  left child  = 0 * 2     = 0
  right child = 0 * 2 + 1 = 1

... ultimately at depth=0 (leaves), indices 0..7 map to leaves[0]..leaves[7]
```

Wait — let me clarify. The root is called with `index=0`. Let's trace for `depth=2`:

```
buildTree(2, leaves, 0, true)        → Root (index 0)
  buildTree(1, leaves, 0, false)     → Left child of root (index 0)
    buildTree(0, leaves, 0, true)    → Leaf: leaves[0]
    buildTree(0, leaves, 1, true)    → Leaf: leaves[1]
  buildTree(1, leaves, 1, false)     → Right child of root (index 1)
    buildTree(0, leaves, 2, true)    → Leaf: leaves[2]
    buildTree(0, leaves, 3, true)    → Leaf: leaves[3]
```

The leaf indices naturally land on `0, 1, 2, 3` — which maps exactly to `leaves[0], leaves[1], leaves[2], leaves[3]`. The formula works because each level doubles the index range, perfectly covering all leaf positions.

**ASCII diagram for depth=2:**
```
                  [0]
                 /   \
               [0]   [1]
               / \   / \
    leaves: [0] [1] [2] [3]
```

##### `return node`

After setting up both children, we return this node. The parent's call to `buildTree` will store this as either `node.left` or `node.right`.

---

## 7. `static int alphaBeta(...)` — The Heart of the Algorithm

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

### Parameters: Alpha, Beta, and Node

| Parameter | Type   | Meaning |
|-----------|--------|---------|
| `node`    | `Node` | The current node being evaluated |
| `alpha`   | `int`  | Best value MAX is **guaranteed** anywhere on the path from root to here |
| `beta`    | `int`  | Best value MIN is **guaranteed** anywhere on the path from root to here |

**Precise definitions:**
- `alpha` = the **lower bound** on the value that MAX will accept. MAX will never choose something less than `alpha`.
- `beta` = the **upper bound** on the value that MIN will accept. MIN will never choose something greater than `beta`.

Initially: `alpha = Integer.MIN_VALUE` (MAX has guaranteed nothing yet), `beta = Integer.MAX_VALUE` (MIN has guaranteed nothing yet).

### Base Case

```java
if (node.depth == 0) {
    return node.value;
}
```

Leaf nodes already have their `value` set by `buildTree`. We simply return it. This is where the recursion bottoms out.

### MAX Node Block

```java
if (node.isMax) {
    int best = Integer.MIN_VALUE;
```

`Integer.MIN_VALUE` is the **smallest possible `int`** in Java: `-2,147,483,648` (i.e., −2³¹). We use it as the starting value for `best` because:
- We want the **first real child value** to automatically be better than our starting point.
- Any real game score will be ≥ `Integer.MIN_VALUE`, so `Math.max(Integer.MIN_VALUE, realValue)` always returns `realValue`.

Think of it as saying: "I've found nothing yet — any real value beats my current best."

```java
best = Math.max(best, alphaBeta(node.left, alpha, beta));
```

- Recursively evaluate the **left child** with the current `alpha` and `beta`.
- `Math.max(best, ...)` keeps `best` as the maximum of what it was before and the left child's result.
- On the first call, this effectively sets `best = left_child_value`.

```java
alpha = Math.max(alpha, best);
```

Update `alpha`: "I've now seen the left child's value. If it's better than the current `alpha`, update `alpha`."

`alpha` represents the best MAX can guarantee. After evaluating the left child, MAX might have a better guarantee than before.

#### THE PRUNING CHECK

```java
if (alpha >= beta) {
    node.right.pruned = true;
} else {
    best = Math.max(best, alphaBeta(node.right, alpha, beta));
}
```

This is the **core of alpha-beta pruning**:

**Condition: `alpha >= beta`**

If the best MAX can guarantee (`alpha`) is **already at least as good as** what MIN will ever allow (`beta`), then:
- MIN will **never** choose to go through this node in the first place.
- Whatever the right child returns, MIN on an ancestor will have already chosen a different path.
- So evaluating the right child is a **waste of time**.
- We mark it as pruned: `node.right.pruned = true`.

**If NOT pruned (`alpha < beta`):**
- The right child might still influence the outcome.
- Recurse into it: `alphaBeta(node.right, alpha, beta)`.
- Update `best` if the right child gives a better MAX value.

```java
node.value = best;
return best;
```

After processing both children (or just left if right was pruned), store the computed best value in `node.value` (so `display()` can show it), and return it to the parent.

### MIN Node Block (Mirror Logic)

```java
} else {
    int best = Integer.MAX_VALUE;
```

`Integer.MAX_VALUE` = `2,147,483,647` (2³¹ - 1). MIN starts with the **largest possible value** as best — because MIN wants to **minimize**, so any real value will be ≤ `Integer.MAX_VALUE`, and `Math.min(Integer.MAX_VALUE, realValue) = realValue`.

```java
best = Math.min(best, alphaBeta(node.left, alpha, beta));
beta = Math.min(best, beta);
```

- Evaluate left child. Keep `best` as the minimum seen so far.
- Update `beta`: MIN now has a tighter guarantee. The upper bound (`beta`) might decrease.

```java
if (alpha >= beta) {
    node.right.pruned = true;
} else {
    best = Math.min(best, alphaBeta(node.right, alpha, beta));
}
```

Same pruning condition: if `alpha >= beta`, prune. From MIN's perspective: "I've already found a value so low that MAX above me would never choose to come here — MAX has `alpha` which is already at least `beta`, something better. So I don't need to evaluate the right child."

```java
node.value = best;
return best;
```

Store and return MIN's best (lowest) value.

### Worked Example with Numbers

Consider this tree (depth=2, 4 leaves: `3, 5, 2, 9`):

```
            MAX: ?
           /      \
       MIN:?      MIN:?
       / \         / \
      3   5       2   9
```

**Step 1:** Call `alphaBeta(root, -∞, +∞)`.

**Step 2:** Root is MAX. `best = -∞`.

**Step 3:** Recurse left: `alphaBeta(left_MIN, -∞, +∞)`.
- Left MIN, `best = +∞`.
- Recurse: `alphaBeta(leaf_3, -∞, +∞)` → returns `3`.
- `best = min(+∞, 3) = 3`. `beta = min(3, +∞) = 3`.
- `alpha=-∞ < beta=3` → no prune.
- Recurse: `alphaBeta(leaf_5, -∞, 3)` → returns `5`.
- `best = min(3, 5) = 3`.
- Left MIN returns `3`.

**Step 4:** Back at root MAX: `best = max(-∞, 3) = 3`. `alpha = max(-∞, 3) = 3`.

**Step 5:** `alpha=3 < beta=+∞` → no prune. Recurse right: `alphaBeta(right_MIN, 3, +∞)`.
- Right MIN, `best = +∞`.
- Recurse: `alphaBeta(leaf_2, 3, +∞)` → returns `2`.
- `best = min(+∞, 2) = 2`. `beta = min(2, +∞) = 2`.
- **CHECK: `alpha=3 >= beta=2`** → **PRUNE!** `right_MIN.right.pruned = true`. Leaf `9` is never evaluated!
- Right MIN returns `2`.

**Step 6:** Back at root MAX: `best = max(3, 2) = 3`. Root value = **3**. ✓

The leaf `9` was never evaluated — pruned! The answer is still correct because MIN on the right would have chosen `min(2,9)=2` anyway, and MAX would have chosen `max(3,2)=3` — the pruning didn't change the answer, just saved computation.

---

## 8. `static void display(...)` — Pretty-Printing the Tree

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

### Why `void`?

This method **doesn't return anything** — its sole job is a **side effect**: printing to the console. `void` = "I produce no return value."

### The 4 Parameters

| Parameter | Type     | Meaning |
|-----------|----------|---------|
| `node`    | `Node`   | The current node to display |
| `prefix`  | `String` | The indentation string built up as we descend the tree |
| `isLast`  | `boolean`| Is this node the **last (rightmost)** child of its parent? |
| `root`    | `boolean`| Is this the root node? (special display treatment) |

### Pruned Node — Early Return Pattern

```java
if (node.pruned) {
    String branch = isLast ? "'-- " : "|-- ";
    System.out.println(prefix + branch + node.name + " (pruned) ");
    return;
}
```

**Early return pattern**: Handle the special case first, then `return` immediately to avoid nested `if-else` complexity.

If a node is pruned:
- Print it with a `(pruned)` label.
- `return` — don't print its children (we never evaluated them anyway).

### The Ternary Operator for Branch Art

```java
String branch = isLast ? "'-- " : "|-- ";
```

This is a **ternary (conditional) expression**: `condition ? valueIfTrue : valueIfFalse`.

In a typical tree visualization:
```
Root A (max) : 3
|-- B(min): 3
|   |-- D : 3 (leaf)
|   '-- E : 5 (leaf)
'-- C(min): 2
    |-- F : 2 (leaf)
    '-- G (pruned)
```

- `|--` means "there are more siblings after me" (not the last child).
- `'--` means "I am the last child" (no more siblings after).

This creates the visual tree structure that makes the output readable.

### Root Special Case

```java
if (root) {
    System.out.println("Root " + node.name + " (max) : " + node.value);
}
```

The root node gets no branch prefix — it's the starting point. It's labeled `"Root"` explicitly.

### Leaf vs. Internal Node Display

```java
if (node.depth == 0) {
    System.out.println(prefix + branch + node.name + " : " + node.value + " (leaf)");
} else {
    String type = node.isMax ? "max" : "min";
    System.out.println(prefix + branch + node.name + "(" + type + ")" + ": " + node.value);
}
```

- **Leaf**: Shows `(leaf)` label — makes it obvious which nodes are terminal.
- **Internal**: Shows `(max)` or `(min)` — tells you whose turn it is at that node.

### Building the `newPrefix`

```java
String newPrefix;
if (root) {
    newPrefix = "";
} else {
    newPrefix = prefix + (isLast ? "    " : "|   ");
}
```

`newPrefix` is what the **children** of this node will use as their prefix. Two cases:

| Parent is last child? | `newPrefix` addition | Visual Effect |
|----------------------|---------------------|---------------|
| `isLast = true`      | `"    "` (4 spaces) | No vertical bar — the parent's branch ended |
| `isLast = false`     | `"|   "` (bar + 3 spaces) | Vertical bar — more siblings will connect here |

This is how the tree drawing maintains the vertical lines connecting sibling subtrees:

```
Root A
|-- B        ← isLast=false → children of B use prefix "|   "
|   |-- D
|   '-- E
'-- C        ← isLast=true → children of C use prefix "    "
    |-- F
    '-- G
```

### Recursive Calls

```java
display(node.left, newPrefix, false, false);
display(node.right, newPrefix, true, false);
```

- Left child: `isLast = false` (there's still the right child after it).
- Right child: `isLast = true` (it's the last child).
- Both: `root = false` (neither is the root).

---

## 9. `static void printPath(...)` — Tracing the Optimal Move

```java
static void printPath(Node node) {
    if (node.depth == 0) {
        System.out.println(node.name);
        return;
    }
    System.out.print((node.name) + " -> ");
    Node next;

    if (!node.left.pruned && node.left.value == node.value) {
        next = node.left;
    } else {
        next = node.right;
    }

    printPath(next);
}
```

### Purpose

After alpha-beta runs, we want to trace the **optimal path**: the sequence of moves that leads to the best outcome. This is the sequence a rational player would follow.

### Base Case

```java
if (node.depth == 0) {
    System.out.println(node.name);
    return;
}
```

When we reach a leaf, print its name with `println` (adds a newline) and stop recursing. The leaf is the **endpoint** of the optimal path.

### `System.out.print` vs `System.out.println`

| Method               | Newline After? | Use Case |
|---------------------|---------------|---------|
| `System.out.print`  | No            | Print intermediate nodes (they connect with ` -> `) |
| `System.out.println`| Yes           | Print the final leaf (ends the line) |

So the output looks like: `A -> B -> D` (all on one line, with `D` ending the line).

### Choosing the Optimal Child

```java
if (!node.left.pruned && node.left.value == node.value) {
    next = node.left;
} else {
    next = node.right;
}
```

The optimal path goes to whichever child **propagated its value upward** (i.e., whose value equals the parent's value).

**Why check `!node.left.pruned` first?**

If the left child was pruned, it never had its `value` computed (or it has a stale/default value). Checking `!node.left.pruned` first uses **short-circuit evaluation**:
- If `node.left.pruned` is `true`, then `!node.left.pruned` is `false`.
- Java immediately knows the whole `&&` is `false` and **does NOT evaluate** `node.left.value == node.value`.
- This prevents comparing an invalid value.

**Why is the left child preferred?**

If both left and right have the same value (unlikely but possible), we go left by default. This is a reasonable tie-breaking rule.

**If left child doesn't match**, go right:
- Either left was pruned, or left's value doesn't equal the parent's value.
- The right child must be the one whose value was chosen.

---

## 10. `public static void main(String[] args)` — The Entry Point

```java
public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);

    System.out.print("Enter depth : ");
    int depth = sc.nextInt();

    int size = (int) Math.pow(2, depth);

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
```

### `public static void main(String[] args)` — Keyword by Keyword

| Keyword       | Why It's There |
|--------------|----------------|
| `public`     | The JVM (Java Virtual Machine) must be able to call `main` from outside the class |
| `static`     | The JVM calls `main` without creating a `practice` object first |
| `void`       | `main` doesn't return a value to the JVM |
| `main`       | **This exact name** is what the JVM looks for as the program's entry point |
| `String[] args` | Command-line arguments passed when running the program (e.g., `java practice hello`) — unused here but **required** by the JVM signature |

### Scanner Setup

```java
Scanner sc = new Scanner(System.in);
```

- `Scanner` reads input from various sources. `System.in` = standard input = the keyboard.
- `sc` is the variable name (short for "scanner").
- `new Scanner(System.in)` creates a new Scanner object connected to the keyboard.

```java
System.out.print("Enter depth : ");
int depth = sc.nextInt();
```

- `System.out.print` (no `ln`) prints without a newline, so the cursor stays on the same line for the user to type.
- `sc.nextInt()` waits for the user to type a number and press Enter, then returns it as an `int`.

### Computing Number of Leaves

```java
int size = (int) Math.pow(2, depth);
```

**Why `2^depth` = number of leaves?**

A **complete binary tree** of depth `d` has:
- `2^0 = 1` node at depth 0 (root, if depth=0).
- `2^1 = 2` nodes at depth 1.
- `2^d` nodes at depth `d` (the leaves).

For depth=3:
```
Level 0:  1 node  (root)
Level 1:  2 nodes
Level 2:  4 nodes
Level 3:  8 nodes ← leaves = 2^3 = 8
```

**Type Casting: `(int)`**

`Math.pow(2, depth)` returns a `double` (floating-point number like `8.0`). We need an `int` to use as an array size. The `(int)` cast **truncates** the decimal part: `(int) 8.0 = 8`.

This is called **explicit type casting** (narrowing conversion). Java won't do it automatically because you could lose precision — so you must explicitly signal "I know what I'm doing."

### Array Creation and Input Loop

```java
int[] leaves = new int[size];
for (int i = 0; i < size; i++) {
    leaves[i] = sc.nextInt();
}
```

- `new int[size]` creates an integer array of `size` elements (default value `0` for all).
- The `for` loop: starts at `i=0`, continues while `i < size`, increments `i` by 1 each iteration.
- `sc.nextInt()` reads each leaf value from the user.

### Reset Counter and Build Tree

```java
counter = 'A';
Node root = buildTree(depth, leaves, 0, true);
```

- **`counter = 'A'`**: Reset the global counter before building the tree. Critical — without this, if `buildTree` were called again in a larger program, names would not start from 'A'.
- `buildTree(depth, leaves, 0, true)`:
  - `depth` = tree depth from user.
  - `leaves` = the values array.
  - `0` = starting index (root is at index 0).
  - `true` = root is a MAX node (MAX player goes first).

### Running Alpha-Beta

```java
int result = alphaBeta(root, Integer.MIN_VALUE, Integer.MAX_VALUE);
```

- Initial `alpha = Integer.MIN_VALUE`: MAX has guaranteed nothing yet — worst possible start.
- Initial `beta = Integer.MAX_VALUE`: MIN has guaranteed nothing yet — worst possible start (for MIN).
- `result` stores the optimal game value.

### Displaying Results

```java
System.out.println("\nGame Tree:");
display(root, "", true, true);
```

- `"\n"` = newline character — adds a blank line before the heading.
- `display(root, "", true, true)`:
  - `""` = empty prefix for the root (no indentation at top level).
  - `true` = root is the last (and only) top-level node → but this controls its children's display.
  - `true` = this IS the root node → special display treatment.

```java
System.out.println("\nOptimal Value: " + result);
System.out.println("\nOptimal Path:");
printPath(root);
```

Print the optimal value and then trace the path from root to the chosen leaf.

### Closing the Scanner

```java
sc.close();
```

**Why close?** `Scanner` wraps an **I/O stream** (System.in). Closing it:
- Releases the I/O resource back to the operating system.
- Good practice to prevent resource leaks.
- Some IDEs and static analysis tools warn if you don't close it.

In a short program that immediately exits, it doesn't matter practically — but in exams, always include `sc.close()` to show good coding habits.

---

## 11. Key Java Concepts — Quick Reference Table

| Concept | Where Used | What It Does |
|---------|-----------|--------------|
| `static` field | `counter` | Shared across all method calls; no object needed |
| `static` method | All methods | Called without creating a `practice` instance |
| `static` inner class | `Node` | Nested class that doesn't need outer class instance |
| Recursion | `buildTree`, `alphaBeta`, `display`, `printPath` | Method calls itself with simpler input until base case |
| Ternary operator `?:` | `display` | `condition ? a : b` — compact if-else for expressions |
| `Integer.MIN_VALUE` | `alphaBeta` MAX block | Smallest int: −2,147,483,648. Starting best for MAX |
| `Integer.MAX_VALUE` | `alphaBeta` MIN block, initial beta | Largest int: 2,147,483,647. Starting best for MIN |
| `Math.max(a, b)` | `alphaBeta`, `buildTree` | Returns the larger of two ints |
| `Math.min(a, b)` | `alphaBeta` | Returns the smaller of two ints |
| `Math.pow(b, e)` | `main` | Returns b^e as a `double` |
| Type casting `(int)` | `main` | Converts `double` to `int`, truncating decimal |
| `Scanner` | `main` | Reads user keyboard input |
| `sc.nextInt()` | `main` | Reads next integer from input |
| `char` arithmetic | `counter++` | Chars are numbers; `++` moves to next character |
| `boolean` flag | `pruned`, `isMax` | Stores true/false state for decisions |
| Early return pattern | `display`, `printPath` | Handle special case first, `return` to avoid deep nesting |
| Short-circuit `&&` | `printPath` | `A && B`: B is only evaluated if A is true |
| `this` keyword | `Node` constructor | Refers to the current object; disambiguates field vs. parameter |
| `new` keyword | `Node node = new Node(...)` | Allocates memory and calls constructor |
| `null` default | `Node.left`, `Node.right` | Reference fields default to `null` if not set |
| `System.out.print` | `printPath` | Prints without newline |
| `System.out.println` | Everywhere else | Prints with newline at end |
| `"\n"` in string | `main` display calls | Inserts blank line in output |

---

## 12. How the Whole Thing Connects — Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          main()                                  │
│                                                                   │
│  1. Read depth and leaf values from user via Scanner             │
│  2. Reset counter = 'A'                                          │
│  3. Call buildTree(depth, leaves, 0, true) → Node root          │
│  4. Call alphaBeta(root, MIN_VALUE, MAX_VALUE) → int result     │
│  5. Call display(root, "", true, true)                           │
│  6. Print result                                                 │
│  7. Call printPath(root)                                         │
│  8. sc.close()                                                   │
└──────────┬───────────────────┬────────────────┬─────────────────┘
           │                   │                │
           ▼                   ▼                ▼
  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐
  │  buildTree()    │  │ alphaBeta()  │  │  display()   │
  │                 │  │              │  │              │
  │ Creates Node    │  │ Traverses    │  │ Prints tree  │
  │ objects forming │  │ the tree;    │  │ with ASCII   │
  │ a binary tree.  │  │ computes     │  │ art using    │
  │                 │  │ optimal      │  │ recursive    │
  │ Recurses until  │  │ values;      │  │ prefix       │
  │ depth==0 (leaf) │  │ prunes       │  │ building.    │
  │                 │  │ branches.    │  │              │
  │ Names nodes     │  │              │  │ Early return │
  │ A, B, C...      │  │ Sets         │  │ for pruned   │
  │ via counter++   │  │ node.value   │  │ nodes.       │
  │                 │  │ & pruned     │  │              │
  └─────────────────┘  └──────────────┘  └──────────────┘
                                                   │
                                                   ▼
                                          ┌──────────────┐
                                          │ printPath()  │
                                          │              │
                                          │ Follows the  │
                                          │ path where   │
                                          │ child.value  │
                                          │ == parent    │
                                          │ .value, and  │
                                          │ child is not │
                                          │ pruned.      │
                                          │              │
                                          │ Prints A ->  │
                                          │ B -> D       │
                                          └──────────────┘
```

### Data Flow

```
User Input (depth + leaf values)
        │
        ▼
  int[] leaves array
        │
        ▼
  buildTree()  ────────────────► Complete Node tree in memory
                                  (all nodes named, leaves valued)
        │
        ▼
  alphaBeta()  ────────────────► Every node.value set,
                                  some node.pruned = true
        │
        ▼
  display()    ────────────────► ASCII tree printed to console
        │
        ▼
  printPath()  ────────────────► Optimal move sequence printed
```

---

## 13. Common Exam Mistakes to Avoid

### 1. Forgetting `counter = 'A'` Before `buildTree`

```java
// ❌ WRONG (counter may be mid-alphabet from a previous call)
Node root = buildTree(depth, leaves, 0, true);

// ✅ CORRECT
counter = 'A';
Node root = buildTree(depth, leaves, 0, true);
```

Without the reset, nodes would be named starting from wherever the counter was — making the output inconsistent.

---

### 2. Wrong Index Formula in `buildTree`

```java
// ❌ WRONG
node.left  = buildTree(depth-1, leaves, index + 1, !isMax);
node.right = buildTree(depth-1, leaves, index + 2, !isMax);

// ✅ CORRECT (heap binary tree indexing)
node.left  = buildTree(depth-1, leaves, index * 2,     !isMax);
node.right = buildTree(depth-1, leaves, index * 2 + 1, !isMax);
```

`index * 2` and `index * 2 + 1` are the **standard formulas** for left and right children in a binary heap. Using `index+1` or `index+2` would access the wrong leaf values.

---

### 3. Wrong Initial Values for `best`

```java
// ❌ WRONG (MAX node starting at MAX_VALUE)
if (node.isMax) {
    int best = Integer.MAX_VALUE;  // MAX wants to maximize, should start LOW!

// ✅ CORRECT
if (node.isMax) {
    int best = Integer.MIN_VALUE;  // Start at the bottom; any real value is better

// ❌ WRONG (MIN node starting at MIN_VALUE)
} else {
    int best = Integer.MIN_VALUE;  // MIN wants to minimize, should start HIGH!

// ✅ CORRECT
} else {
    int best = Integer.MAX_VALUE;  // Start at the top; any real value is lower
```

**Memory trick**: MAX starts at MINIMUM (so anything beats it). MIN starts at MAXIMUM (so anything beats it in the other direction).

---

### 4. Mixing Up Alpha and Beta Updates

```java
// ❌ WRONG (updating beta in MAX block)
if (node.isMax) {
    best = Math.max(best, alphaBeta(node.left, alpha, beta));
    beta = Math.max(beta, best);   // ← WRONG! MAX updates alpha, not beta

// ✅ CORRECT
if (node.isMax) {
    best = Math.max(best, alphaBeta(node.left, alpha, beta));
    alpha = Math.max(alpha, best); // MAX updates alpha

// ❌ WRONG (updating alpha in MIN block)
} else {
    best = Math.min(best, alphaBeta(node.left, alpha, beta));
    alpha = Math.min(best, alpha);  // ← WRONG! MIN updates beta, not alpha

// ✅ CORRECT
} else {
    best = Math.min(best, alphaBeta(node.left, alpha, beta));
    beta = Math.min(best, beta);   // MIN updates beta
```

**Rule**: MAX owns alpha (raises its floor). MIN owns beta (lowers its ceiling).

---

### 5. Forgetting `node.value = best` Before Returning

```java
// ❌ WRONG (value never stored in node — display() shows wrong value)
node.value = best;  // ← this line missing
return best;

// ✅ CORRECT
node.value = best;  // Store so display() and printPath() can use it
return best;
```

Without `node.value = best`, internal nodes have `value = 0` (Java's default for `int`). The `display()` method would show `0` for all internal nodes, and `printPath()` would fail to trace the correct path.

---

### 6. Using `println` Instead of `print` in `printPath` for Intermediate Nodes

```java
// ❌ WRONG (each node on its own line)
System.out.println(node.name + " -> ");
// Output: A ->
//         B ->
//         D

// ✅ CORRECT (all on one line)
System.out.print(node.name + " -> ");
// Output: A -> B -> D
```

`printPath` uses `print` (no newline) for intermediate nodes and `println` only for the final leaf, so the whole path appears on a single line.

---

### 7. Not Checking `pruned` Before Comparing Values in `printPath`

```java
// ❌ WRONG (may compare unpopulated value of pruned left child)
if (node.left.value == node.value) {
    next = node.left;
}

// ✅ CORRECT (check pruned FIRST — short-circuit prevents bad comparison)
if (!node.left.pruned && node.left.value == node.value) {
    next = node.left;
}
```

A pruned node's `value` was never set by `alphaBeta`. Comparing it to the parent's value could give a false match (both might be `0` by Java default). Always check `!pruned` first.

---

### 8. Wrong Initial Call to `alphaBeta`

```java
// ❌ WRONG (starting alpha/beta at 0 — would incorrectly prune early)
int result = alphaBeta(root, 0, 0);

// ✅ CORRECT (worst possible bounds — nothing is pruned due to initial values)
int result = alphaBeta(root, Integer.MIN_VALUE, Integer.MAX_VALUE);
```

Starting alpha at 0 would cause incorrect pruning if any leaf value is negative. Starting beta at 0 would cause incorrect pruning if any leaf value is positive. Always start at the extremes.

---

### 9. Forgetting `sc.close()`

```java
// ✅ Always close your Scanner at the end of main
sc.close();
```

Some graders deduct marks for resource leaks. Close all I/O resources when done.

---

### 10. Confusing `depth` Direction (Root vs. Leaf)

**Exam trap**: Some implementations store depth as the **distance from root** (root = 0). This implementation stores it as **distance to the leaves** (root = max depth, leaves = 0).

```
This program:         Alternative (don't confuse):
  Root: depth=3          Root: depth=0
  ...                    ...
  Leaves: depth=0        Leaves: depth=3
```

The base case `if (depth == 0)` works because **leaves have depth 0** in this implementation. Leaves are reached when depth has been decremented all the way to 0.

---

*End of document. Estimated word count: 5,000+. Estimated line count: 600+.*
*Study this document section by section. Pay special attention to Sections 6, 7, and 13.*
