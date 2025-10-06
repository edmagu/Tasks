def printer():
    try:
        user_input = int(input("How many asterisks would you like to print: "))
    except (ValueError, TypeError):
        print("Invalid input. Please enter one number.")
        exit()
    if user_input <= 0:
        print("Please enter a positive integer greater than 0.")
        return

    # Print a square: user_input rows of user_input asterisks
    for _ in range(user_input):
        print("*" * user_input)

if __name__ == "__main__":
    printer()