# Simple Reflex Agent - Vacuum Cleaner World                             
environment = {                                                          
   "A": "Dirty",                                                         
   "B": "Dirty"                                                          
}                                                                        
location = "A"                                                           
steps = 6                                                                
print("Initial Environment:", environment)                               
print("Initial Vacuum Location:", location)                              
print("\nAgent Execution:\n")                                            
for step in range(1, steps + 1):                                         
   status = environment[location]                                        
   print("Step", step)                                                   
   print("Location:", location)                                          
   print("Room Status:", status)                                         
   if status == "Dirty":                                                 
      action = "Suck"                                                    
      environment[location] = "Clean"                                    
   elif location == "A":                                                 
      action = "Move Right"                                              
      location = "B"                                                     
   else:                                                                 
      action = "Move Left"                                               
      location = "A"                                                     
   print("Action:", action)                                              
   print("Environment:", environment)                                    
   print("-" * 30)                                                       
print("\nFinal Environment:", environment)                               
print("Final Vacuum Location:", location)                                
