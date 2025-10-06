# Elias Daniel Macero Gutierrez
# Random Number Guessing Game
# Date 10/12/2025
# Version 1.2.0

import random

def rand_num() -> int:
    """Return a random integer between 1 and 10 (inclusive)."""
    return random.randint(1, 10)


def main() -> None:
    """Play a simple guessing game: user guesses until they find the secret number.

    The user may type 'exit' (case-insensitive) to quit. The function validates
    inputs and reports number of attempts when the user guesses correctly.
    """
    secret = rand_num()
    guesses = 0
    try:
        while True:
            raw = input("Guess a number between 1 and 10 (or type 'exit' to quit): ")
            if raw.lower() == 'exit':
                print("Exiting the game. Goodbye!")
                break

            # Try to parse the guess as an integer
            try:
                user_guess = int(raw)
            except ValueError:
                print("Invalid input. Please enter an integer between 1 and 10, or 'exit'.")
                continue

            if user_guess < 1 or user_guess > 10:
                print("Your guess is out of range, try again.")
                continue

            guesses += 1
            if user_guess == secret:
                print(f"You guessed the correct number in {guesses} attempt(s)!")
                break
            else:
                # Provide a hint to make the game friendlier
                hint = 'lower' if user_guess > secret else 'higher'
                print(f"Nope — try {hint}! (Attempts: {guesses})")
    except KeyboardInterrupt:
        print("\nExiting the game. Goodbye!")


if __name__ == "__main__":
    main()