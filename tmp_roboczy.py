file = open("frequencies_txt", "r")
frequency = file.readline()

while frequency:
    if frequency == "\n":
        break
    frequency = file.readline()
    print(f"wartość podana do generatora: {frequency}\n")