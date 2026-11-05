from collections import deque                                            
                                                                         
grid = [                                                                 
   [0, 0, 0, 0, 0],                                                      
   [0, 1, 1, 1, 0],                                                      
   [0, 0, 0, 1, 0],                                                      
   [0, 1, 0, 0, 0],                                                      
   [0, 0, 0, 0, 0]                                                       
]                                                                        
start = (0, 0)                                                           
goal = (4, 4)                                                            
directions = [                                                           
   (-1, 0), # Up                                                         
   (1, 0), # Down                                                        
   (0, -1), # Left                                                       
   (0, 1) # Right                                                        
]                                                                        
def bfs(grid, start, goal):                                              
   queue = deque()                                                       
   queue.append(start)                                                   
   visited = set()                                                       
   visited.add(start)                                                    
   parent = {}                                                           
   parent[start] = None                                                  
   rows = len(grid)                                                      
   cols = len(grid[0])                                                   
   while queue:                                                          
      current = queue.popleft()                                          
      if current == goal:                                                
        path = []                                                        
        while current is not None:                                       
           path.append(current)                                          
           current = parent[current]                                     
        path.reverse()                                                   
        return path                                                      
      for dr, dc in directions:                                          
        new_row = current[0] + dr                                        
        new_col = current[1] + dc                                        
        if (0 <= new_row < rows and                                      
             0 <= new_col < cols and                                     
             grid[new_row][new_col] == 0):                               
           neighbor = (new_row, new_col)                                 
           if neighbor not in visited:                                   
             visited.add(neighbor)                                       
             parent[neighbor] = current                                  
             queue.append(neighbor)                                      
   return None                                                           
path = bfs(grid, start, goal)                                            
if path:                                                                 
   print("Robot Path Planning using BFS")                                
   print("\nGrid:")                                                      
   for row in grid:                                                      
      print(row)                                                         
   print("\nStart Position:", start)                                     
   print("Goal Position:", goal)                                         
   print("\nShortest Path:")                                             
   for step, position in enumerate(path):                                
      print("Step", step, ":", position)                                 
   print("\nPath Length:", len(path) - 1)                                
else:                                                                    
   print("No path found.")                                               
