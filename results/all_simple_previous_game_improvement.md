
###All simple 'previous game' algorithm
## Improvement:

If total_risk is close to 0, we cannot correctly predict - then better to refuse.
CLOSE_TO_ZERO = between [-2, 2].

## Results:
| ------ | ------ |
| Correct prediction percent | 54% |
| We gain | -43.85 |
| Per game gain | -0.035 |
| Correct predictions | 646 |
| Incorrect predictions | 280 |
| We cannot predict | 39 |
| Refusals | 265 |
| Refusals percent | 27% |
