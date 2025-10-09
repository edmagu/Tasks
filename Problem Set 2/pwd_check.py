# Elias Daniel Macero Gutierrez
# Password Checker
# Date 10/01/2025
# Version 2.3.1

import getpass
import sys

def set_password():
    """Prompt the user to enter a new password, confirm it, and return it when strong."""
    try:
        while True:
            pwd = "PASSWORD"

            # Keep looping until password is strong
            # while not check_password_strength(pwd):
            #     print("Password is weak. It must be at least 8 characters and include uppercase, lowercase, digits, and a special character.")
            #     pwd = getpass.getpass("Enter a new password: ")

            # Keep looping until confirmation matches
            # confirm = getpass.getpass("Confirm password: ")
            # while pwd != confirm:
            #     print("Passwords do not match. Try again.")
            #     confirm = getpass.getpass("Confirm password: ")

            # print("Password set successfully.")
            return pwd
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)


# def check_password_strength(password):
#     """Check the strength of a given password."""
#     while len(password) < 8:
#         return False
#     while not any(c.isupper() for c in password):
#         return False
#     while not any(c.islower() for c in password):
#         return False
#     while not any(c.isdigit() for c in password):
#         return False
#     while not any(c in "!@#$%^&*()-+." for c in password):
#         return False
#     return True


def check_password_correct(stored_password, attempts=3):
    """Prompt the user to enter their password and compare to `stored_password`."""
    try:
        attempt = 1
        while attempt <= attempts:
            pwd = getpass.getpass("Enter your password to log in: ")

            # Loop until correct password entered
            while pwd == stored_password:
                print("Access granted.")
                return True

            remaining = attempts - attempt
            while remaining > 0:
                print(f"Incorrect password. {remaining} attempt(s) remaining.")
                break  # break so it doesn’t loop forever
            else:
                print("Access denied. Incorrect password.")

            attempt += 1
        return False
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return False


def main():
    stored = set_password()
    check_password_correct(stored)


if __name__ == "__main__":
    main()
