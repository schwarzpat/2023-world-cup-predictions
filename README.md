
# FIFA Women's World Cup Simulation

# 2023-world-cup-predictions
 Predictions for the 2023 Women WC
 
 The data is from https://www.r-bloggers.com/2023/07/probabilistic-forecasting-for-the-fifa-womens-world-cup-2023/ . The methodology is also based on the seem blog entry and the paper "Forecasting sports tournaments by ratings of (prob)abilities: A comparison for the EURO 2008" by Christoph Leitner, Achim Zeileis and Kurt Hornik. 
 
 This repository aims to implement it in python.
 
 # Pairwise Comparisons

The pairwise winning probabilities between teams are represented in the following heatmap:

![Pairwise Comparisons Heatmap](<https://github.com/schwarzpat/2023-world-cup-predictions/blob/main/figures/Figure_1.png>)

# Tournament Simulation

This code simulates the outcome of the FIFA Women's World Cup based on team consensus scores. The simulation uses the Bradley-Terry model to calculate the probabilities of match outcomes, and the simulation is run multiple times to generate a distribution of possible outcomes.

## Methodology

### 1. Bradley-Terry Model

The Bradley-Terry model is a probabilistic model that is often used to predict the outcome of a pairwise competition. In the context of a soccer match, it calculates the probability of Team A beating Team B based on their respective consensus scores. 

The model uses a logistic function to calculate this probability:

```math
p = rac{1}{1 + e^{-(	ext{{consensus}}_A - 	ext{{consensus}}_B)}}
```

This function returns a value between 0 and 1, representing the probability of Team A beating Team B. To make the favorites more likely to win, the consensus scores are multiplied by a factor greater than 1 before using them in the logistic function.

### 2. Match Simulation

Each match is simulated by generating a random number and comparing it to the calculated probability. If the random number is less than or equal to the calculated probability, Team A is considered to have won the match. If the random number is greater than the calculated probability but less than or equal to twice the calculated probability, the match is considered a draw. Otherwise, Team B is considered to have won the match.

### 3. Tournament Simulation

The tournament is simulated by first simulating all the matches in each group and calculating the final standings. The top two teams from each group advance to the knockout stage. 

In the knockout stage, pairs of teams play against each other, and the winner advances to the next round. This continues until only one team is left, which is considered the winner of the tournament.

The tournament simulation is run multiple times to generate a distribution of possible outcomes. 

## Results

The results of the simulation are a list of the winners of each simulated tournament. The distribution of winners can be visualized with a bar plot, with the x-axis representing the number of wins and the y-axis representing the teams.

![Simulated tournament wins](<lhttps://github.com/schwarzpat/2023-world-cup-predictions/blob/main/figures/Figure_2.png>)
