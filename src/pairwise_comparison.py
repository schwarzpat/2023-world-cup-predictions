import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('2023-world-cup-predictions/data/wwc2023.csv')
df.head()

# Let's normalize the "win" column to represent abilities
df["ability"] = df["win"] / df["win"].sum()

# Displaying the abilities
team_abilities = df[["team", "ability"]].sort_values(by="ability", ascending=False)
team_abilities

# Checking the unique values in the "team" column
teams = df["team"].unique()
teams

# Initialize a dataframe to store the probabilities
pairwise_probs = pd.DataFrame(index=teams, columns=teams)

# Populate the dataframe with pairwise probabilities using the Bradley-Terry model
for team_a in teams:
    for team_b in teams:
        if team_a != team_b:
            ability_a = df.loc[df["team"] == team_a, "ability"].values[0]
            ability_b = df.loc[df["team"] == team_b, "ability"].values[0]
            prob_a_beats_b = ability_a / (ability_a + ability_b)
            pairwise_probs.loc[team_a, team_b] = prob_a_beats_b

# Replace NaN (resulting from a team playing against itself) with 0.5
pairwise_probs = pairwise_probs.fillna(0.5)
pairwise_probs = pairwise_probs.apply(pd.to_numeric)

# Plotting the heatmap
plt.style.use('dark_background')
plt.figure(figsize=(20, 15))
sns.heatmap(pairwise_probs, cmap="RdYlBu_r", annot=False, cbar=True, linewidths=.5)
plt.title('Pairwise Probabilities of Teams Winning')
plt.show()