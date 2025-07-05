# generate summary files of trials of each session

import pandas as pd
import glob
import os

# Set working directory to script location
os.chdir(os.path.dirname(__file__))

# Define input and output folders
input_folder = "sessions"
output_folder = "blocks"
os.makedirs(output_folder, exist_ok=True)

# Find all session CSV files in the input folder
csv_files = glob.glob(os.path.join(input_folder, "session_*.csv"))

# Process each session file
for file in csv_files:
    df = pd.read_csv(file)

    # Group by block number and block type, count number of trials per block
    summary_df = df.groupby(['block_N', 'block_type']).size().reset_index(name='NumTrials')
    summary_df = summary_df[['block_type', 'NumTrials']]

    # Prepare output file name and path
    base_name = os.path.basename(file)
    output_name = f"summary_{base_name}"
    output_path = os.path.join(output_folder, output_name)

    # Save summary to CSV
    summary_df.to_csv(output_path, index=False)

print("Summary files saved to:", output_folder)
