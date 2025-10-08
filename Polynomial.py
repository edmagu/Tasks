# Polynomial grapher with user-friendly parser that supports multiple terms with same power.
# Author: Elias Daniel Macero Gutierrez
# Version: 2.4 - integer tick increments & continuous plot
import re
import math

def _parse_polynomial_input(s: str):
    """Parse a user-friendly polynomial string into a list of coefficients
    highest-degree first.

    Supports multiple occurrences of the same power (they are summed).
    Returns a list of floats [a_n, ..., a_0].
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
    """Plot a polynomial with Desmos-like visuals, centered on x-intercepts.
    Continuous curve and integer tick increments on both axes.
    """
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise RuntimeError("This function requires numpy and matplotlib") from exc

    # Normalize input to a list of floats (highest-degree first)
    if isinstance(coefficient, str):
        coeffs = _parse_polynomial_input(coefficient)
    elif isinstance(coefficient, (list, tuple)):
        coeffs = [float(c) for c in coefficient]
    else:
        raise TypeError("coefficient must be a list/tuple/str of numbers or formula")

    if len(coeffs) == 0:
        raise ValueError("Empty coefficient list")

    # Build polynomial object
    p = np.poly1d(coeffs)
    degree = p.order
    leading = coeffs[0]

    # Find real roots
    roots = np.roots(coeffs)
    real_roots = sorted([r.real for r in roots if abs(r.imag) < 1e-9 and np.isfinite(r.real)])

    # Find real critical points (derivative roots)
    real_crit = []
    if degree >= 1:
        dp = p.deriv()
        crit = np.roots(dp)
        real_crit = sorted([c.real for c in crit if abs(c.imag) < 1e-9 and np.isfinite(c.real)])

    # Determine center_x:
    # Prefer midpoint of min/max real roots so all x-intercepts sit around center.
    xs_interest = []
    xs_interest.extend(real_roots)
    xs_interest.extend(real_crit)
    xs_interest = [x for x in xs_interest if np.isfinite(x)]

    if real_roots:
        center_x = 0.5 * (min(real_roots) + max(real_roots))
    elif real_crit:
        center_x = 0.5 * (min(real_crit) + max(real_crit))
    else:
        center_x = 0.0

    # Determine horizontal half-span so roots + critical points and nearby vertex visible
    if xs_interest:
        max_dist = max(abs(x - center_x) for x in xs_interest)
        half_span = max(2.0, max_dist * 1.6 + 1.0)  # scale factor + padding
    else:
        half_span = 5.0

    # Expand span slightly depending on leading coefficient magnitude for clarity
    lead_abs = abs(leading) if leading != 0 else 1.0
    extra = max(0.0, (lead_abs ** (1 / max(1, degree + 1))) - 1.0)
    half_span += extra

    x_min = center_x - half_span
    x_max = center_x + half_span

    # make continuous: dense sampling (smooth, continuous curve)
    num_pts = 8000 if degree >= 3 else 4000
    x = np.linspace(x_min, x_max, num_pts)
    y = p(x)

    # compute sensible y-limits while avoiding extreme spikes
    finite = np.isfinite(y)
    if not finite.any():
        raise RuntimeError("Polynomial evaluation produced no finite values on the plotting grid.")
    y_finite = y[finite]
    y_low, y_high = np.percentile(y_finite, [1, 99])
    y_margin = max(1.0, 0.12 * (y_high - y_low)) if y_high != y_low else 1.0
    y_min = y_low - y_margin
    y_max = y_high + y_margin
    if abs(y_max - y_min) < 1e-3:
        y_min -= 1.0
        y_max += 1.0

    # round axis tick ranges to integers so ticks increment by 1
    xtick_min = math.ceil(x_min)
    xtick_max = math.floor(x_max)
    if xtick_min > xtick_max:
        # ensure at least one integer tick visible
        xtick_min = math.floor(x_min)
        xtick_max = math.ceil(x_max)
    ytick_min = math.floor(y_min)
    ytick_max = math.ceil(y_max)
    if ytick_min == ytick_max:
        ytick_min -= 1
        ytick_max += 1

    # build integer tick arrays (step = 1)
    x_ticks = list(range(xtick_min, xtick_max + 1))
    y_ticks = list(range(ytick_min, ytick_max + 1))

    # Create plot with Desmos-like styling
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Glow effect: multiple plotted lines with increasing linewidth and lower alpha
    base_color = (0.0, 0.4, 0.8)  # blue
    for w, a in [(8, 0.05), (5, 0.08), (3, 0.12)]:
        ax.plot(x, y, linewidth=w, color=base_color, alpha=a, solid_capstyle='round', zorder=1)
    # main crisp line
    ax.plot(x, y, linewidth=2.6, color=base_color, zorder=2, solid_capstyle='round')

    # Place spines so axes collide at (center_x, 0)
    ax.spines['left'].set_position(('data', center_x))   # vertical axis at center_x
    ax.spines['bottom'].set_position(('data', 0.0))     # horizontal axis at y = 0
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_zorder(3)
    ax.spines['bottom'].set_zorder(3)

    # Recompute limits in case spines positioning influences tick layout
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Draw arrowheads on axes relative to current axis limits
    def _draw_axis_arrow(ax, axis='x', size=12, color='k'):
        xm, xM = ax.get_xlim()
        ym, yM = ax.get_ylim()
        if axis == 'x':
            # arrow at right end of x-axis (y=0)
            ax.annotate('', xy=(xM + 0.02*(xM-xm), 0), xytext=(xM, 0),
                        arrowprops=dict(arrowstyle='-|>', mutation_scale=size, color=color))
            # arrow at left end
            ax.annotate('', xy=(xm - 0.02*(xM-xm), 0), xytext=(xm, 0),
                        arrowprops=dict(arrowstyle='-|>', mutation_scale=size, color=color))
        else:
            # vertical arrows up and down at x=center_x
            ax.annotate('', xy=(center_x, yM + 0.02*(yM-ym)), xytext=(center_x, yM),
                        arrowprops=dict(arrowstyle='-|>', mutation_scale=size, color=color))
            ax.annotate('', xy=(center_x, ym - 0.02*(yM-ym)), xytext=(center_x, ym),
                        arrowprops=dict(arrowstyle='-|>', mutation_scale=size, color=color))
    _draw_axis_arrow(ax, 'x')
    _draw_axis_arrow(ax, 'y')

    # set integer ticks (step = 1)
    # If user domain is very large, matplotlib will still display many ticks; keep step=1 per request
    if len(x_ticks) >= 2:
        ax.set_xticks(x_ticks)
    else:
        # ensure at least ticks at integer positions around center
        ax.set_xticks([math.floor(center_x)-1, math.floor(center_x), math.floor(center_x)+1])

    if len(y_ticks) >= 2:
        ax.set_yticks(y_ticks)
    else:
        ax.set_yticks([math.floor(0)-1, 0, math.floor(0)+1])

    ax.set_xticklabels([str(int(t)) for t in ax.get_xticks()])
    ax.set_yticklabels([str(int(t)) for t in ax.get_yticks()])

    ax.grid(True, which='major', linestyle='--', linewidth=0.6, color='#dddddd', zorder=0)
    ax.set_xlabel("x", loc='right')
    ax.set_ylabel("p(x)", loc='top', rotation=0)

    # Annotate real roots (x-intercepts) exactly on the x-axis
    for r in real_roots:
        if x_min <= r <= x_max:
            ax.plot(r, 0.0, 'o', color='firebrick', markersize=6, zorder=6)
            ax.annotate(f"{r:.6g}", xy=(r, 0.0), xytext=(6, 6), textcoords='offset points',
                        color='firebrick', fontsize=8, zorder=7)

    # Annotate critical points
    for c in real_crit:
        if x_min <= c <= x_max:
            val = p(c)
            if np.isfinite(val):
                ax.plot(c, val, 's', color='darkorange', markersize=5, zorder=6)
                ax.annotate(f"{c:.6g}", xy=(c, val), xytext=(6, -10), textcoords='offset points',
                            color='darkorange', fontsize=8, zorder=7)

    # Leading coefficient display in title and legend
    lead_str = f"Leading coef: {leading:.6g}"
    ax.set_title(f"p(x) = polynomial — {lead_str}", fontsize=12)

    # Add formatted polynomial label (small)
    ax.legend([_format_poly_label(coeffs)], loc='upper left', fontsize='small', frameon=False)

    # Hover cursor: show (x, p(x)) near cursor like Desmos coordinate readout
    annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"), fontsize=9)
    annot.set_visible(False)

    def _on_move(event):
        if event.inaxes != ax:
            if annot.get_visible():
                annot.set_visible(False)
                fig.canvas.draw_idle()
            return
        xm = event.xdata
        if xm is None:
            return
        try:
            ym = float(p(xm))
        except Exception:
            if annot.get_visible():
                annot.set_visible(False)
                fig.canvas.draw_idle()
            return
        if not np.isfinite(ym):
            if annot.get_visible():
                annot.set_visible(False)
                fig.canvas.draw_idle()
            return
        annot.xy = (xm, ym)
        annot.set_text(f"x={xm:.4g}\ny={ym:.4g}")
        annot.get_bbox_patch().set_alpha(0.9)
        annot.set_visible(True)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", _on_move)

    # Tight layout and show
    plt.tight_layout()
    plt.show()


def _format_poly_label(coeffs):
    """Return a human-friendly polynomial string from coeffs (highest-degree first)."""
    degree = len(coeffs) - 1
    parts = []
    for i, a in enumerate(coeffs):
        exp = degree - i
        if abs(a) < 1e-12:
            continue
        sign = "-" if a < 0 else "+"
        a_abs = abs(a)
        if exp == 0:
            term = f"{a_abs:.6g}"
        elif exp == 1:
            coeff_str = "" if abs(a_abs - 1.0) < 1e-12 else f"{a_abs:.6g}"
            term = f"{coeff_str}x"
        else:
            coeff_str = "" if abs(a_abs - 1.0) < 1e-12 else f"{a_abs:.6g}"
            term = f"{coeff_str}x^{exp}"
        parts.append((sign, term))

    if not parts:
        return "p(x) = 0"

    # Build string starting with correct sign for first term
    first_sign, first_term = parts[0]
    if first_sign == "-":
        expr = "-" + first_term
    else:
        expr = first_term
    for sign, term in parts[1:]:
        expr += f" {sign} {term}"
    return f"p(x) = {expr}"


if __name__ == "__main__":
    import sys
    try:
        print("Enter a polynomial formula (e.g. 2x^2 - 3x + 1) OR coefficients (e.g. 2 -3 1).")
        raw = input("> ").strip()
        polynomial_grapher(raw)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
