from collections import deque                                            
                                                                         
def get_successors(state):                                               
   successors = []                                                       
   for source in range(3):                                               
      if len(state[source]) == 0:                                        
        continue                                                         
      disk = state[source][-1]                                           
      for destination in range(3):                                       
        if source == destination:                                        
           continue                                                      
        if (len(state[destination]) == 0 or                              
             state[destination][-1] > disk):                             
           new_state = [list(rod) for rod in state]                      
           new_state[source].pop()                                       
           new_state[destination].append(disk)                           
           new_state = tuple(tuple(rod) for rod in new_state)            
           successors.append((new_state, source, destination, disk))     
   return successors                                                     
def display_state(state):                                                
   print("Rod A:", list(state[0]))                                       
   print("Rod B:", list(state[1]))                                       
   print("Rod C:", list(state[2]))                                       
   print()                                                               
def tower_of_hanoi(n):                                                   
   initial_state = (tuple(range(n, 0, -1)), (), ())                      
   goal_state = ((), (), tuple(range(n, 0, -1)))                         
   queue = deque()                                                       
   queue.append((initial_state, []))                                     
   visited = set()                                                       
   visited.add(initial_state)                                            
   while queue:                                                          
      current_state, path = queue.popleft()                              
      if current_state == goal_state:                                    
        return path + [(current_state, "Goal")]                          
      for successor, source, destination, disk in get_successors(current_state):
        if successor not in visited:                                     
           visited.add(successor)                                        
           move = (                                                      
             f"Move disk {disk} from "                                   
             f"Rod {'ABC'[source]} to Rod {'ABC'[destination]}"          
           )                                                             
           new_path = path + [(current_state, move)]                     
           queue.append((successor, new_path))                           
   return None                                                           
n = 3                                                                    
solution = tower_of_hanoi(n)                                             
if solution:                                                             
   print("Tower of Hanoi - State Space Search")                          
   print("Number of disks:", n)                                          
   print("\nSolution Path:\n")                                           
   initial_state = solution[0][0]                                        
   print("Initial State:")                                               
   display_state(initial_state)                                          
   for i in range(len(solution) - 1):                                    
      state, move = solution[i]                                          
      print("Step", i + 1, ":", move)                                    
      next_state = solution[i + 1][0]                                    
      display_state(next_state)                                          
                                                                         
                                                                         
                                                                         
                                                                         
                                                                         
   print("Goal State Reached!")                                          
else:                                                                    
   print("No solution found.")                                           
