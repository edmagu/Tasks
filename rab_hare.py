# Elias Daniel Macero Gutierrez
# Tortoise and the Hare
# Date 10/12/2025
# Version 4.2.1



import os
import json
import openai
from typing import Dict, Any

DEFAULT_VALUES = {
    "min_race_length": 10,
    "recommended_race_length": 20,
    "tortoise_moves": [
        {"prob": 50, "move": 3},
        {"prob": 20, "move": -6},
        {"prob": 30, "move": 1},
    ],
    "hare_moves": [
        {"prob": 20, "move": 0},
        {"prob": 20, "move": 9},
        {"prob": 10, "move": -12},
        {"prob": 30, "move": 1},
        {"prob": 20, "move": -2}, 
    ],
}

def default_values() -> Dict[str, Any]:
    return DEFAULT_VALUES


def fetch_values_from_model() -> Dict[str, Any]:
    """Ask ChatGPT (via OpenAI API) to return the race parameters as JSON.

    The model is explicitly instructed to return ONLY a JSON object with the
    required schema so this program can parse it directly.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY not set — using default values.")
        return default_values()

    openai.api_key = api_key

    prompt = (
        "You are designing movement probabilities for a Tortoise and a Hare race.\n"
        "Return ONLY a JSON object (no explanatory text) with this exact schema:\n"
        "{\n"
        "  \"min_race_length\": integer,\n"
        "  \"recommended_race_length\": integer,\n"
        "  \"tortoise_moves\": [{\"prob\": int, \"move\": int}, ...],\n"
        "  \"hare_moves\": [{\"prob\": int, \"move\": int}, ...]\n"
        "}\n"
        "Make sure the probabilities for each animal sum to 100. Use integers for probabilities and moves.\n"
        "Example movements you may use (but you can keep these):\n"
        "Tortoise options: 50% 3 ahead, 20% 6 back, 30% 1 ahead\n"
        "Hare options: 20% no move, 20% 9 ahead, 10% 12 back, 30% 1 ahead, 20% 2 back\n"
        "Choose a sensible `min_race_length` and `recommended_race_length`.\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=500,
        )
        content = response.choices[0].message.content.strip()
        # Attempt to parse JSON. If the model returns code fences or extra text,
        # try to find the first JSON object inside the content.
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Try to extract a JSON substring
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1 and end > start:
                sub = content[start:end+1]
                data = json.loads(sub)
            else:
                raise
        # Basic validation: check required keys
        if not all(k in data for k in ("min_race_length", "recommended_race_length", "tortoise_moves", "hare_moves")):
            print("Model returned JSON missing required keys — falling back to defaults.")
            return default_values()
        return data
    except Exception as e:
        print("OpenAI request failed or returned invalid JSON:", e)
        print("Falling back to default values.")
        return default_values()


def print_values(values: Dict[str, Any]) -> None:
    print("\nRace parameters:")
    print(f"Minimum race length: {values['min_race_length']}")
    print(f"Recommended race length: {values['recommended_race_length']}")
    print("\nTortoise moves:")
    for move in values['tortoise_moves']:
        print(f"  - {move['prob']}% -> {move['move']} squares")
    print("\nHare moves:")
    for move in values['hare_moves']:
        print(f"  - {move['prob']}% -> {move['move']} squares")


def rab_hare():
    """Main entry: fetch values from the model (or defaults), print them,
    prompt the user for a race length, then run the race simulation on a
    number line until someone reaches or passes the finish line.
    """

    values = fetch_values_from_model()
    print_values(values)

    min_len = int(values.get('min_race_length', 10))
    recommended = int(values.get('recommended_race_length', min_len))

    # Ask user for race length
    try:
        while True:
            raw = input(f"Enter race length in units (min {min_len}, recommended {recommended}): ").strip()
            try:
                race_len = int(raw)
            except ValueError:
                print("Please enter an integer.")
                continue
            if race_len < min_len:
                print(f"Race length must be at least {min_len}.")
                continue
            break
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        return

    # Run interactive simulation using the helper
    simulate_race(values, race_len)


def simulate_race(values: Dict[str, Any], race_len: int, seed: int | None = None) -> None:
    """Simulate a race given parameter dict `values` and integer `race_len`.

    If `seed` is provided, random will be seeded for deterministic output.
    This function prints per-turn moves and a simple ASCII number line.
    """
    import random

    if seed is not None:
        random.seed(seed)

    def make_choices(moves):
        weights = [m['prob'] for m in moves]
        steps = [m['move'] for m in moves]
        return steps, weights

    tortoise_steps, tortoise_weights = make_choices(values['tortoise_moves'])
    hare_steps, hare_weights = make_choices(values['hare_moves'])

    tortoise_pos = 0
    hare_pos = 0
    turn = 0

    print("\nStarting race!\n")
    finish = race_len

    # Helper to draw a simple number line showing positions (clamped)
    def draw_line(t_pos, h_pos, finish, width=60):
        # Map positions from 0..finish to 0..width
        def map_pos(p):
            if p <= 0:
                return 0
            if p >= finish:
                return width
            return int((p / finish) * width)

        t = map_pos(t_pos)
        h = map_pos(h_pos)
        line = ['-' for _ in range(width + 1)]
        if t == h:
            line[t] = 'B'  # Both
        else:
            line[t] = 'T'
            line[h] = 'H'
        # mark finish
        line[-1] = '|'
        return ''.join(line)

    # Run the simulation until someone reaches or passes finish
    while tortoise_pos < finish and hare_pos < finish:
        turn += 1
        t_move = random.choices(tortoise_steps, weights=tortoise_weights, k=1)[0]
        h_move = random.choices(hare_steps, weights=hare_weights, k=1)[0]
        tortoise_pos += t_move
        hare_pos += h_move

        # Prevent negative positions
        tortoise_pos = max(0, tortoise_pos)
        hare_pos = max(0, hare_pos)

        print(f"Turn {turn}: Tortoise moved {t_move} -> pos {tortoise_pos}; Hare moved {h_move} -> pos {hare_pos}")
        print(draw_line(tortoise_pos, hare_pos, finish))

    # Determine winner (can be a tie)
    if tortoise_pos >= finish and hare_pos >= finish:
        print("\nIt's a tie!")
    elif tortoise_pos >= finish:
        print("\nTortoise wins!")
    else:
        print("\nHare wins!")


if __name__ == "__main__":
    rab_hare()