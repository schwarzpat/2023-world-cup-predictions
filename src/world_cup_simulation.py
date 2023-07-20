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

def simulate_knockout_stage(match_setup, teams):
    winners = []
    for match in match_setup:
        team1 = teams.loc[teams["team"] == match[0]]
        team2 = teams.loc[teams["team"] == match[1]]
        outcome, _ = simulate_match(team1, team2)
        if outcome >= 0.5:
            winners.append(match[0])
        else:
            winners.append(match[1])
    return winners

def simulate_tournament(teams):
    group_winners = []
    group_runners_up = []
    for group_name, group in teams.groupby("group"):
        standings = simulate_group(group)
        group_winners.append(standings.iloc[0]["team"])
        group_runners_up.append(standings.iloc[1]["team"])

    round_of_16 = [
        [group_winners[0], group_runners_up[2]],  # 1st Group A vs 2nd Group C
        [group_winners[2], group_runners_up[0]],  # 1st Group C vs 2nd Group A
        [group_winners[4], group_runners_up[6]],  # 1st Group E vs 2nd Group G
        [group_winners[6], group_runners_up[4]],  # 1st Group G vs 2nd Group E
        [group_winners[1], group_runners_up[3]],  # 1st Group B vs 2nd Group D
        [group_winners[3], group_runners_up[1]],  # 1st Group D vs 2nd Group B
        [group_winners[5], group_runners_up[7]],  # 1st Group F vs 2nd Group H
        [group_winners[7], group_runners_up[5]]   # 1st Group H vs 2nd Group F
    ]

    winners_round_of_16 = simulate_knockout_stage(round_of_16, teams)

    quarterfinals = [
        [winners_round_of_16[0], winners_round_of_16[2]],
        [winners_round_of_16[1], winners_round_of_16[3]],
        [winners_round_of_16[4], winners_round_of_16[6]],
        [winners_round_of_16[5], winners_round_of_16[7]]
    ]

    winners_quarterfinals = simulate_knockout_stage(quarterfinals, teams)

    semifinals = [
        [winners_quarterfinals[0], winners_quarterfinals[1]],
        [winners_quarterfinals[2], winners_quarterfinals[3]]
    ]

    winners_semifinals = simulate_knockout_stage(semifinals, teams)

    finals = [winners_semifinals[0], winners_semifinals[1]]

    winner_final = simulate_knockout_stage([finals], teams)[0]

    return winner_final

teams = pd.read_csv('2023-world-cup-predictions/data/wwc2023.csv')


n_simulations = 10000


results = [simulate_tournament(teams) for _ in range(n_simulations)]
win_counts = Counter(results)
win_counts_df = pd.DataFrame.from_dict(win_counts, orient='index', columns=['wins']).reset_index()
win_counts_df.rename(columns={'index': 'team'}, inplace=True)
win_counts_df = win_counts_df.sort_values(by='wins', ascending=False)
win_counts_df['wins'] = win_counts_df['wins'] / n_simulations * 100


# Plot distribution of winners
plt.style.use('dark_background')
plt.figure(figsize=(10,8))
bars = plt.barh(win_counts_df['team'], win_counts_df['wins'], color='skyblue')

# Label the bars with their percentage values
for bar in bars:
    width = bar.get_width()
    plt.text(width + 1,  # x position
             bar.get_y() + bar.get_height() / 2,  # y position
             f'{width:.1f}%',  # text
             ha='left',  # horizontal alignment
             va='center')  # vertical alignment

plt.xlabel('Win Percentage (%)')
plt.title('Distribution of Winners')
plt.gca().invert_yaxis()
plt.show()
