import heapq
import sys

capital = int(input("Input start capital C: "))
max_number = int(input("Input max number of laptops N: "))
total = int(input("Input total number of laptops K: "))

prices = list(map(int, input("Input price array (K numbers separated by space): ").split()))
gains = list(map(int, input("Input gain array (K numbers separated by space): ").split()))

if len(prices) != total or len(gains) != total:
    print("Error: number of prices and gains must equal K")
    sys.exit()

laptops = [(prices[i], gains[i], i+1) for i in range(total)]
laptops.sort(key=lambda x: x[0])

chosen = []
bought = 0
heap = []

i = 0

while bought < max_number:
    while i < total and laptops[i][0] <= capital:
        price, gain, idx = laptops[i]
        heapq.heappush(heap, (-gain, price, idx))
        i += 1

    if not heap:
        break

    gain_neg, price, idx = heapq.heappop(heap)
    gain = -gain_neg

    capital += gain
    chosen.append(idx)
    bought += 1

print("Final capital:", capital)
print("Chosen laptops:", chosen)