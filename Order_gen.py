# generate order of sessions for each participant randomized in blocks

import random
import pandas as pd
import os
import string

# Set working directory to script location
os.chdir(os.path.dirname(__file__))

# Set parameters
participant_total = 15
num_sessions = 20
block_size = 4
session_labels = [f"session_{l}" for l in string.ascii_uppercase[:num_sessions]]
output_file = "participant_sessions.csv"

# Check if output file exists
if os.path.exists(output_file):
    # Load existing assignments
    df = pd.read_csv(output_file)
    existing = df['participant'].tolist()
    base_order = df.iloc[0, 1:].tolist()
    # Split sessions into blocks
    blocks = [base_order[i:i + block_size] for i in range(0, num_sessions, block_size)]
else:
    # Shuffle session labels and split into blocks
    random.shuffle(session_labels)
    blocks = [session_labels[i:i + block_size] for i in range(0, num_sessions, block_size)]
    df = pd.DataFrame()
    existing = []

# Determine how many new participants to add
n_new = participant_total - len(existing)
if n_new <= 0:
    print("No new participants needed.")
    exit()
start_idx = len(existing) + 1

# Assign sessions to new participants
for i in range(n_new):
    pid = f"P{start_idx + i:03}"
    shuffled = [random.sample(block, len(block)) for block in blocks]
    flat = [s for block in shuffled for s in block]
    row = {"participant": pid}
    row.update({f"session{j+1}": flat[j] for j in range(num_sessions)})
    df.loc[len(df)] = row

# Save updated assignments to CSV
df.to_csv(output_file, index=False)
print(f"Added {n_new} participants.")
print(f"File saved to: {output_file}")