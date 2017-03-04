###Simple 'previous game' algorithm

- Get previous game for each team
- Calculate risk for it = goals win - goals lose
- Total risk = home_risk - guest_risk
- Rule: total_risk < 0 ? second : first

## Results:
| ------ | ------ |
| We gain | -56.63 |
| Per game gain | -0.0460 |
| Correct predictions | 701 |
| Incorrect predictions | 490 |
| We cannot predict | 39 |