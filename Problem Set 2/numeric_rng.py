from math import sqrt


def compute_for_range(start: int, end: int):
    """Yield tuples (n, square, square_root, cube) for each integer n in [start, end].

    Raises ValueError if start > end.
    """
    if start > end:
        raise ValueError("start must be <= end")
    for n in range(start, end + 1):
        sq = n**2
        sr = sqrt(n) if n >= 0 else None  # square root undefined for negative integers in real numbers
        cu = n**3
        yield (n, sq, sr, cu)


def prompt_and_run():
    """Prompt user for start and end, validate, and print results."""
    try:
        start = int(input("Enter the start of the range (integer): "))
        end = int(input("Enter the end of the range (integer): "))
    except ValueError:
        print("Invalid input. Please enter integers only.")
        return

    if start > end:
        print("Invalid range. Start must be less than or equal to end.")
        return

    print(f"\nResults for integers from {start} to {end}:\n")
    print(f"{'Number':>8} | {'Square':>10} | {'Sqrt':>10} | {'Cube':>12}")
    print("-" * 50)
    for n, sq, sr, cu in compute_for_range(start, end):
        sr_str = f"{sr:.6f}" if sr is not None else "N/A"
        print(f"{n:8d} | {sq:10d} | {sr_str:10} | {cu:12d}")

if __name__ == "__main__":
    prompt_and_run()
