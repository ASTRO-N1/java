environment={
    "A":"dirty",
    "B":"dirty"
}
location="A"
print("intial environment:",environment)
print("intial location:",location)

print("\n Agent execution:\n")
step=1
while "dirty" in environment.values():
    status=environment[location]

    print("step",step)
    print("Location:", location)
    print("Room Status:", status)

    if status=="dirty":
        action = "Suck"
        environment[location] = "Clean"

    elif location=="A":
        action="move right"
        location="B"

    else:
        action="move left"
        location="A"        


    
    print("Action:", action)
    print("Environment:", environment)
    print("-" * 30)

    step += 1

print("\nFinal Environment:", environment)
print("Final Vacuum Location:", location)