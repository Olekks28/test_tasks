# Pinata Burst Problem

## Description
This program uses @lru_cache to store subproblem results and speed up calculations.

## Input
Enter the pinatas array as integers separated by spaces.

**Note:** If the array contains many zeros, replace

```python
pinatas = list(map(int, raw.strip().split()))
```
with
```python
pinatas = [x for x in map(int, raw.strip().split()) if x != 0] 
```

## Algorithmic complexity
O(n^3), where n is the number of pinatas.



