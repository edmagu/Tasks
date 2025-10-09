# Elias Daniel Macero Gutierrez
# Animal Food Simulation
# Date 09/29/2025
# Version 1.2.3

import time
from decimal import Decimal
def drop_ball():
    bounces = 0
    height = float(input("Enter the initial height of the ball (in meters): "))
    while height > 0.1:
        print(f"The ball is at height: {Decimal.from_float(height)} meters")
        height = height * 2/3
        bounces += 1
        time.sleep(0.5)  # Pause for a second to simulate time passing

    if height <= 0.1:
        print("The ball has stopped bouncing.")
        print(f"Total bounces: {bounces}")

if __name__ == "__main__":
    drop_ball()