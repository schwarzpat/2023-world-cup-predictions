
import numpy as np
import pandas as pd
from scipy.stats import logistic
from collections import Counter
import matplotlib.pyplot as plt

np.random.seed(42)

def simulate_match(team1, team2):
    consensus1 = 1.5 * team1["consensus"].item()
    consensus2 = 1.5 * team2["consensus"].item()
    
    p = logistic.cdf(consensus1 - consensus2)
    
    outcome = np.random.choice([1, 0, 0.5], p=[0.9 * p, 0.9 * (1 - p), 0.1])
    if outcome == 1:
        goal_difference = np.random.rand()
    elif outcome == 0:
        goal_difference = -np.random.rand()
    else:
        goal_difference = 0

    return outcome, goal_difference

def simulate_group(group):
    group = group.reset_index(drop=True)
    standings = pd.DataFrame({"team": group["team"], "points": 0, "goal_difference": 0})
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            team1 = group.iloc[i]
            team2 = group.iloc[j]
            outcome, goal_difference = simulate_match(team1, team2)
            if outcome == 1:
                standings.loc[i, "points"] += 3
                standings.loc[i, "goal_difference"] += goal_difference
                standings.loc[j, "goal_difference"] -= goal_difference
            elif outcome == 0:
                standings.loc[j, "points"] += 3
                standings.loc[i, "goal_difference"] -= goal_difference
                standings.loc[j, "goal_difference"] += goal_difference
            else:
                standings.loc[i, "points"] += 1
                standings.loc[j, "points"] += 1
    return standings.sort_values(["points", "goal_difference"], ascending=[False, False])

def simulate_tournament(teams):
    group_winners = []
    for group_name, group in teams.groupby("group"):
        standings = simulate_group(group)
        group_winners.append(standings.iloc[0]["team"])
        group_winners.append(standings.iloc[1]["team"])

    np.random.shuffle(group_winners)
    while len(group_winners) > 1:
        team1 = teams.loc[teams["team"] == group_winners[0]]
        team2 = teams.loc[teams["team"] == group_winners[1]]
        outcome, _ = simulate_match(team1, team2)
        if outcome >= 0.5:
            del group_winners[1]
        else:
            del group_winners[0]
    return group_winners[0]

# Read the data
teams = pd.read_csv('2023-world-cup-predictions/data/wwc2023.csv')

# Number of simulations
n_simulations = 10000

# Simulate tournament
results = [simulate_tournament(teams) for _ in range(n_simulations)]

# Count the number of times each team won
win_counts = Counter(results)

# Convert to a DataFrame for easier viewing
win_counts_df = pd.DataFrame.from_dict(win_counts, orient='index', columns=['wins']).reset_index()
win_counts_df.rename(columns={'index': 'team'}, inplace=True)
win_counts_df = win_counts_df.sort_values(by='wins', ascending=False)

# Convert wins to percentages
win_counts_df['wins'] = win_counts_df['wins'] / n_simulations * 100

# Plot distribution of winners
plt.figure(figsize=(10,8))
plt.barh(win_counts_df['team'], win_counts_df['wins'], color='skyblue')
plt.xlabel('Win Percentage (%)')
plt.title('Distribution of Winners')
plt.gca().invert_yaxis()
plt.show()
