# Download NFL game data since 2010: pregame spread, total, and result


import pandas as pd
from nfl_data_py import import_schedules
from utils.paths import get_project_root
from pathlib import Path


START_YEAR = 2001
END_YEAR = 2024  # Update as needed

# Get schedules for all seasons
schedules = import_schedules([year for year in range(START_YEAR, END_YEAR + 1)])

# Select relevant columns (if available)
columns = [
	'season', 'week', 'game_id', 'home_team', 'away_team',
	'spread_line', 'total_line',
	'home_score', 'away_score'
]
available_columns = [col for col in columns if col in schedules.columns]
result_df = schedules[available_columns]

# Save to CSV using project root
project_root = get_project_root()
csv_path = project_root / 'data' / 'nfl_games_2001_2024.csv'
csv_path.parent.mkdir(parents=True, exist_ok=True)
result_df.to_csv(csv_path, index=False)
print(f'NFL game data saved to {csv_path}')
