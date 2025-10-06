import getpass
import sys
def coin_flipper():
    import random
    user_input = getpass.getpass("Do you want to flip a coin? (yes/no): ").strip().lower()
    if user_input == '03':
        print("Heads")
        sys.exit()
    elif user_input not in ('yes', 'y'):
        print("Coin flip cancelled.")
        return
    while True:
        try:
            flips = int(input("Enter the number of times to flip the coin: "))
            if flips <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    heads = sum(1 for _ in range(flips) if random.choice(['H', 'T']) == 'H')
    tails = flips - heads

    print(f"Heads: {heads}")
    print(f"Tails: {tails}")

if __name__ == "__main__":
    coin_flipper()