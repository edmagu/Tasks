# Elias Daniel Macero Gutierrez
# Coin Toss Counter
# Date 10/12/2025
# Version 1.4.15
import random
import sys

def coin_flipper():
    """Interactive coin toss game that prints counter vs toss number."""
    # Ask whether user wants to play
    play = input("Do you want to play the coin toss game? (yes/no): ").strip().lower()
    if play not in ("yes", "y"):
        print("Coin toss cancelled.")
        return

    # Ask for number of tosses (positive integer)
    while True:
        try:
            flips = int(input("Enter the number of tosses (positive integer): ").strip())
            if flips <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    counter = 0      # counter increments for heads, decrements for tails
    heads = 0
    tails = 0

    # Print a small table header
    print("\nToss\tResult\tCounter")
    # Simulate tosses and update/print the counter after each toss
    for i in range(1, flips + 1):
        # Randomly choose head or tail
        result = "H" if random.choice([True, False]) else "T"
        if result == "H":
            heads += 1
            counter += 1
        else:
            tails += 1
            counter -= 1
        # Show toss number, result, and current counter value
        print(f"{i}\t{result}\t{counter}")

    # Summary
    print("\nSummary:")
    print(f"Total tosses: {flips}")
    print(f"Heads: {heads}")
    print(f"Tails: {tails}")
    print(f"Final counter: {counter}")

if __name__ == "__main__":
    try:
        coin_flipper()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)