import datetime

import SMF100A_ESU40_v2


def result_file_name(name_of_file):
    now = datetime.datetime.now()
    year = str(now.year)
    month = "%02d" % now.month
    day = "%02d" % now.day
    hour = "%02d" % now.hour
    minute = "%02d" % now.minute
    second = "%02d" % now.second
    prefix_name = year + month + day + "_" + hour + minute + second + "_"
    full_name_of_file = prefix_name + name_of_file + ".txt"
    return full_name_of_file


print("Wprowadź nazwę pliku: ")
file_name = input()
final_file_name = result_file_name(file_name)
print(final_file_name)
final_results_txt = open(f"{final_file_name}", "w")

for value in SMF100A_ESU40_v2.frequency:
    final_results_txt.write("f [MHz]\tU [dBuV]")
