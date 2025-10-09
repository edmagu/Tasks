# Elias Daniel Macero Gutierrez
# Postage Calculator
# Date 10/12/2025
# Version 1.0.7
from math import ceil


def calculate_postage(weight_grams):
    if weight_grams <= 0:
        raise ValueError("Weight must be a positive number of grams")

    if weight_grams <= 30:
        return 0.48
    if weight_grams <= 50:
        return 0.70
    if weight_grams <= 100:
        return 0.90

    # weight > 100g
    extra = weight_grams - 100
    # number of 50g increments (round up)
    increments = ceil(extra / 50)
    return 0.90 + increments * 0.18


def postage():

    try:
        raw = input("Enter the weight of the letter in grams: ").strip()
        weight = float(raw)
    except (ValueError, TypeError):
        print("Invalid input. Please enter a numeric weight in grams.")
        return 0

    try:
        price = calculate_postage(weight)
    except ValueError as e:
        print(e)
        return 0

    print(f"The postage price is: ${price:.2f}")
    return price


if __name__ == "__main__":
    postage()