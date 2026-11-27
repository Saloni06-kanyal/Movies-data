-- Movie Data Analytics Project: SQL practice and analysis
-- Database: SQLite (also adaptable to PostgreSQL/MySQL with minor changes)
--
-- Setup:
-- 1. Create a table named movies using the schema below.
-- 2. Import the cleaned dataset into this table, mapping the workbook headers
--    to the snake_case column names below.
-- 3. Run each SELECT query to explore the dataset.
--
-- Note: source currency is not documented. Revenue values are kept as recorded.

CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER,
    title TEXT,
    budget REAL,
    original_language TEXT,
    popularity REAL,
    release_date TEXT,
    revenue REAL,
    runtime REAL,
    vote_average REAL,
    vote_count INTEGER
);

-- Q1. Inspect the table size.
SELECT COUNT(*) AS movie_records
FROM movies;

-- Q2. Find the 10 movies with the highest recorded revenue.
SELECT title, release_date, original_language, revenue, vote_average, vote_count
FROM movies
WHERE revenue IS NOT NULL
ORDER BY revenue DESC
LIMIT 10;

-- Q3. Find highly rated movies with at least 100 votes.
SELECT title, release_date, vote_average, vote_count
FROM movies
WHERE vote_average > 0
  AND vote_count >= 100
ORDER BY vote_average DESC, vote_count DESC
LIMIT 20;

-- Q4. Count movie records by original language.
SELECT COALESCE(original_language, 'Unknown') AS language,
       COUNT(*) AS movie_records,
       ROUND(AVG(NULLIF(vote_average, 0)), 2) AS average_nonzero_rating
FROM movies
GROUP BY original_language
ORDER BY movie_records DESC;

-- Q5. Count records and calculate average rating by release year.
SELECT CAST(SUBSTR(release_date, 1, 4) AS INTEGER) AS release_year,
       COUNT(*) AS movie_records,
       ROUND(AVG(NULLIF(vote_average, 0)), 2) AS average_nonzero_rating,
       SUM(revenue) AS total_recorded_revenue
FROM movies
WHERE release_date IS NOT NULL
  AND LENGTH(release_date) >= 4
  AND SUBSTR(release_date, 1, 4) GLOB '[0-9][0-9][0-9][0-9]'
GROUP BY SUBSTR(release_date, 1, 4)
ORDER BY release_year;

-- Q6. Check for missing or questionable values.
SELECT
    SUM(CASE WHEN title IS NULL OR TRIM(title) = '' THEN 1 ELSE 0 END) AS missing_titles,
    SUM(CASE WHEN release_date IS NULL OR TRIM(release_date) = '' THEN 1 ELSE 0 END) AS missing_release_dates,
    SUM(CASE WHEN runtime IS NULL THEN 1 ELSE 0 END) AS missing_runtimes,
    SUM(CASE WHEN budget IS NULL THEN 1 ELSE 0 END) AS missing_budgets,
    SUM(CASE WHEN budget = 0 THEN 1 ELSE 0 END) AS zero_budgets,
    SUM(CASE WHEN revenue = 0 THEN 1 ELSE 0 END) AS zero_revenues,
    SUM(CASE WHEN vote_count = 0 OR vote_count IS NULL THEN 1 ELSE 0 END) AS no_vote_records
FROM movies;

-- Q7. Compare revenue and budget where both are positive.
-- This is not profit; it excludes marketing, distribution, taxes, and other costs.
SELECT title, budget, revenue,
       revenue - budget AS revenue_minus_budget,
       ROUND(100.0 * (revenue - budget) / budget, 2) AS revenue_over_budget_percent
FROM movies
WHERE budget > 0 AND revenue > 0
ORDER BY revenue_minus_budget DESC
LIMIT 20;

-- Q8. Explore the relationship between popularity and revenue.
-- Review a scatter plot as well; correlation does not establish causation.
SELECT title, popularity, revenue, vote_average, vote_count
FROM movies
WHERE popularity IS NOT NULL AND revenue IS NOT NULL
ORDER BY popularity DESC
LIMIT 100;

-- Q9. Identify potential duplicate records by movie ID.
SELECT movie_id, COUNT(*) AS record_count
FROM movies
WHERE movie_id IS NOT NULL
GROUP BY movie_id
HAVING COUNT(*) > 1
ORDER BY record_count DESC;

-- Q10. Calculate revenue summaries by original language.
SELECT COALESCE(original_language, 'Unknown') AS language,
       COUNT(*) AS movie_records,
       ROUND(AVG(NULLIF(revenue, 0)), 2) AS average_nonzero_revenue,
       MAX(revenue) AS highest_recorded_revenue
FROM movies
GROUP BY original_language
ORDER BY movie_records DESC;
