import pandas as pd
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv('2023-world-cup-predictions/data/wwc2023.csv')

# Normalize the "win" column to represent abilities
df["ability"] = df["win"] / df["win"].sum()

# Get the unique teams
teams = df["team"].unique()

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

# Convert probabilities to numeric
pairwise_probs = pairwise_probs.apply(pd.to_numeric)

# Create a heatmap figure
fig = go.Figure(data=go.Heatmap(
    z=pairwise_probs.values,
    x=teams,
    y=teams,
    colorscale='Viridis'
))

# Customize the layout
fig.update_layout(
    title='Pairwise Comparisons',
    xaxis=dict(title='Team B'),
    yaxis=dict(title='Team A'),
)

# Add annotations to the heatmap
for i, team_a in enumerate(teams):
    for j, team_b in enumerate(teams):
        if team_a != team_b:
            fig.add_annotation(
                x=team_b,
                y=team_a,
                text=f'{pairwise_probs.loc[team_a, team_b]:.2f}',
                showarrow=False,
                font=dict(color='white' if i != j else 'black')
            )

# Display the interactive plot
fig.show()
