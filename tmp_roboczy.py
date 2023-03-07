import random
import statistics as stat

with open("C:\\Users\\bglowacz\\PycharmProjects\\Praca_IL-PIB\\frequencies_txt", "r") as frequencies_file:
    frequencies = frequencies_file.readlines()

frequencies = [float(x) for x in frequencies]
level = []
result_list = []

for x in frequencies:
    random_number = random.randint(1, 100)
    level.append(random_number)
print("Oryginalne poziomy: ", level)

standard_deviation = stat.pstdev(level)
print(f"Odchylenie standardowe wynosi: {standard_deviation}")
median = stat.median(level)
print(f"Mediana wynosi: {median}")

for x in range(0, len(frequencies)):
    while level[x] < median:
        random_number = random.randint(1, 100)
        level[x] = random_number
        str(level[x]).replace(str(x), str(random_number))

    result_list.append(str(frequencies[x]) + "  " + str(level[x]) + "")
print(f"Nowe poziomy, z zamienionymi wartościami poniżej mediany: {level}")
print(result_list)

result_file = open("result.txt", "w")
for x in range(0, len(frequencies)):
    result_file.write(result_list[x])

