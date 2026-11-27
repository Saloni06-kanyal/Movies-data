"""Reproducible analysis for the Movie Data Analytics portfolio project.

Place Movies_Data_Analytics_Project.xlsx beside this script, then run:
    pip install -r requirements.txt
    python analysis.py

Creates CSV summaries, an insights text file, and PNG charts in ./outputs/.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
WORKBOOK = BASE_DIR / "Movies_Data_Analytics_Project.xlsx"
OUTPUT_DIR = BASE_DIR / "outputs"

NUMERIC_COLUMNS = [
    "Budget", "Popularity", "Revenue", "Runtime", "Vote Average", "Vote Count"
]


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
        "Revenue", "Runtime", "Vote Average", "Vote Count", "Popularity"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Workbook is missing required columns: {sorted(missing)}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")
    df["Release Year"] = df["Release Date"].dt.year

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Exclude exact duplicate rows if the selected worksheet contains any.
    rows_read = len(df)
    df = df.drop_duplicates().copy()
    duplicate_rows_removed = rows_read - len(df)

    # Revenue ranking uses recorded values; currency is not documented in the source.
    top_revenue = df.nlargest(20, "Revenue")[
        ["Title", "Release Year", "Original Language", "Budget", "Revenue",
         "Vote Average", "Vote Count", "Popularity"]
    ]
    top_revenue.to_csv(OUTPUT_DIR / "top_revenue_movies.csv", index=False)

    # A minimum vote count makes the rating ranking less sensitive to tiny samples.
    top_rated = df[
        (df["Vote Count"] >= 100) & (df["Vote Average"] > 0)
    ].sort_values(["Vote Average", "Vote Count"], ascending=[False, False]).head(20)
    top_rated[
        ["Title", "Release Year", "Original Language", "Vote Average", "Vote Count"]
    ].to_csv(OUTPUT_DIR / "top_rated_movies_100_votes.csv", index=False)

    language_summary = df.groupby("Original Language", dropna=False).agg(
        Movie_Records=("Title", "size"),
        Average_Vote=("Vote Average", "mean"),
        Total_Recorded_Revenue=("Revenue", "sum"),
        Median_Popularity=("Popularity", "median"),
    ).reset_index().sort_values("Movie_Records", ascending=False)
    language_summary.to_csv(OUTPUT_DIR / "language_summary.csv", index=False)

    year_summary = df.dropna(subset=["Release Year"]).groupby("Release Year").agg(
        Movie_Records=("Title", "size"),
        Average_Vote=("Vote Average", "mean"),
        Total_Recorded_Revenue=("Revenue", "sum"),
        Median_Popularity=("Popularity", "median"),
    ).reset_index().sort_values("Release Year")
    year_summary.to_csv(OUTPUT_DIR / "year_summary.csv", index=False)

    # Quality report makes assumptions visible instead of silently imputing data.
    quality = pd.DataFrame([
        {"Metric": "Rows read from selected worksheet", "Value": rows_read},
        {"Metric": "Exact duplicate rows removed by script", "Value": duplicate_rows_removed},
        {"Metric": "Rows after exact duplicate removal", "Value": len(df)},
        {"Metric": "Missing title values", "Value": int(df["Title"].isna().sum())},
        {"Metric": "Missing release dates", "Value": int(df["Release Date"].isna().sum())},
        {"Metric": "Missing runtime values", "Value": int(df["Runtime"].isna().sum())},
        {"Metric": "Zero budget values", "Value": int((df["Budget"] == 0).sum())},
        {"Metric": "Zero revenue values", "Value": int((df["Revenue"] == 0).sum())},
        {"Metric": "Zero runtime values", "Value": int((df["Runtime"] == 0).sum())},
        {"Metric": "Zero vote-average values", "Value": int((df["Vote Average"] == 0).sum())},
        {"Metric": "Zero or missing vote-count values", "Value": int((df["Vote Count"].fillna(0) == 0).sum())},
    ])
    quality.to_csv(OUTPUT_DIR / "data_quality_report.csv", index=False)

    # Correlation is exploratory and does not imply cause and effect.
    correlation_columns = ["Revenue", "Budget", "Popularity", "Vote Average", "Vote Count", "Runtime"]
    corr = df[correlation_columns].corr(numeric_only=True)
    corr.to_csv(OUTPUT_DIR / "numeric_correlation_matrix.csv")

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

    # Chart 3: popularity versus recorded revenue; log scale helps show wide ranges.
    scatter_df = df[
        (df["Popularity"] > 0) & (df["Revenue"] > 0)
    ].dropna(subset=["Popularity", "Revenue"])
    plt.figure(figsize=(8, 6))
    plt.scatter(scatter_df["Popularity"], scatter_df["Revenue"], alpha=0.55)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Popularity (log scale)")
    plt.ylabel("Recorded revenue (log scale)")
    plt.title("Movie Popularity vs Recorded Revenue")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "popularity_vs_revenue.png", dpi=160)
    plt.close()

    # Chart 4: ratings against vote counts for titles with positive values.
    rating_df = df[
        (df["Vote Average"] > 0) & (df["Vote Count"] > 0)
    ].dropna(subset=["Vote Average", "Vote Count"])
    plt.figure(figsize=(8, 6))
    plt.scatter(rating_df["Vote Count"], rating_df["Vote Average"], alpha=0.5)
    plt.xscale("log")
    plt.xlabel("Vote count (log scale)")
    plt.ylabel("Vote average")
    plt.title("Audience Rating vs Number of Votes")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "ratings_vs_vote_count.png", dpi=160)
    plt.close()

    # Chart 5: most common original-language codes.
    top_languages = language_summary.head(10).copy()
    top_languages["Language Label"] = top_languages["Original Language"].fillna("Unknown").astype(str)
    top_languages = top_languages.sort_values("Movie_Records")
    plt.figure(figsize=(8, 5))
    plt.barh(top_languages["Language Label"], top_languages["Movie_Records"])
    plt.xlabel("Number of movie records")
    plt.title("Top 10 Original Languages by Record Count")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_languages.png", dpi=160)
    plt.close()

    # Generate short, data-driven notes for a portfolio README/demo.
    highest_revenue = df.loc[df["Revenue"].idxmax()] if df["Revenue"].notna().any() else None
    valid_rated = df[(df["Vote Count"] >= 100) & (df["Vote Average"] > 0)]
    highest_rated = valid_rated.sort_values(
        ["Vote Average", "Vote Count"], ascending=[False, False]
    ).head(1)
    most_common_language = language_summary.head(1)
    most_common_year = year_summary.sort_values("Movie_Records", ascending=False).head(1)

    lines = [
        "MOVIE DATA ANALYTICS — GENERATED INSIGHTS",
        "",
        f"Worksheet analyzed: {sheet}",
        f"Rows read: {rows_read:,}",
        f"Exact duplicate rows removed: {duplicate_rows_removed:,}",
        f"Rows analyzed after duplicate removal: {len(df):,}",
        "Currency: not specified in the source workbook; revenue values are reported as recorded.",
        "",
    ]
    if highest_revenue is not None:
        lines.append(
            f"Highest recorded revenue: {highest_revenue['Title']} "
            f"({highest_revenue['Revenue']:,.0f})."
        )
    if not highest_rated.empty:
        row = highest_rated.iloc[0]
        lines.append(
            f"Highest vote average among titles with at least 100 votes: {row['Title']} "
            f"({row['Vote Average']:.2f}; {row['Vote Count']:.0f} votes)."
        )
    if not most_common_language.empty:
        row = most_common_language.iloc[0]
        lines.append(
            f"Most common original-language code: {row['Original Language']} "
            f"({int(row['Movie_Records']):,} records)."
        )
    if not most_common_year.empty:
        row = most_common_year.iloc[0]
        lines.append(
            f"Most represented release year: {int(row['Release Year'])} "
            f"({int(row['Movie_Records']):,} records)."
        )
    lines.extend([
        "",
        "Cautions:",
        "- Revenue is not profit.",
        "- Zero budgets may represent unknown or unreported values.",
        "- Descriptive patterns and correlations do not establish causation.",
        "- Confirm the dataset source, licence, and currency before redistribution or stronger claims.",
    ])
    (OUTPUT_DIR / "insights_summary.txt").write_text("\n".join(lines), encoding="utf-8")

    print(f"Loaded worksheet: {sheet}")
    print(f"Rows read: {rows_read:,}; exact duplicates removed: {duplicate_rows_removed:,}")
    print(f"Rows analyzed: {len(df):,}")
    print(f"Outputs saved to: {OUTPUT_DIR}")
    if highest_revenue is not None:
        print(f"Top recorded revenue: {highest_revenue['Title']}")
    print("Charts: top_10_revenue.png, movies_by_year.png, popularity_vs_revenue.png,")
    print("        ratings_vs_vote_count.png, top_languages.png")


if __name__ == "__main__":
    main()
