# Ball Height Approximation
# Elias Daniel Macero Gutierrez
# Date 09/29/2025
# Version 1.0.3

animals = 10
food = 1000

import time
hour = 0
def hourly():
    global animals, food, hour, user
    user = input("Do the animals eat the food? (y/n): ").strip().lower()

    while animals < food:
        hour += 1
        animals *= 2
        """Darn you Nicole"""
        if user == 'y':
            food += 4000; food -= animals
        elif user == 'n':
            food += 4000
        print(f"Animals: {animals:8d} | Food: {food:8d} | Hour: {hour:2d}")
        
        time.sleep(1)  
    if animals > food:
        print("The animals have surpassed their food supply and will starve. The end.")
        print(f"Final count - Animals: {animals} | Food: {food}")
        print(f"It took {hour} hours.")

if __name__ == "__main__":
    hourly()