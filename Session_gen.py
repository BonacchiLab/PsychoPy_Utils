#generate session in randomized blocks of trials

import os
import random
import string
import pandas as pd

# Set working directory to script location
os.chdir(os.path.dirname(__file__))

def generate_session(n_trials=1000):
    contrast_values = [0, 0.06, 0.12, 0.25, 1]

    def choose_side(block_type):
        if block_type == "B80_20":
            return random.choices(["left", "right"], weights=[80, 20])[0]
        elif block_type == "B20_80":
            return random.choices(["left", "right"], weights=[20, 80])[0]
        else:
            return random.choice(["left", "right"])

    session_data = []
    total_trials = 0
    block_n = 1

    # Add 90 trials of neutral block
    for _ in range(90):
        session_data.append({
            "_side": choose_side("B50_50"),
            "_contrast": random.choice(contrast_values),
            "block_N": block_n,
            "block_type": "B50_50"
        })
    total_trials += 90
    block_n += 1

    # Alternate between biased blocks
    current_block = random.choice(["B80_20", "B20_80"])
    while total_trials < n_trials:
        block_size = min(random.randint(20, 100), n_trials - total_trials)
        for _ in range(block_size):
            session_data.append({
                "_side": choose_side(current_block),
                "_contrast": random.choice(contrast_values),
                "block_N": block_n,
                "block_type": current_block
            })
        total_trials += block_size
        block_n += 1
        current_block = "B20_80" if current_block == "B80_20" else "B80_20"

    return pd.DataFrame(session_data)

# Generate session
df = generate_session()

# Create sessions folder if it doesn't exist
session_folder = "sessions"
os.makedirs(session_folder, exist_ok=True)

# Determine next available session letter
existing = os.listdir(session_folder)
used_letters = [
    f[len("session_"):-4] for f in existing
    if f.startswith("session_") and f.endswith(".csv") and len(f) == 13
]

next_letter = None
for letter in string.ascii_uppercase:
    if letter not in used_letters:
        next_letter = letter
        break

if next_letter is None:
    raise ValueError("All session letters A–Z are already used.")

# Save file
filename = f"session_{next_letter}.csv"
df.to_csv(os.path.join(session_folder, filename), index=False)
print(df.head(1))
print("File saved to:", os.path.join(session_folder, filename))