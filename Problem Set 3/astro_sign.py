from typing import Tuple


def _month_str_to_int(s: str):
    """Convert a month name or abbreviation to month number (1-12).

    Returns None if the month is not recognized.
    """
    s = s.strip().lower()
    months = {
        'january': 1, 'jan': 1,
        'february': 2, 'feb': 2,
        'march': 3, 'mar': 3,
        'april': 4, 'apr': 4,
        'may': 5,
        'june': 6, 'jun': 6,
        'july': 7, 'jul': 7,
        'august': 8, 'aug': 8,
        'september': 9, 'sep': 9, 'sept': 9,
        'october': 10, 'oct': 10,
        'november': 11, 'nov': 11,
        'december': 12, 'dec': 12,
    }
    return months.get(s)


ZODIAC_RANGES = [
    ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)),
    ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)),
    ("Sagittarius", (11, 22), (12, 21)),
    ("Capricorn", (12, 22), (1, 19)),
    ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)),
]


def _date_ge(a: Tuple[int, int], b: Tuple[int, int]):
    """Return True if date a (m,d) is greater than or equal to date b (m,d) in calendar order ignoring year."""
    am, ad = a
    bm, bd = b
    return (am, ad) >= (bm, bd)


def _date_le(a: Tuple[int, int], b: Tuple[int, int]):
    am, ad = a
    bm, bd = b
    return (am, ad) <= (bm, bd)


def determine_zodiac(month: int, day: int):
    """Return zodiac sign name for a given month (1-12) and day, or None if not found."""
    target = (month, day)
    for name, start, end in ZODIAC_RANGES:

        if start[0] < end[0] or (start[0] == end[0] and start[1] <= end[1]):
            if _date_ge(target, start) and _date_le(target, end):
                return name
        else:

            if _date_ge(target, start) or _date_le(target, end):
                return name
    return None


def astro_sign():
    """Interactive function: ask for month and day and print the zodiac sign.

    Returns the sign string (or None on invalid input) so it can be tested.
    """
    try:
        month_input = input("Enter your birth month (e.g., March): ").strip()
        day = int(input("Enter your birth day (1-31): ").strip())
    except (ValueError, TypeError):
        print("Invalid input. Please enter a valid month and integer day.")
        return astro_sign()

    month = _month_str_to_int(month_input)
    if month is None:
        print(f"Unrecognized month: '{month_input}'. Please enter a full month name or 3-letter abbreviation.")
        return astro_sign()


    days_in_month = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if day < 1 or day > days_in_month.get(month, 31):
        print(f"Invalid day '{day}' for month {month_input}.")
        return astro_sign()

    sign = determine_zodiac(month, day)
    if sign:
        print(f"Your zodiac sign is: {sign}.")
    else:
        print("Could not determine zodiac sign for the given date.")
    return sign


if __name__ == "__main__":
    astro_sign()