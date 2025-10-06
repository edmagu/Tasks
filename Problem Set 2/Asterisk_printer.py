def printer():
    try:
        user_input = int(input("How many asterisks would you like to print: "))
    except (ValueError, TypeError):
        print("Invalid input. Please enter one number.")
        exit()
    for i in range(user_input):
        print("*")

if __name__ == "__main__":
    printer()
