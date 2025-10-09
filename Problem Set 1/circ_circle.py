import math

def circumference_circle():
    
    radius = float(input("What is the radius of the circle: "))
    circumference = 2*math.pi*radius
    c = round(circumference, 2)
    print(f"The circumference of the circle is {c} cm")

if __name__ == "__main__":
    circumference_circle()