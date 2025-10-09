import math
def temp():
    try:
        user_option = str(input("Would you like to convert from Celsius to Fahrenheit (C) or from Fahrenheit to Celsius (F)? ")).strip().upper()
        if user_option == "C" or user_option == "CELSIUS":
            CF()
        elif user_option == "F" or user_option == "FAHRENHEIT":
            FC()
    except (ValueError, TypeError):
        print("These values are inacceptable, try again")

def CF():
    try:
        C = float(input("What is the temperature in Celsius: "))
        F = (C*1.8)+32
        print(f"The temperature in Fahrenheit is {round(F, 2)}°F")
    except (ValueError, TypeError):
        print("These values are inacceptable, try again")
        temp()

def FC():
    try:
        F = float(input("What is the temperature in Fahrenheit: "))
        C = 5/9*(F-32)
        print(f"The temperature in Celsius is {round(C)}°C")
    except (ValueError, TypeError):
        print("These values are inacceptable, try again")
        temp()
    
if __name__ == "__main__":
    temp()