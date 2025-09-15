# Steel Property Explorer (Pure Python)

A simple, **no-third‑party** Python project that analyzes a small metallurgical dataset (steel samples) and produces a text report with summary statistics, outlier counts, correlations, and a simple linear regression (**Hardness vs Carbon**).

## Why this project?
- **Pure Python:** Only built-ins; no NumPy/Pandas/Matplotlib.
- **Analytical core:** From-scratch CSV parsing, descriptive statistics, IQR outlier detection, Pearson correlation, and linear regression.
- **Resume impact:** Clear domain tie-in (metallurgy) + analytical thinking + clean CLI.

## Files
- `steel_analytics.py` — main script (no external libraries)
- `steel_samples.csv` — sample dataset (50 rows)
- `report.txt` — generated analytics report

## Run
```bash
# Option A: Use the bundled dataset
python steel_analytics.py

# Option B: Supply your own CSV in the same column format
python steel_analytics.py path/to/your_data.csv
```

## Output
The script prints and saves a `report.txt` containing:
- Summary statistics for numeric columns (count, mean, std, min, quartiles, max, outliers)
- Pearson correlation and linear regression for **Hardness vs Carbon**
- Top-5 samples by **Hardness** and **UTS**

## Resume Bullets (pick 2–3)
- Built a **pure‑Python** analytics tool for steel samples—implemented CSV parsing, descriptive stats, **IQR outlier detection**, **Pearson correlation**, and **linear regression** from scratch; generated an automated report.
- Analyzed **composition–process–property** relationships (e.g., **Hardness vs Carbon**) and surfaced Top‑N insights (hardness, UTS) for metallurgical decision support.
- Wrote clean CLI code with zero third‑party dependencies; organized data and outputs for reproducibility.

## Keywords
Python, Pure Python, CLI, CSV Parsing, Descriptive Statistics, Quartiles/IQR, Pearson Correlation, Linear Regression, Top‑N Analysis, Metallurgy, Materials Analytics.