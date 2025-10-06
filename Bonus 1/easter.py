import math


def easter():
    try:
        year = int(input("What year do you want to find easter for: "))
    except (ValueError, TypeError):
        print("Invalid input, please input a whole number.")
        exit()

    a = year % 19
    b = year/ 100
    c = year % 100
    d = b / 4
    e = b % 4
    f = (8*b + 13) / 25
    g = (19*a + b - d - f + 15) % 30
    h = (a + 11*g) / 319
    i = c / 4
    j = c % 4
    m = (2*e + 2*i - g - h - j + 32) % 7
    month = (g - h + m + 90) / 25
    day = (g - h + m + month + 19) % 32

    print(f"The month is {round(month)}, the day is {round(day)} in the year {year}")

if __name__ == "__main__":
    easter()
