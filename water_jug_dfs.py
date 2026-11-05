# Water Jug Problem using DFS

A = 4
B = 3
GOAL = 2

def dfs():
    stack = [(0, 0)]
    visited = set()
    parent = {(0, 0): None}
    action = {(0, 0): "Initial State"}

    while stack:
        a, b = stack.pop()
        current = (a, b)

        if a == GOAL or b == GOAL:
            path = []

            while current is not None:
                path.append((current, action[current]))
                current = parent[current]

            path.reverse()
            return path

        # Generate possible next states
        next_states = [
            ((A, b), "Fill A"),
            ((a, B), "Fill B"),
            ((0, b), "Empty A"),
            ((a, 0), "Empty B"),
            ((a - min(a, B-b), b + min(a, B-b)), "Pour A to B"),
            ((a + min(b, A-a), b - min(b, A-a)), "Pour B to A")
        ]

        for state, move in next_states:
            if state not in visited:
                visited.add(state)
                parent[state] = current
                action[state] = move
                stack.append(state)

    return None


solution = dfs()

if solution:
    print("Water Jug Problem using DFS")

    for step, (state, move) in enumerate(solution):
        print("Step:", step)
        print("Action:", move)
        print("Jug A:", state[0], "litres")
        print("Jug B:", state[1], "litres")
        print("--------------------")

else:
    print("No solution found")