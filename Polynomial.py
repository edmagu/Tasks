# Polynomial grapher with user-friendly parser that supports multiple terms with same power.
# Author: Elias Daniel Macero Gutierrez
# Version: 1.0
import re

def _parse_polynomial_input(s: str):
    """Parse a user-friendly polynomial string into a list of coefficients
    highest-degree first.

    Supports multiple occurrences of the same power (they are summed), examples:
      - "2x^2 - 3x + 1"
      - "x^3 + 2x^3 - x + 5"  -> x^3 terms summed to 3x^3
      - "-x^3 + 4x - 7"
      - "x^2 + x + 1"
      - "2 -3 1"   (space or comma separated coefficients, highest-degree first)
      - "2, -3, 1"

    Returns a list of floats [a_n, ..., a_0].
    Raises ValueError on parse failure.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    s = s.strip()
    if not s:
        raise ValueError("Empty input")

    # If input looks like plain coefficients (no 'x' present) parse as list
    if 'x' not in s.lower():
        parts = re.split(r'[,\s]+', s)
        try:
            coeffs = [float(p) for p in parts if p != '']
        except ValueError:
            raise ValueError("Could not parse coefficients list; use numbers separated by space or comma.")
        if not coeffs:
            raise ValueError("No coefficients found")
        return coeffs

    # Normalize: remove whitespace, unify exponent operator to '^'
    t = s.replace('**', '^')
    t = re.sub(r'\s+', '', t)

    # Make splitting easier: ensure leading sign handled, convert binary '-' into '+-'
    if t.startswith('-'):
        t = '0' + t
    t = t.replace('-', '+-')
    tokens = [tok for tok in t.split('+') if tok != '']

    terms = {}  # exponent -> coefficient (float)
    for tok in tokens:
        tok_low = tok.lower()
        if 'x' in tok_low:
            i = tok_low.index('x')
            coeff_part = tok_low[:i]
            exp_part = tok_low[i+1:]  # may be '', or '^2'
            # coefficient
            if coeff_part in ('', '+'):
                coeff = 1.0
            elif coeff_part == '-':
                coeff = -1.0
            else:
                try:
                    coeff = float(coeff_part)
                except ValueError:
                    raise ValueError(f"Invalid coefficient in term '{tok}'")
            # exponent
            if exp_part == '':
                exp = 1
            else:
                if exp_part.startswith('^'):
                    try:
                        exp = int(exp_part[1:])
                    except ValueError:
                        raise ValueError(f"Invalid exponent in term '{tok}'")
                else:
                    raise ValueError(f"Invalid exponent syntax in term '{tok}' (use ^ or omit)")
        else:
            # constant term
            try:
                coeff = float(tok_low)
            except ValueError:
                raise ValueError(f"Invalid constant term '{tok}'")
            exp = 0

        terms[exp] = terms.get(exp, 0.0) + coeff  # sum multiple terms of same power

    if not terms:
        raise ValueError("No terms parsed from polynomial")

    max_exp = max(terms.keys())
    coeffs = [terms.get(e, 0.0) for e in range(max_exp, -1, -1)]
    # remove leading zeros if any (but keep a single zero for the zero polynomial)
    while len(coeffs) > 1 and abs(coeffs[0]) < 1e-12:
        coeffs.pop(0)
    return coeffs


def polynomial_grapher(coefficient):
    """Plot a polynomial given coefficients or a formula string.

    Accepts:
      - a formula string like "2x^2 - 3x + 1"
      - a coefficients string like "2 -3 1" or a list/tuple of numbers
    """
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except Exception as e:
        raise RuntimeError("This function requires numpy and matplotlib") from e

    # Normalize input to a list of floats (highest-degree first)
    if isinstance(coefficient, str):
        coeffs = _parse_polynomial_input(coefficient)
    elif isinstance(coefficient, (list, tuple)):
        coeffs = [float(c) for c in coefficient]
    else:
        raise TypeError("coefficient must be a list/tuple/str of numbers or formula")

    if len(coeffs) == 0:
        raise ValueError("Empty coefficient list")

    # Determine a good plotting window based on degree and leading coefficient
    degree = len(coeffs) - 1
    lead = abs(coeffs[0]) if coeffs[0] != 0 else 1.0
    span = max(5, int(5 * (lead ** (1 / (degree + 1)))))  # simple heuristic
    x_min, x_max = -span, span

    x = np.linspace(x_min, x_max, 1000)
    y = np.polyval(coeffs, x)

    # compute roots and filter real roots
    roots = np.roots(coeffs)
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-8 and x_min <= r.real <= x_max]

    # Prepare plot
    fig, ax = plt.subplots(figsize=(8, 5))

    # build readable polynomial string for legend, omit "1" coef for non-constant terms
    terms = []
    for i, a in enumerate(coeffs):
        exp = degree - i
        if abs(a) < 1e-12:
            continue
        sign_str = "-" if a < 0 else ""
        a_abs = abs(a)
        if exp == 0:
            # constant term: include numeric value with sign
            terms.append(f"{sign_str}{a_abs:.4g}")
        else:
            # non-constant: omit 1.0 coefficient (use sign and x^exp)
            coeff_str = "" if abs(a_abs - 1.0) < 1e-12 else f"{a_abs:.4g}"
            if exp == 1:
                terms.append(f"{sign_str}{coeff_str}x")
            else:
                terms.append(f"{sign_str}{coeff_str}x^{exp}")

    # join terms with plus, but ensure proper + and - spacing
    if not terms:
        poly_label = "0"
    else:
        # rebuild expression preserving signs that are already in term strings
        expr = terms[0]
        for t in terms[1:]:
            if t.startswith('-'):
                expr += " - " + t[1:]
            else:
                expr += " + " + t
        poly_label = expr

    ax.plot(x, y, label=f"p(x) = {poly_label}")
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xlabel("x")
    ax.set_ylabel("p(x)")
    ax.set_title("Polynomial Grapher")
    if real_roots:
        for r in real_roots:
            ax.plot(r, 0, 'ro')
            ax.annotate(f"{r:.3g}", xy=(r, 0), xytext=(5, 5), textcoords='offset points', color='red')
    ax.legend(loc='best', fontsize='small')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import sys
    try:
        print("Enter a polynomial formula (e.g. 2x^2 - 3x + 1) OR coefficients (e.g. 2 -3 1).")
        raw = input("> ").strip()
        polynomial_grapher(raw)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
