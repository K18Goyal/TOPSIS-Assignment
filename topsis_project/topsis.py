"""
TOPSIS Command Line Program

Usage:
python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>

Example:
python topsis.py data.csv "1,1,1,2" "+,+,-,+" result.csv
"""

# ===============================
# STEP 0: Import required libraries
# ===============================
import sys              # for command-line arguments
import os               # for file existence checking
import pandas as pd     # for CSV file handling
import numpy as np      # for numerical calculations


# ===============================
# STEP 1: Function to handle errors
# ===============================
def terminate(message):
    # Print error message and exit program
    print(f"Error: {message}")
    sys.exit(1)


# ==================================================
# STEP 2: Read and validate all input parameters
# ==================================================
def read_and_validate_inputs():

    # STEP 2.1: Check number of command-line arguments
    if len(sys.argv) != 5:
        terminate(
            "Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>"
        )

    # STEP 2.2: Extract arguments
    input_file, weight_str, impact_str, output_file = sys.argv[1:]

    # STEP 2.3: Check if input CSV file exists
    if not os.path.isfile(input_file):
        terminate("Input file not found")

    # STEP 2.4: Read CSV file
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        terminate(f"Unable to read input file: {e}")

    # STEP 2.5: Check minimum number of columns
    if df.shape[1] < 3:
        terminate("Input file must contain at least three columns")

    # STEP 2.6: Validate numeric criteria columns (2nd to last)
    try:
        criteria = df.iloc[:, 1:].apply(pd.to_numeric)
    except:
        terminate("All columns except the first must contain numeric values only")

    # STEP 2.7: Parse weights and impacts
    try:
        weights = np.array([float(w) for w in weight_str.split(",")])
        impacts = impact_str.split(",")
    except:
        terminate("Weights and impacts must be comma separated")

    # STEP 2.8: Check matching count of weights, impacts, and criteria
    if len(weights) != criteria.shape[1] or len(impacts) != criteria.shape[1]:
        terminate("Number of weights, impacts, and criteria columns must be same")

    # STEP 2.9: Validate impact symbols
    for imp in impacts:
        if imp not in ["+", "-"]:
            terminate("Impacts must be either '+' or '-'")

    # Return validated values
    return df, criteria, weights, impacts, output_file


# ==========================================
# STEP 3: Perform TOPSIS calculations
# ==========================================
def calculate_topsis(data, criteria, weights, impacts):

    # STEP 3.1: Normalize the decision matrix
    norm = np.sqrt((criteria ** 2).sum())
    normalized_matrix = criteria / norm

    # STEP 3.2: Apply weights to normalized matrix
    weighted_matrix = normalized_matrix * weights

    # STEP 3.3: Determine ideal best and ideal worst values
    ideal_best = []
    ideal_worst = []

    for i, impact in enumerate(impacts):
        column = weighted_matrix.iloc[:, i]
        if impact == "+":
            ideal_best.append(column.max())
            ideal_worst.append(column.min())
        else:
            ideal_best.append(column.min())
            ideal_worst.append(column.max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # STEP 3.4: Calculate Euclidean distances
    distance_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

    # STEP 3.5: Calculate TOPSIS score
    topsis_score = distance_worst / (distance_best + distance_worst)

    # STEP 3.6: Rank alternatives based on TOPSIS score
    data["Topsis Score"] = topsis_score
    data["Rank"] = topsis_score.rank(ascending=False, method="dense").astype(int)

    return data


# ===============================
# STEP 4: Main execution function
# ===============================
def main():

    # STEP 4.1: Validate inputs
    data, criteria, weights, impacts, output_file = read_and_validate_inputs()

    # STEP 4.2: Compute TOPSIS results
    result = calculate_topsis(data, criteria, weights, impacts)

    # STEP 4.3: Save output to CSV file
    try:
        result.to_csv(output_file, index=False)
        print(f"TOPSIS result successfully saved to {output_file}")
    except Exception as e:
        terminate(f"Unable to write output file: {e}")


# ===============================
# STEP 5: Program entry point
# ===============================
if __name__ == "__main__":
    main()
