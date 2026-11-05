# Rule-Based Chatbot using Pattern Matching                              
patterns = {                                                             
   "hello": "Hello! How can I help you?",                                
   "hi": "Hi! Nice to meet you.",                                        
   "hey": "Hey! How are you?",                                           
   "how are you": "I am fine. Thank you for asking!",                    
   "what is your name": "I am a simple rule-based chatbot.",             
   "who are you": "I am a chatbot created using Python.",                
   "help": "I can respond to simple greetings and questions.",           
   "thank you": "You're welcome!",                                       
   "thanks": "You're welcome!",                                          
   "bye": "Goodbye! Have a nice day."                                    
}                                                                        
exit_commands = ["bye", "exit", "quit"]                                  
print("===================================")                             
print("  Simple Rule-Based Chatbot")                                     
print("===================================")                             
print("Chatbot: Hello! I am a simple chatbot.")                          
print("Chatbot: Type 'bye', 'exit' or 'quit' to end the conversation.\n")
while True:                                                              
   user_input = input("You: ")                                           
   user_input = user_input.lower().strip()                               
   if user_input in exit_commands:                                       
      print("Chatbot: Goodbye! Have a nice day.")                        
      break                                                              
   matched = False                                                       
   for pattern, response in patterns.items():                            
      if pattern in user_input:                                          
        print("Chatbot:", response)                                      
        matched = True                                                   
        break                                                            
   if matched == False:                                                  
      print("Chatbot: Sorry, I don't understand that.")                  
