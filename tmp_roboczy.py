import time
import math

start_time = time.perf_counter()

file = open('frequencies_txt', 'r')
frequency = file.read().splitlines()
print(f"Częstotliwości wysłane na generator: {frequency} MHz")


for x in range(0, len(frequency), 1):
    print(f"Częstotliwość nr {x+1}: {frequency[x]}")

file.close()

end_time = time.perf_counter()

print(f"Elapsed time: {(end_time - start_time)*math.pow(10, 6)} us")