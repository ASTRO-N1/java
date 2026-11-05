# Water Jug Problem using DFS                                            
CAPACITY_A = 4                                                           
CAPACITY_B = 3                                                           
GOAL = 2                                                                 
def get_next_states(state):                                              
   a, b = state                                                          
   states = []                                                           
   states.append(((CAPACITY_A, b), "Fill Jug A"))                        
   states.append(((a, CAPACITY_B), "Fill Jug B"))                        
   states.append(((0, b), "Empty Jug A"))                                
   states.append(((a, 0), "Empty Jug B"))                                
   amount = min(a, CAPACITY_B - b)                                       
   states.append(((a - amount, b + amount), "Pour A -> B"))              
   amount = min(b, CAPACITY_A - a)                                       
   states.append(((a + amount, b - amount), "Pour B -> A"))              
   return states                                                         
def dfs():                                                               
   initial = (0, 0)                                                      
   stack = [initial]                                                     
   visited = set()                                                       
   visited.add(initial)                                                  
   parent = {initial: None}                                              
   action = {initial: "Initial State"}                                   
   while stack:                                                          
      current = stack.pop()                                              
      if current[0] == GOAL or current[1] == GOAL:                       
        path = []                                                        
        while current is not None:                                       
           path.append((current, action[current]))                       
           current = parent[current]                                     
        path.reverse()                                                   
        return path                                                      
      next_states = get_next_states(current)                             
      for next_state, move in next_states:                               
        if next_state not in visited:                                    
           visited.add(next_state)                                       
           parent[next_state] = current                                  
           action[next_state] = move                                     
           stack.append(next_state)                                      
   return None                                                           
solution = dfs()                                                         
if solution:                                                             
   print("Water Jug Problem using DFS")                                  
   print("Jug A Capacity =", CAPACITY_A, "liters")                       
   print("Jug B Capacity =", CAPACITY_B, "liters")                       
   print("Goal =", GOAL, "liters")                                       
   print("\nSolution Path:\n")                                           
   for step, (state, move) in enumerate(solution):                       
      print("Step", step)                                                
      print("Action:", move)                                             
      print("Jug A:", state[0], "liters")                                
      print("Jug B:", state[1], "liters")                                
      print("-" * 30)                                                    
else:                                                                    
   print("No solution found.")                                           
