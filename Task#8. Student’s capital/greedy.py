capital = int(input("Input start capital C: "))
max_number = int(input("Input max number of laptops N: "))
total = int(input("Input total number of laptops K: "))
prices = list(map(int, input("Input price array (K numbers separated by space): ").split()))
gains = list(map(int, input("Input gain array (K numbers separated by space): ").split()))

if len(prices) != total or len(gains) != total:
    print("Error: number of prices and gains must equal K")
    exit()
laptops = [(prices[i], gains[i], i+1) for i in range(total)]
bought = 0
used = [False] * len(laptops)
chosen = []

while bought < max_number:
    max_gain = -1
    max_index = -1
    for i, (price, gain, idx) in enumerate(laptops):
        if not used[i] and price <= capital:
            if gain > max_gain:
                max_gain = gain
                max_index = i
    if max_index == -1:
        break
    capital += laptops[max_index][1]
    used[max_index] = True
    bought += 1
    chosen.append(laptops[max_index][2])

print("Final capital:", capital)
print("Chosen laptops:", chosen)


