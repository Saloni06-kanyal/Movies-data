"""Load the repository's cleaned Excel sheet into SQLite and run sql/movie_analysis.sql."""
from pathlib import Path
import re
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "Movies_Data_Analytics_Project.xlsx"
SQL_FILE = ROOT / "sql" / "movie_analysis.sql"
OUTPUT = ROOT / "outputs"
DB_FILE = OUTPUT / "movie_analysis.sqlite"

ALIASES = {
    "movie_id": ["movieid", "id", "tmdbid", "movieidentifier"],
    "title": ["title", "movietitle", "name"],
    "budget": ["budget"],
    "original_language": ["originallanguage", "language", "originallanguagecode"],
    "popularity": ["popularity"],
    "release_date": ["releasedate", "releasedate", "dateofrelease"],
    "revenue": ["revenue"],
    "runtime": ["runtime", "duration"],
    "vote_average": ["voteaverage", "averagerating", "rating"],
    "vote_count": ["votecount", "numberofvotes", "votes"],
}
REQUIRED = set(ALIASES) - {"movie_id"}
NUMERIC = ["movie_id", "budget", "popularity", "revenue", "runtime", "vote_average", "vote_count"]


def key(value):
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def main():
    if not WORKBOOK.exists():
        raise FileNotFoundError(f"Workbook not found: {WORKBOOK}")
    if not SQL_FILE.exists():
        raise FileNotFoundError(f"SQL file not found: {SQL_FILE}")

    book = pd.ExcelFile(WORKBOOK)
    sheet = "Cleaned_Data" if "Cleaned_Data" in book.sheet_names else book.sheet_names[0]
    source = pd.read_excel(WORKBOOK, sheet_name=sheet)
    lookup = {key(col): col for col in source.columns}
    rename = {}
    for target, candidates in ALIASES.items():
        found = next((lookup[c] for c in candidates if c in lookup), None)
        if found is not None:
            rename[found] = target
        elif target in REQUIRED:
            raise ValueError(
                f"Could not map required SQL column '{target}' from worksheet '{sheet}'. "
                f"Available columns: {list(source.columns)}"
            )

    data = source.rename(columns=rename).copy()
    for col in ALIASES:
        if col not in data:
            data[col] = pd.NA
    data = data[list(ALIASES)]
    for col in NUMERIC:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    dates = pd.to_datetime(data["release_date"], errors="coerce")
    data["release_date"] = dates.dt.strftime("%Y-%m-%d")
    data = data.where(pd.notna(data), None)

    OUTPUT.mkdir(exist_ok=True)
    if DB_FILE.exists():
        DB_FILE.unlink()

    with sqlite3.connect(DB_FILE) as connection:
        # Import the data first; SQL queries must not run against an empty table.
        data.to_sql("movies", connection, if_exists="replace", index=False)
        sql_text = SQL_FILE.read_text(encoding="utf-8")
        connection.executescript(sql_text)

        count = connection.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
        if count == 0:
            raise RuntimeError("The movies table is empty; refusing to report successful SQL execution.")

        query_number = 0
        for raw_statement in sql_text.split(";"):
            statement = "\n".join(
                line for line in raw_statement.splitlines()
                if not line.lstrip().startswith("--")
            ).strip()
            if not statement or not re.match(r"(?is)^SELECT\b", statement):
                continue
            query_number += 1
            result = pd.read_sql_query(statement, connection)
            csv_path = OUTPUT / f"sql_q{query_number:02d}_results.csv"
            result.to_csv(csv_path, index=False)
            print(f"Q{query_number}: {len(result)} result row(s) -> {csv_path.relative_to(ROOT)}")

    print(f"Worksheet loaded: {sheet}")
    print(f"Source rows imported: {len(data)}")
    print(f"Rows available to SQL: {count}")
    print(f"SQL SELECT queries executed: {query_number}")
    print(f"SQLite database: {DB_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
