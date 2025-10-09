def printer():
    try:
        user_input = int(input("How many asterisks would you like to print: "))
    except (ValueError, TypeError):
        print("Invalid input. Please enter one number.")
        exit()
    print("*" * user_input, "\n")

if __name__ == "__main__":
    printer()