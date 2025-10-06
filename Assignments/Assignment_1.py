# Assignment 1 - Menu driven program using if statements and loops
# Author: Elias Daniel Macero Gutierrez
# This program displays a menu to the user and performs one of:
    # 1) display a random ASCII art, 2) display a square of stars (n), 
    # 3) display a triangle of n lines, or 4) exit the program.
    # After completing a selection the user is asked whether to run again.
# Version 2.1
import random
import sys

def display_header():
    """Print a simple program header."""
    print("=" * 50)
    print("Assignment 1 - If statements and loops".center(50))
    print("Select from the menu to perform an action".center(50))
    print("=" * 50)

def random_ascii_art():
    """Choose and print one of three ASCII drawings at random."""
    arts = [
        r"""
         /\_/\ 
        ( o.o )
         > ^ <
        """,
        r"""
          /\
         /  \
        |    |
        |____|
        """,
        r"""
         __
        /  \
       |    |
       |____|
        """,
    ]
    art = random.choice(arts)  # pick exactly one art
    print(art)

def square_stars(n: int):
    """Print an n x n square made of '*' characters."""
    for i in range(n):
        print(' * ' * n)

def triangle_stars(n: int):
    """Print a right-angled triangle of '*' with n lines."""
    for i in range(1, n + 1):
        # Print leading spaces
        print(' ' * (n - i), end='')
        # Print stars
        print('* ' * i)

def get_positive_int(prompt: str) -> int:
    """Prompt until the user enters a positive integer; returns it."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if val <= 0:
                print("Please enter a positive integer.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

def menu() -> None:
    """Show menu, perform selection, and optionally repeat or exit."""
    while True:
        display_header()
        print("Please select one of the following:")
        print("1) Display a random ASCII Art")
        print("2) Display a square of stars of n size")
        print("3) Display a triangle of n lines")
        print("4) Exit")
        choice = input("Enter choice (1-4): ").strip()

        # Handle choices with if statements
        if choice == '1':
            # Show one random ASCII art
            random_ascii_art()
        elif choice == '2':
            # Ask for size and print square
            n = get_positive_int("Enter the size n for the square: ")
            square_stars(n)
        elif choice == '3':
            # Ask for size and print triangle
            n = get_positive_int("Enter the number of lines for the triangle: ")
            triangle_stars(n)
        elif choice == '4':
            # Exit the program using sys.exit as requested
            print("Exiting program. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection. Please choose 1, 2, 3 or 4.")
            continue

        # After completing an action ask user whether to restart
        while True:
            again = input("Do you want to make another selection? (y/n): ").strip().lower()
            if again in ('y', 'yes'):
                break  # break inner loop to show menu again
            if again in ('n', 'no'):
                print("Exiting program. Goodbye!")
                sys.exit(0)
            print("Please answer 'y' or 'n'.")

def main():
    try:
        menu()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print("\nProgram interrupted. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()


