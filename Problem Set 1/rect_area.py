# Elias Daniel Macero Gutierrez
# Area of a rectangle calculator
# 2025-09-26
# Version 1.0.5

def calculator():
    h_str = 0
    w_str = 0
    try:
        h_str = float(input("Height of rectangle in meters: ")) if h_str <= 0 else None
        w_str = float(input("Width of rectangle in meters: ")) if w_str <= 0 else None

# Checks if it's a negative and if it is prompts the user to input a positive value
        if h_str or w_str == None:
            print("The values have to be positive\n")
            return calculator()
# Does the area calculation
        area = h_str * w_str
        print(f"The area of the rectangle is {round(area, 2)} m^2")
# Basic error checking if it's not a number or if it is typed correctly  
    except (ValueError, TypeError):
        print("This input doesn't work, it's a calculator you put real numbers (mathematical term) in it.")
        return calculator()
if __name__ == "__main__":
    calculator()