from functools import lru_cache

while True:
    try:
        raw = input("Enter the pinatas array (integers separated by spaces): ")
        pinatas = list(map(int, raw.strip().split()))
        # If the array has many zeros use:
        # pinatas = [x for x in map(int, raw.strip().split()) if x != 0]
        break
    except ValueError:
        print("Error: you must enter only integers separated by spaces. Try again")

nums = [1] + pinatas + [1]
n = len(nums)


@lru_cache(None)
def dp(left, right):
    if left + 1 >= right:
        return 0
    best = 0
    for i in range(left + 1, right):
        best = max(best, dp(left, i) + dp(i, right) + nums[left] * nums[i] * nums[right])
    return best


print("Max candies:", dp(0, n-1))
