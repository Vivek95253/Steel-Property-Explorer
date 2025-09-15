#!/usr/bin/env python3
"""
Steel Property Explorer — pure Python (no third‑party libraries)

Usage:
  python steel_analytics.py           # reads steel_samples.csv and prints + saves report.txt
  python steel_analytics.py input.csv # specify a different CSV
"""

# --- No external imports used; only built-ins ---

def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_csv(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    header = lines[0].split(",")
    data = []
    for line in lines[1:]:
        parts = line.split(",")
        row = {}
        for k, v in zip(header, parts):
            # convert numerics where possible
            try:
                if "." in v or "e" in v.lower():
                    row[k] = float(v)
                else:
                    row[k] = int(v)
            except ValueError:
                row[k] = v
        data.append(row)
    return header, data

def column(rows, key):
    vals = []
    for r in rows:
        v = r.get(key)
        if isinstance(v, (int, float)):
            vals.append(float(v))
    return vals

def mean(lst):
    return sum(lst)/len(lst) if lst else 0.0

def median(sorted_lst):
    n = len(sorted_lst)
    if n == 0: return 0.0
    m = n // 2
    if n % 2 == 1:
        return sorted_lst[m]
    return (sorted_lst[m-1] + sorted_lst[m]) / 2.0

def stdev_sample(lst):
    n = len(lst)
    if n < 2: return 0.0
    m = mean(lst)
    var = sum((x - m)*(x - m) for x in lst) / (n - 1)
    return var ** 0.5

def pearson_corr(x, y):
    n = min(len(x), len(y))
    if n < 2: return 0.0
    xm = mean(x); ym = mean(y)
    xs = stdev_sample(x); ys = stdev_sample(y)
    if xs == 0 or ys == 0: return 0.0
    num = sum((x[i]-xm)*(y[i]-ym) for i in range(n))
    den = (n-1)*xs*ys
    return num/den

def linear_regression(x, y):
    # returns slope, intercept, r2
    n = min(len(x), len(y))
    if n < 2: return 0.0, 0.0, 0.0
    xm = mean(x); ym = mean(y)
    num = sum((x[i]-xm)*(y[i]-ym) for i in range(n))
    den = sum((x[i]-xm)*(x[i]-xm) for i in range(n))
    if den == 0: return 0.0, ym, 0.0
    slope = num/den
    intercept = ym - slope*xm
    # r^2
    corr = pearson_corr(x, y)
    r2 = corr*corr
    return slope, intercept, r2

def quartiles(lst):
    if not lst: return 0.0, 0.0, 0.0
    s = sorted(lst)
    n = len(s)
    med = median(s)
    if n % 2 == 0:
        lower = s[:n//2]
        upper = s[n//2:]
    else:
        lower = s[:n//2]
        upper = s[n//2+1:]
    q1 = median(lower)
    q3 = median(upper)
    return q1, med, q3

def iqr_outliers(lst):
    if not lst: return [], 0.0, 0.0, 0.0
    q1, med, q3 = quartiles(lst)
    iqr = q3 - q1
    lower = q1 - 1.5*iqr
    upper = q3 + 1.5*iqr
    out = [x for x in lst if x < lower or x > upper]
    return out, q1, med, q3

def top_k(rows, key, k=5, desc=True):
    nums = [(r.get(key), r) for r in rows if isinstance(r.get(key), (int, float))]
    nums.sort(key=lambda t: t[0], reverse=desc)
    return [r for _, r in nums[:k]]

def format_table(rows, keys):
    # simple fixed-width table string
    widths = {k: len(k) for k in keys}
    for r in rows:
        for k in keys:
            widths[k] = max(widths[k], len(str(r.get(k, ""))))
    line = " | ".join(k.ljust(widths[k]) for k in keys)
    sep  = "-+-".join("-"*widths[k] for k in keys)
    out = [line, sep]
    for r in rows:
        out.append(" | ".join(str(r.get(k, "")).ljust(widths[k]) for k in keys))
    return "\n".join(out)

def analyze(rows):
    # numeric columns of interest
    numeric = ["Carbon_pct","Manganese_pct","Silicon_pct","QuenchTemp_C","TemperTemp_C","TemperTime_min","Hardness_HRC","UTS_MPa","Yield_MPa","Elongation_pct"]
    stats = []
    for key in numeric:
        col = column(rows, key)
        if not col:
            continue
        outliers, q1, med, q3 = iqr_outliers(col)
        stats.append({
            "Metric": key,
            "Count": len(col),
            "Mean": round(mean(col), 3),
            "StdDev": round(stdev_sample(col), 3),
            "Min": round(min(col), 3),
            "Q1": round(q1, 3),
            "Median": round(med, 3),
            "Q3": round(q3, 3),
            "Max": round(max(col), 3),
            "Outliers": len(outliers),
        })
    # correlations & regression
    x = column(rows, "Carbon_pct")
    yH = column(rows, "Hardness_HRC")
    yU = column(rows, "UTS_MPa")
    yY = column(rows, "Yield_MPa")
    corr_c_h = round(pearson_corr(x, yH), 3)
    slope, intercept, r2 = linear_regression(x, yH)
    regression = (round(slope, 3), round(intercept, 3), round(r2, 3))

    # top samples by hardness and UTS
    top_h = top_k(rows, "Hardness_HRC", 5, True)
    top_u = top_k(rows, "UTS_MPa", 5, True)
    return stats, corr_c_h, regression, top_h, top_u

def generate_report(path):
    text = read_text(path)
    header, data = parse_csv(text)
    stats, corr_c_h, regression, top_h, top_u = analyze(data)

    lines = []
    lines.append("STEEL PROPERTY EXPLORER — ANALYTICS REPORT (pure Python)")
    lines.append("="*66)
    lines.append(f"Input file: {path}")
    lines.append(f"Total samples: {len(data)}")
    lines.append("")

    lines.append("[1] SUMMARY STATISTICS")
    lines.append(format_table(stats, ["Metric","Count","Mean","StdDev","Min","Q1","Median","Q3","Max","Outliers"]))
    lines.append("")

    lines.append("[2] CORRELATION & REGRESSION (Hardness vs Carbon)")
    lines.append(f"Pearson correlation (Carbon% vs Hardness HRC): {corr_c_h}")
    s, b, r2 = regression
    lines.append(f"Linear regression  Hardness ≈ {s} * Carbon_pct + {b}   (R^2 = {r2})")
    lines.append("Note: Positive slope indicates higher carbon tends to increase hardness.")
    lines.append("")

    lines.append("[3] TOP-5 SAMPLES BY HARDNESS (HRC)")
    lines.append(format_table(top_h, ["SampleID","Carbon_pct","QuenchTemp_C","TemperTemp_C","TemperTime_min","Hardness_HRC"]))
    lines.append("")
    lines.append("[4] TOP-5 SAMPLES BY UTS (MPa)")
    lines.append(format_table(top_u, ["SampleID","Carbon_pct","Hardness_HRC","UTS_MPa","Yield_MPa","Elongation_pct"]))
    lines.append("")
    lines.append("End of report.")
    return "\n".join(lines)

def main():
    import sys
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = "steel_samples.csv"
    report = generate_report(csv_path)
    print(report)
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    main()
