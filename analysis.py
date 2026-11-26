"""Reproducible analysis for the Movie Data Analytics portfolio project.

Place Movies_Data_Analytics_Project.xlsx beside this script, then run:
    python analysis.py

Outputs CSV summaries and PNG charts in ./outputs/.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
WORKBOOK = BASE_DIR / "Movies_Data_Analytics_Project.xlsx"
OUTPUT_DIR = BASE_DIR / "outputs"


def main():
    if not WORKBOOK.exists():
        raise FileNotFoundError(
            f"Could not find {WORKBOOK.name}. Download the workbook from the repository "
            "and place it beside analysis.py."
        )

    xls = pd.ExcelFile(WORKBOOK)
    sheet = "Cleaned_Data" if "Cleaned_Data" in xls.sheet_names else xls.sheet_names[0]
    df = pd.read_excel(WORKBOOK, sheet_name=sheet)

    required = {
        "Title", "Budget", "Original Language", "Release Date",
        "Revenue", "Runtime", "Vote Average", "Vote Count"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Workbook is missing required columns: {sorted(missing)}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")
    df["Release Year"] = df["Release Date"].dt.year

    # Exclude exact duplicate rows if the selected worksheet contains any.
    before = len(df)
    df = df.drop_duplicates().copy()
    duplicate_rows_removed = before - len(df)

    # Revenue ranking is based on recorded revenue; source currency is not documented.
    top_revenue = df.nlargest(20, "Revenue")[
        ["Title", "Release Year", "Original Language", "Budget", "Revenue",
         "Vote Average", "Vote Count"]
    ]
    top_revenue.to_csv(OUTPUT_DIR / "top_revenue_movies.csv", index=False)

    # Use a minimum vote count to avoid ranking titles with very few ratings.
    top_rated = df[(df["Vote Count"] >= 100) & (df["Vote Average"] > 0)].sort_values(
        ["Vote Average", "Vote Count"], ascending=[False, False]
    ).head(20)
    top_rated[["Title", "Release Year", "Original Language", "Vote Average", "Vote Count"]].to_csv(
        OUTPUT_DIR / "top_rated_movies_100_votes.csv", index=False
    )

    language_summary = df.groupby("Original Language", dropna=False).agg(
        Movie_Records=("Title", "size"),
        Average_Vote=("Vote Average", "mean"),
        Total_Recorded_Revenue=("Revenue", "sum"),
    ).reset_index().sort_values("Movie_Records", ascending=False)
    language_summary.to_csv(OUTPUT_DIR / "language_summary.csv", index=False)

    year_summary = df.dropna(subset=["Release Year"]).groupby("Release Year").agg(
        Movie_Records=("Title", "size"),
        Average_Vote=("Vote Average", "mean"),
        Total_Recorded_Revenue=("Revenue", "sum"),
    ).reset_index().sort_values("Release Year")
    year_summary.to_csv(OUTPUT_DIR / "year_summary.csv", index=False)

    quality = pd.DataFrame([
        {"Metric": "Rows read from selected worksheet", "Value": before},
        {"Metric": "Exact duplicate rows removed by script", "Value": duplicate_rows_removed},
        {"Metric": "Rows after exact duplicate removal", "Value": len(df)},
        {"Metric": "Missing runtime values", "Value": int(df["Runtime"].isna().sum())},
        {"Metric": "Zero budget values", "Value": int((df["Budget"] == 0).sum())},
        {"Metric": "Zero runtime values", "Value": int((df["Runtime"] == 0).sum())},
        {"Metric": "Zero vote-average values", "Value": int((df["Vote Average"] == 0).sum())},
        {"Metric": "Zero vote-count values", "Value": int((df["Vote Count"] == 0).sum())},
    ])
    quality.to_csv(OUTPUT_DIR / "data_quality_report.csv", index=False)

    # Chart 1: top ten recorded revenues.
    chart_df = df.nlargest(10, "Revenue").sort_values("Revenue")
    plt.figure(figsize=(10, 6))
    plt.barh(chart_df["Title"].astype(str), chart_df["Revenue"])
    plt.xlabel("Recorded revenue (currency not specified in source)")
    plt.title("Top 10 Movies by Recorded Revenue")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_10_revenue.png", dpi=160)
    plt.close()

    # Chart 2: number of records by release year.
    plt.figure(figsize=(10, 5))
    plt.plot(year_summary["Release Year"], year_summary["Movie_Records"], marker="o")
    plt.xlabel("Release year")
    plt.ylabel("Number of movie records")
    plt.title("Movie Records by Release Year")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "movies_by_year.png", dpi=160)
    plt.close()

    print(f"Loaded worksheet: {sheet}")
    print(f"Rows analyzed: {len(df):,}")
    print(f"Outputs saved to: {OUTPUT_DIR}")
    print(f"Top recorded revenue: {df.loc[df['Revenue'].idxmax(), 'Title']}")


if __name__ == "__main__":
    main()
