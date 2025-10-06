# Elias Daniel Macero Gutierrez
# Credit Score Assessment
# Date 10/05/2025
# Version 3.0.2

AGE_POINTS = [
    (lambda age: age < 20, -10),
    (lambda age: 21 <= age <= 30, 0),
    (lambda age: 31 <= age <= 50, 20),
    (lambda age: age > 50, 25),
]

ADDRESS_POINTS = [
    (lambda yrs: yrs < 1, -5),
    (lambda yrs: 1 <= yrs <= 3, 5),
    (lambda yrs: 4 <= yrs <= 8, 12),
    (lambda yrs: yrs > 8, 20),
]

INCOME_POINTS = [
    (lambda inc: inc < 15000, 0),
    (lambda inc: 15000 <= inc < 25000, 12),
    (lambda inc: 25000 <= inc < 40000, 24),
    (lambda inc: inc >= 40000, 30),
]

JOB_POINTS = [
    (lambda yrs: yrs < 2, -4),
    (lambda yrs: 2 <= yrs <= 4, 8),
    (lambda yrs: yrs > 4, 15),
]

def _points_from_table(value, table):
    for cond, pts in table:
        try:
            if cond(value):
                return pts
        except Exception:
            continue
    # Shouldn't get here; return 0 as safe default
    return 0


def compute_points(age: int, years_at_address: float, annual_income: float, years_at_job: float) -> int:
    """Compute the total points from the provided inputs."""
    total = 0
    total += _points_from_table(age, AGE_POINTS)
    total += _points_from_table(years_at_address, ADDRESS_POINTS)
    total += _points_from_table(annual_income, INCOME_POINTS)
    total += _points_from_table(years_at_job, JOB_POINTS)
    return total


def action_from_points(points: int) -> str:
    """Return recommended card action based on points total."""
    if points < 20:
        return "No card"
    if 21 <= points <= 35:
        return "Card with $500 limit"
    if 36 <= points <= 60:
        return "Card with $2000 limit"
    if points > 60:
        return "Card with $5000 limit"
    # Edge case: exactly 20 points (not covered above)
    if points == 20:
        return "Card with $500 limit"
    return "No card"


def estimate_credit_score(points: int, min_points: int = -19, max_points: int = 90) -> int:
    """Estimate a 300-850 credit score by linearly scaling points between min_points and max_points."""
    # Clamp points
    p = max(min_points, min(max_points, points))
    # scale to 300..850
    ratio = (p - min_points) / (max_points - min_points)
    score = int(round(300 + ratio * (850 - 300)))
    return score


def score_category(score: int) -> str:
    if score >= 750:
        return "Excellent"
    if score >= 700:
        return "Good"
    if score >= 650:
        return "Fair"
    return "Poor"


def assess_score_interactive() -> None:
    """Interactively prompt user for inputs, compute points, estimated score, and print recommendations."""
    try:
        age = int(input("Enter your age (years): ").strip())
        years_addr = float(input("Years at current address: ").strip())
        income = float(input("Annual income (e.g., 25000): ").strip())
        years_job = float(input("Years at same job: ").strip())
    except (ValueError, TypeError):
        print("Invalid input. Please enter numeric values for age, years, and income.")
        return

    points = compute_points(age, years_addr, income, years_job)
    est_score = estimate_credit_score(points)
    category = score_category(est_score)
    action = action_from_points(points)

    print("\nAssessment results:")
    print(f"  Points total: {points}")
    print(f"  Estimated credit score (approx): {est_score}")
    print(f"  Category: {category}")
    print(f"  Recommended action: {action}")


if __name__ == "__main__":
    assess_score_interactive()