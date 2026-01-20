import sys
import os
import pandas as pd
import numpy as np


def terminate(msg):
    """
    Print error message and exit program
    """
    print(f"Error: {msg}")
    sys.exit(1)


def main():
    """
    Main function to execute TOPSIS from command line
    """

    # STEP 1: Read command-line arguments
    if len(sys.argv) != 5:
        terminate(
            "Usage: python -m topsis_khushi <input.csv> <weights> <impacts> <output.csv>"
        )

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]

    # STEP 2: Check input file
    if not os.path.exists(input_file):
        terminate("Input file does not exist")

    # STEP 3: Read CSV
    try:
        df = pd.read_csv(input_file)
    except Exception:
        terminate("Unable to read input CSV file")

    if df.shape[1] < 3:
        terminate("Input file must have at least 3 columns")

    # STEP 4: Convert criteria columns to numeric
    try:
        data = df.iloc[:, 1:].astype(float)
    except Exception:
        terminate("Criteria columns must contain numeric values only")

    # STEP 5: Parse weights and impacts
    try:
        weights = np.array([float(w) for w in weights_str.split(",")])
        impacts = impacts_str.split(",")
    except Exception:
        terminate("Weights and impacts must be comma-separated")

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        terminate("Number of weights, impacts, and criteria columns must match")

    for imp in impacts:
        if imp not in ["+", "-"]:
            terminate("Impacts must be either + or -")

    # STEP 6: Normalize decision matrix
    norm = np.sqrt((data ** 2).sum())
    normalized = data / norm

    # STEP 7: Apply weights
    weighted = normalized * weights

    # STEP 8: Determine ideal best and worst
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == "+":
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # STEP 9: Calculate distances
    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # STEP 10: Calculate TOPSIS score
    score = dist_worst / (dist_best + dist_worst)

    # STEP 11: Rank alternatives
    df["Topsis Score"] = score
    df["Rank"] = score.rank(ascending=False, method="dense").astype(int)

    # STEP 12: Save output
    try:
        df.to_csv(output_file, index=False)
        print(f"TOPSIS result successfully saved to {output_file}")
    except Exception:
        terminate("Unable to write output file")
