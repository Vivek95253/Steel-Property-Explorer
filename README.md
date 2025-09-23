# Process Optimization and Data Analytics

Performed regression analysis on blast furnace data to identify key factors affecting Si content in hot metal and analyzed impact of coke rate, oxygen enrichment and tempresure on silicon variability.

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



## Keywords
Python, Pure Python, CLI, CSV Parsing, Descriptive Statistics, Quartiles/IQR, Pearson Correlation, Linear Regression, Top‑N Analysis, Metallurgy, Materials Analytics.
