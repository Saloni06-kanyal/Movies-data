# Movie Data Analytics Project

An entry-level data analytics portfolio project exploring movie revenue, audience ratings, original languages, release years, popularity, and data quality using Excel and Python, with SQL practice queries for structured analysis.

## Project files

| File | Purpose |
|---|---|
| [Movies_Data_Analytics_Project.xlsx](Movies_Data_Analytics_Project.xlsx) | Excel workbook with original data, cleaned data, quality checks, summaries, and charts |
| [analysis.py](analysis.py) | Reproducible Python analysis that creates summary CSV files, five charts, and a generated insights summary |
| [requirements.txt](requirements.txt) | Python package dependencies |
| [sql/movie_analysis.sql](sql/movie_analysis.sql) | SQL table schema and 10 practice/analysis queries |
| [README.md](README.md) | Project overview, methods, findings, and limitations |

## Dataset

The workbook contains 4,535 rows before exact duplicate removal and 10 original fields: title, budget, movie ID, original language, popularity, release date, revenue, runtime, vote average, and vote count. The dates in this file range from 2000 to 2017.

**Dataset provenance:** The source URL/licence was not included in the supplied file, so I have not guessed or attributed a source. Add the original provider URL and its usage/licensing terms here when known.

## Questions explored

- Which movies have the highest recorded revenue?
- Which highly rated movies also have at least 100 votes?
- Which original languages appear most often in this dataset?
- Which release years contain the most records?
- How are popularity and recorded revenue related in the supplied records?
- How do vote averages vary with the number of votes?
- What data-quality issues should be considered before interpreting the results?

## Key findings from the supplied workbook

These findings are descriptive of the supplied dataset only; they should not be interpreted as complete industry-wide statistics.

- **4,533 records** remain after removing 2 exact duplicate rows.
- **Avatar** has the highest recorded revenue in this dataset: **2,787,965,087** (currency is not labelled in the source file).
- Among movies with at least 100 votes, **Your Name.** has the highest recorded vote average at **8.5**, with **1,030 votes**.
- English (`en`) is the most frequent original-language code: **3,680 records**.
- **2013** is the most represented release year, with **336 records**.
- The average recorded vote average is approximately **6.19**. Ratings with zero votes or other data limitations should be interpreted cautiously.

## Data cleaning and methodology

- Removed only exact duplicate rows; no fuzzy matching of similar titles was performed.
- Kept missing runtime values blank rather than inventing values.
- Retained zero values in the source columns. A zero budget may mean the budget was unknown or unreported; it is not proof that a movie cost nothing to make.
- Derived budget-versus-revenue metrics only when both values are greater than zero.
- “Revenue minus budget” is a simple comparison, **not profit**. Marketing, distribution, taxes, and other costs are not included.
- The Python script uses pandas for tabular analysis and matplotlib for charts.
- The charts are exploratory. Correlation does not prove cause and effect.

## Run the Python analysis

Use Python 3.10+ and place `Movies_Data_Analytics_Project.xlsx` in the same folder as `analysis.py`.

```bash
pip install -r requirements.txt
python analysis.py
```

The script reads the `Cleaned_Data` worksheet when available (otherwise it reads the first worksheet) and writes the following to an `outputs/` folder:

**CSV / text reports**
- `top_revenue_movies.csv`
- `top_rated_movies_100_votes.csv`
- `language_summary.csv`
- `year_summary.csv`
- `data_quality_report.csv`
- `numeric_correlation_matrix.csv`
- `insights_summary.txt`

**Charts**
- `top_10_revenue.png`
- `movies_by_year.png`
- `popularity_vs_revenue.png`
- `ratings_vs_vote_count.png`
- `top_languages.png`

## SQL analysis

The file [sql/movie_analysis.sql](sql/movie_analysis.sql) includes a table schema and 10 queries for record counts, top revenue, high ratings with a vote threshold, language and year summaries, data-quality checks, revenue-versus-budget comparisons, popularity exploration, duplicate IDs, and revenue summaries by language.

The SQL file expects a table named `movies` with snake_case column names, as specified in its `CREATE TABLE` statement. Create/populate that table in SQLite or another SQL database before running the queries. Importing the Excel data into a database is a separate setup step; the script does not automatically create or populate a database.

## Dashboard extension

A Tableau or Power BI dashboard is a planned extension, not a completed deliverable in this repository yet. A useful dashboard could include:
- KPI cards for movie count, average rating, and highest recorded revenue
- Top 10 movies by recorded revenue
- Movie records by release year
- Popularity versus recorded revenue scatter plot
- Filters for release year and original-language code

Use the workbook's cleaned data and label revenue units as unspecified until the original dataset documentation confirms the currency.

## Limitations

- The source file does not document currency, dataset provider, or licensing; verify these before making stronger claims or redistributing the data.
- Coverage is limited to records supplied in the workbook and is not assumed to include every movie released during 2000–2017.
- Revenue is not the same as profit.
- Descriptive patterns and correlations do not establish cause and effect.
- The SQL queries require the table to be created and populated first.

## Future improvements

- Add the original dataset citation and licence when known.
- Import the data into SQLite and run the SQL queries, validating the outputs.
- Build and publish a Tableau or Power BI dashboard.
- Add screenshots of the final dashboard and generated charts to the repository.
