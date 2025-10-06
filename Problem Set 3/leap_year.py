def leap_year():
    try:
        year = int(input("Enter a year (e.g., 2024): "))
        if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
            print("Leap Year")
        else:
            print("Not a Leap Year")
    except ValueError:
        print("Invalid input. Please enter a valid year.")

if __name__ == "__main__":
    leap_year()