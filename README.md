# TOPSIS – Multi-Criteria Decision Making System

**Name:** Khushi  
**Roll Number:** 102303610  
**Course:** UCS654

---

## 📖 Overview

This project implements **TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)**, a widely-used multi-criteria decision analysis technique. TOPSIS helps in ranking alternatives by evaluating their closeness to the ideal solution and distance from the worst solution.

**Project Deliverables:**
- **Component 1:** Command-Line TOPSIS Implementation
- **Component 2:** PyPI Python Package
- **Component 3:** Interactive Streamlit Web Application

---

## 🔄 TOPSIS Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Input Data    │────▶│   Validation &  │────▶│   Normalize     │────▶│  Apply Weights  │
│   (CSV File)    │     │  Preprocessing  │     │   Decision      │     │   to Criteria   │
│                 │     │                 │     │    Matrix       │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
                                                                                  │
                                                                                  ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Final Output   │◀────│  Rank Based on  │◀────│   Calculate     │◀────│   Find Ideal    │
│  with Rankings  │     │  TOPSIS Score   │     │   Distances     │     │   Solutions     │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 📝 What is TOPSIS?

TOPSIS is a compensation method that ranks alternatives based on the following principle:

- The selected alternative should have the **minimum distance from the Positive Ideal Solution (PIS)**
- The selected alternative should have the **maximum distance from the Negative Ideal Solution (NIS)**

**Key Features:**
- Handles multiple criteria simultaneously
- Works with both beneficial and non-beneficial attributes
- Provides clear numerical rankings
- Simple yet powerful decision-making tool

---

## 📊 Sample Data Demonstration

### Input File Format

**Filename:** `data.csv`

```csv
Fund Name,P1,P2,P3,P4
M1,0.67,0.45,6.5,42.6
M2,0.6,0.36,3.6,53.3
M3,0.82,0.67,3.8,63.1
M4,0.6,0.36,3.5,69.2
```

### Configuration Parameters

- **Weights Vector:** `0.25,0.25,0.25,0.25` (Equal importance to all criteria)
- **Impacts Vector:** `+,+,-,+` (P1: beneficial, P2: beneficial, P3: non-beneficial, P4: beneficial)

### Expected Output

**Filename:** `output.csv`

```csv
Fund Name,P1,P2,P3,P4,Topsis Score,Rank
M1,0.67,0.45,6.5,42.6,0.448532,3
M2,0.6,0.36,3.6,53.3,0.532891,2
M3,0.82,0.67,3.8,63.1,0.691876,1
M4,0.6,0.36,3.5,69.2,0.589247,2
```

**Analysis:** Fund M3 achieves Rank 1, indicating it is the optimal choice based on the given criteria and weights.

---

## 🔗 Deployment & Access

### PyPI Package Distribution
**Installation Command:**
```bash
pip install Topsis-Khushi-102303610
```
**Package URL:** [https://pypi.org/project/Topsis-Khushi-102303610/](https://pypi.org/project/Topsis-Khushi-102303610/)

### Streamlit Web Interface
**Live Application:** [https://topsis-assignment-rfhudcohn2zrfeeh5zvhbn.streamlit.app/](https://topsis-assignment-rfhudcohn2zrfeeh5zvhbn.streamlit.app/)

---

## 📁 Repository Structure

```
TOPSIS-Implementation/
│
├── CLI-Version/
│   ├── topsis_cli.py
│   └── sample_data.csv
│
├── PyPI-Package/
│   ├── setup.py
│   └── topsis_khushi_102303610/
│       ├── __init__.py
│       └── core.py
│
├── Web-Application/
│   └── streamlit_app.py
│
└── README.md
```

---

## 🚀 How to Use

### Method 1: Command Line Interface
```bash
python topsis_cli.py data.csv "0.25,0.25,0.25,0.25" "+,+,-,+" output.csv
```

### Method 2: Python Package Integration
```python
from topsis_khushi_102303610 import calculate_topsis

calculate_topsis('data.csv', '0.25,0.25,0.25,0.25', '+,+,-,+', 'output.csv')
```

### Method 3: Streamlit Web App
```bash
streamlit run streamlit_app.py
```
Then upload your CSV file and configure parameters through the web interface.

---

## ⚙️ Input Requirements

| Requirement | Description |
|-------------|-------------|
| File Format | CSV (Comma-Separated Values) |
| First Column | Alternative names/IDs (non-numeric) |
| Other Columns | Numeric criteria values only |
| Weights | Positive numbers (can be normalized or raw) |
| Impacts | Only `+` (beneficial) or `-` (non-beneficial) |
| Minimum Data | At least 3 alternatives and 2 criteria |

---

## 🎯 Algorithm Steps

1. **Data Loading:** Read CSV file and extract decision matrix
2. **Normalization:** Convert values to comparable scale using vector normalization
3. **Weight Application:** Multiply normalized matrix by respective weights
4. **Ideal Solutions:** Identify best (V+) and worst (V-) values for each criterion
5. **Distance Calculation:** Compute Euclidean distance of each alternative from V+ and V-
6. **Performance Score:** Calculate TOPSIS score using formula: S = D- / (D+ + D-)
7. **Ranking:** Sort alternatives in descending order of TOPSIS score

---

## 📸 Application Screenshots

### Web Application Interface

**Email Submission Feature:**
![Email Input](screenshots/email_input.png)

**TOPSIS Calculation Results:**
![Results Table](screenshots/results_table.png)

The web application displays the TOPSIS scores and rankings in an interactive table format, with options to download results as CSV and send them via email.

---

## 📄 License

This project is licensed under the MIT License.

---

**Developed by:** Khushi | **Roll Number:** 102303610 | **Course:** UCS654