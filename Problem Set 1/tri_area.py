import math # >:D

def tri_area():

    tri_height = int(input("What is the height of the traingle in meters: "))
    tri_base = int(input("How long is the base of the triangle in meters: "))
    
    try:
        area = (tri_height*tri_base)/2
        print(f"The area of the triangle is {area}m^2.")
    except ValueError:
        print("These values are inacceptable, input whole numbers.")

if __name__ == "__main__":
	tri_area()
	