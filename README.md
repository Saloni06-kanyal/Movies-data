# Movie Data Analytics Project

An entry-level data analytics portfolio project exploring movie revenue, audience ratings, original languages, release years, and data quality using Excel and Python.

## Project files

| File | Purpose |
|---|---|
| [Movies_Data_Analytics_Project.xlsx](Movies_Data_Analytics_Project.xlsx) | Excel workbook with original data, cleaned data, quality checks, summaries, and charts |
| [analysis.py](analysis.py) | Reproducible Python analysis that creates summary CSV files and charts |
| [requirements.txt](requirements.txt) | Python package dependencies |
| [README.md](README.md) | Project overview, methods, findings, and limitations |

## Dataset

The workbook contains 4,535 rows before exact duplicate removal and 10 original fields: title, budget, movie ID, original language, popularity, release date, revenue, runtime, vote average, and vote count. The dates in this file range from 2000 to 2017.

**Dataset provenance:** The source URL/licence was not included in the supplied file, so I have not guessed or attributed a source. Add the original provider URL and its usage/licensing terms here when known.

## Questions explored

- Which movies have the highest recorded revenue?
- Which highly rated movies also have at least 100 votes?
- Which original languages appear most often in this dataset?
- Which release years contain the most records?
- What data-quality issues should be considered before interpreting the results?

## Key findings from this dataset

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

## Run the Python analysis

Use Python 3.10+ and place `Movies_Data_Analytics_Project.xlsx` in the same folder as `analysis.py`.

```bash
pip install -r requirements.txt
python analysis.py
```

The script reads the `Cleaned_Data` worksheet when available (otherwise it reads the first worksheet) and writes CSV summaries and PNG charts to an `outputs/` folder.

## Limitations

- The source file does not document currency, dataset provider, or licensing; verify these before making stronger claims or redistributing the data.
- Coverage is limited to records supplied in the workbook and is not assumed to include every movie released during 2000–2017.
- Revenue is not the same as profit.
- Descriptive patterns do not establish cause and effect.

## Possible future improvements

- Add the original dataset citation and licence.
- Build an interactive dashboard in Power BI or Tableau.
- Add SQL queries or a Jupyter notebook if extending the project toward a code-based analytics portfolio.
