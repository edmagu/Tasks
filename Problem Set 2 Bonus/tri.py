# Elias Daniel Macero Gutierrez
# Triangular * Printer
# Date 09/29/2025
# Version 1.0.5

def print_triangular():
    n = int(input("Enter the number of rows for the triangular pattern (positive integer): "))
    if n < 1:
        print("Please enter a positive integer greater than 0.")
        return

    for i in range(1, n + 1):
        # Print leading spaces
        print(' ' * (n - i), end='')
        # Print stars
        print('* ' * i)

if __name__ == "__main__":
    print_triangular()

