import math # Calculates the perimeter of a rectangle basedn on user input 

def rect_perimeter():

    height_rect = int(input("What is the height of the rectangle in meters: ")) 
    width_rect = int(input("What is the width of the rectangle in meters: "))

    try:
        h = height_rect
        w = width_rect
        perimeter = 2*h+2*w
        print(f"The perimeter is {perimeter} m")
    except ValueError:
        print("These values are inacceptable, try again")

if __name__ == "__main__":
    rect_perimeter()