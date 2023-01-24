import math
import time

start_time = time.perf_counter()

with open('frequencies_txt', 'r') as file:
    frequency = file.read().splitlines()
print(f"Częstotliwości wysłane na generator: {', '.join(frequency)} MHz")

for i, freq in enumerate(frequency, 1):
    print(f"Częstotliwość nr {i}: {freq}")

end_time = time.perf_counter()

print(f"Elapsed time: {(end_time - start_time)*math.pow(10, 6)} us")

