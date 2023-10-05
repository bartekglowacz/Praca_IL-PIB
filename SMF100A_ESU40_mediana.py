"""
Program do obsługi ESU40 i SMF100A. Rozpatrywane częstotliwości zadaje się z pliku txt. Wyniki również otrzymuje się w pliku txt.
W przypadku kiedy ESU40 odczyta jakiś poziom znacznie odbiegający od pozostałych - pomiar jest powtarzany w tym punkcie z wydłużonym
czasem pomiaru. Kryterium, które uznaje wynik za dobry lub nie jest mediana pomniejszona o 5. Jeżeli wartość odczytana jest mniejsza
od tej wartości to pomiar jest powtarzany.
"""

import datetime
import statistics
import time
import pyvisa
import SMF100A_preset
import ESU40_preset
import matplotlib.pyplot as draw


# Funkcja do nadawania nazwy plikom wynikowym
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


def set_frequency():
    file = open('frequencies_txt', 'r')
    frequency = file.read().splitlines()
    frequency = [float(x.replace(",", ".")) for x in frequency]
    return frequency


def wait(measurement_pause):
    time.sleep(measurement_pause / 1000)


class Device:
    def __init__(self, name, ip_address, frequency_band):
        self.name = name
        self.name_connected = None
        self.ip_address = ip_address
        self.frequency_band = frequency_band

    def connect(self):
        # Connect to the device over LAN
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.name_connected = rm.open_resource(f'TCPIP::{self.ip_address}::INSTR', timeout=10000) #timeout gdyby ESU miało problem z wyrabianiem z odczytem

    def IDN(self):
        print(f"Dane podłączonego urządzenia:\nNazwa: {self.name}\nIDN: {self.name_connected.query('*IDN?')}")

    def frequencies_swapping(self):
        self.frequency_band = set_frequency()
        # print(self.frequency_band)


esu_results = []
smf_results = []

# tworzenie klasy ESU40
ESU40 = Device("ESU40", "10.0.0.4", "frequencies.txt")
ESU40.connect()
ESU40.IDN()
ESU40.frequencies_swapping()

# tworzenie klasy SMF 100A
SMF100A = Device("SMF100A", "10.0.0.3", "frequencies.txt")
SMF100A.connect()
SMF100A.IDN()
SMF100A.frequencies_swapping()

# ustawienie wstępne SMF 100A:
print("Tłumik na SMF o stałej wartości - wpisz 1\nTłumik automatyczny - wpisz 2")
choice = int(input())
if choice == 1:  # tłumik o stałej wartości
    print(f"Wprowadź wartość tłumika na {SMF100A.name}")
    attenuator_value = input()
    SMF100A_preset.set_attenuator(attenuator_value)
if choice == 2:  # tłumik automatyczny
    SMF100A_preset.set_auto_attenuator()
SMF100A_preset.select_unit("dBuV")
print(f"Wprowadź wartość poziomu napięcia na {SMF100A.name}")
level = float(input())
SMF100A_preset.set_level(level)
SMF100A_preset.output_on_off("ON")

# ustawienie wstępne ESU40:
ESU40_preset.ESU40_reset()
ESU40_preset.display_on()
ESU40_preset.select_coupling("AC")
ESU40_preset.select_RF_input(1)

ESU40_preset.set_auto_attenuator()
# ESU40_preset.set_RefLevel(30) # dla pomiarów z ręcznym ustawieniem poziomu odniesienia [dB]

ESU40_preset.set_detector("AVER")
ESU40_preset.set_span()

frequency = set_frequency()
print(f"{frequency = }")
print("Podaj czas pomiaru w milisekundach")
pause = float(input())

for x in frequency:
    SMF100A.name_connected.write(f"FREQ {x} MHz") #ustawianie częstotliwości na SMF
    SMF100A_freq = float(SMF100A.name_connected.query('FREQ?')) / 10 ** 6  # odczytywanie częstotliwości SMF 100A
    ESU40.name_connected.write(f"FREQ:CENT {x} MHz") #ustawianie częstotliwości środkowej na ESU
    ESU40_preset.set_RBW()
    ESU40_preset.set_measurement_time("auto") #ZMIANA CZASU POMIARU ("auto")
    ESU40.name_connected.write("CALC:MARK:MAX")
    # ESU_freq = float(ESU40.name_connected.query('SENSe:FREQuency:CENTer?')) / 10 ** 6  # odczytywanie częstotliwości ESU40
    ESU_level = float(ESU40.name_connected.query_ascii_values('CALC:MARK1:Y?')[0]) #odczyt poziomu na ustawionej częstotlwości poprzez ustawienie markera
    wait(pause)
    # print(f"f na {SMF100A.name}: {x}")
    print(f"f z ekranu SMF: {SMF100A_freq} MHz")
    # print("poziom generatora: ", SMF100A.name_connected.query("POW?")) # odczytywanie wartości napięcia z ekranu SMF 100A
    # print(f"f na {ESU40.name}: {x}")
    # print(f"f z ekranu ESU: {ESU_freq} MHz")
    print("U z ekranu ESU40: ", ESU_level)  # odczytywanie poziomy sygnału z ESU40
    smf_results.append(x)
    esu_results.append(ESU_level)

print(f"Częstotliwości: {smf_results}")
print(f"Oryginalne poziomy: {esu_results}")

median = statistics.median(esu_results)
print(f"\nMediana wyników z ESU40: {median}\n")

for x in range(0, len(smf_results)):
    if esu_results[x] < median - 70: #czasami ESU nie wyrabia z odczytem i łapie dziurę - ta instrukcja jest po to żeby tę dziurę domierzyć z wydłużonym czasem pomiaru
        t = 5000
        SMF100A.name_connected.write(f"FREQ {smf_results[x]} MHz")
        print(f"Domiarka na f = {smf_results[x]} MHz")
        ESU40.name_connected.write(f"FREQ:CENT {smf_results[x]} MHz")
        ESU40_preset.set_RBW()
        ESU40_preset.set_measurement_time(1000)  # domiarka z czasem 1000 ms
        ESU40.name_connected.write("CALC:MARK1:MAX")
        ESU_level = float(ESU40.name_connected.query_ascii_values('CALC:MARK1:Y?')[0])
        wait(t)
        print(f"Wartość domierzona: {ESU_level}")
        print(f"Czas odczytu wynosi {t} ms")
        esu_results[x] = ESU_level
    else:
        esu_results[x] = esu_results[x]

# Tworzenie pliku z wynikami
print("Wprowadź nazwę pliku: ")
file_name = input()
final_file_name = result_file_name(file_name)
final_results_txt = open(f"C:\\Users\\bglowacz\\PycharmProjects\\Praca_IL-PIB\\pliki wynikowe txt\\{final_file_name}",
                         "w")

final_results_txt.write("f [MHz]\tU [dBuV]\n")
for x in range(0, len(smf_results)):
    final_results_txt.write(str(smf_results[x]).replace(".", ",") + "\t" + str(esu_results[x]).replace(".", ",") + "\n")
final_results_txt.close()

SMF100A_preset.output_on_off("OFF")

###