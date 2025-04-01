from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd

# Prompt for teammate name
exclude_name = input("Enter the name of the teammate to exclude (e.g., Jamal Murray): ")

# Step 1: Get player IDs
jokic_id = players.find_players_by_full_name("Nikola Jokic")[0]['id']
exclude_player = players.find_players_by_full_name(exclude_name)

if not exclude_player:
    print(f"No player found for '{exclude_name}'.")
    exit()

exclude_id = exclude_player[0]['id']

# Step 2: Pull game logs for both players (can expand seasons)
season = '2024'
print(f"Fetching Jokic + {exclude_name}'s logs for {season} season...")

jokic_log = playergamelog.PlayerGameLog(player_id=jokic_id, season=season, season_type_all_star='Regular Season')
exclude_log = playergamelog.PlayerGameLog(player_id=exclude_id, season=season, season_type_all_star='Regular Season')

jokic_df = jokic_log.get_data_frames()[0]
exclude_df = exclude_log.get_data_frames()[0]

# Step 3: Filter out games where the excluded teammate played
exclude_game_ids = set(exclude_df['Game_ID'])
filtered_df = jokic_df[~jokic_df['Game_ID'].isin(exclude_game_ids)]

# Step 4: Convert GAME_DATE and sort by most recent
filtered_df['GAME_DATE'] = pd.to_datetime(filtered_df['GAME_DATE'])
filtered_df = filtered_df.sort_values(by="GAME_DATE", ascending=False)

# Step 5: Save to file
filename = f"jokic_without_{exclude_name.lower().replace(' ', '_')}_2024.csv"
filtered_df.to_csv(filename, index=False)
print(f"Saved file: {filename}")
