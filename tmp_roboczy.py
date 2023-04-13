record = open(f"C:\\Users\\bglowacz\\PycharmProjects\\Praca_IL-PIB\\pliki wynikowe txt\\20230413_125017_test.txt")
f_result = []
U_result = []
record.readline()
for x in record:
    f_result.append(float(x.partition(";")[0].replace(",", ".")))
    U_result.append(float(x.partition(";")[2].replace(",", ".")))
print(f_result)
print(U_result)
#f_record = record