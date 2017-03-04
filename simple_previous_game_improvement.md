
###Simple 'previous game' algorithm
## Improvement:

If total_risk is close to 0, we cannot correctly predict - then better to refuse.
CLOSE_TO_ZERO = between [-2, 2].

## Results:
| ------ | ------ |
| We gain | -36.7 |
| Per game gain | -0.029 |
| Correct predictions | 647 |
| Incorrect predictions | 420 |
| We cannot predict | 39 |
| Refusals | 124 |