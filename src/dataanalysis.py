
import pandas as pd
from utils.paths import get_project_root
from pathlib import Path
from pandasql import sqldf
from sqlalchemy.sql import text

df = pd.read_csv(get_project_root() / 'data' / 'nfl_games_2001_2024.csv')



# SQL query to calculate spread, total, and result
query = """
SELECT 
    CASE WHEN spread_line > 0 THEN spread_line ELSE -spread_line END AS spread,
    total_line,
    CASE WHEN spread_line > 0 THEN home_score - away_score ELSE away_score - home_score END AS result,
    home_score, away_score,
    CASE WHEN spread_line > 0 THEN 1 ELSE 0 END AS home_team_favored
FROM df
WHERE home_score IS NOT NULL AND away_score IS NOT NULL
"""
query2 = f"""
SELECT
    total_line,
    spread,
    home_team_favored,
    CASE WHEN result - spread > -6 THEN TRUE ELSE FALSE END AS teaser_covered
    FROM 
    ({query})
WHERE spread >= 7.5 AND spread <= 8.5
"""

query3 = f"""
SELECT
    total_line,
    spread,
    home_team_favored,
    CASE WHEN result - spread < 6 THEN TRUE ELSE FALSE END AS teaser_covered
    FROM 
    ({query})
WHERE spread >= 1.5 AND spread <= 2.5
"""
# Run query using pandasql
resultdf = sqldf(query2, locals())
print(resultdf.head())
query4 = """
SELECT COUNT(*)
    FROM resultdf
WHERE teaser_covered = TRUE
"""
print(f' Number of cases where teaser covered: {sqldf(query4, locals())}')

# Logistic regression: teaser_covered ~ spread + total_line
import statsmodels.api as sm

# Ensure teaser_covered is binary (0/1)
resultdf['teaser_covered'] = resultdf['teaser_covered'].astype(int)

# Define predictors and outcome
X = resultdf[ 'total_line']
X = sm.add_constant(X)  # Adds intercept term
y = resultdf['teaser_covered']

# Fit logistic regression model
model = sm.Logit(y, X)
result = model.fit()
print(result.summary())

sample_data = pd.DataFrame({
    'total_line': [40, 42, 46]
})
sample_data = sm.add_constant(sample_data)


print(result.predict(sample_data))

