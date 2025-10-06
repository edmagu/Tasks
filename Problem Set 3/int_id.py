# Elias Daniel Macero Gutierrez
# Integer Identifier
# Date 10/12/2025
# Version 2.1



def integer_identifier(num: int) -> str:
    """Return whether an integer is Positive, Negative, or Zero."""
    if num > 0:
        return "Positive"
    elif num < 0:
        return "Negative"
    else:
        return "Zero"

def even_odd_identifier(num: int) -> str:
    """Return whether an integer is Even or Odd."""
    return "Even" if num % 2 == 0 else "Odd"

def int_id() -> None:
    """Prompt the user for an integer and print its sign and parity."""
    try:
        user_input = int(input("Enter an integer: "))
    except (ValueError, TypeError):
        print("Invalid input. Please enter one integer.")
        return int_id()

    sign = integer_identifier(user_input)
    parity = even_odd_identifier(user_input)
    print(f"The number {user_input} is {sign} and {parity}.")


if __name__ == "__main__":
    int_id()
