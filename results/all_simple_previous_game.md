###All Simple 'previous game' algorithm

- Get all previous game for each team
- Calculate risk for it = goals win - goals lose
- Total risk = home_risk - guest_risk
- Rule: total_risk < 0 ? second : first

## Results:
| ------ | ------ |
| Correct prediction percent | 66% |
| We gain | -55.35 |
| Per game gain | -0.045 |
| Correct predictions | 791 |
| Incorrect predictions | 400 |
| We cannot predict | 39 |