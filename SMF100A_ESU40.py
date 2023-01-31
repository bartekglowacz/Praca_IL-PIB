import time

import pyvisa

# Preset urządzeń i dodanie własnych nastaw, np. wartość tłumika lub tryb urządzenia
import SMF100A_preset
import ESU40_preset


def frequency_band_SMF(frequency_file):
    for x in range(0, len(frequency_file), 1):
        frequency_file[x] = frequency_file[x].replace(",", ".")
    # print(frequency_file)
    frequency_file = [float(x) for x in frequency_file]
    return frequency_file


def set_single_frequency_SMF(frequency_band_SMF):
    single_frequency = frequency_band_SMF  # zastąpić to 0 zmienną, która będzie czekała na odczyt z ESU
    # print(f"Na generator poszło: {single_frequency = }")
    SMF100A.write(f"FREQ {single_frequency} MHz")
    return single_frequency


def set_single_frequency_ESU(single_frequency):
    # print("Wprowadź częstotliwość: ")
    # frequency = input()
    single_frequency = set_single_frequency_SMF(frequency_band_SMF)
    ESU40.write(f"FREQ:CENT {single_frequency}MHz")


def set_level_SMF(level):
    SMF100A.write(f":POW {level} dBuV")
    SMF100A.write("OUTP ON")


def wait(ms):  # czas pauzy w milisekundach
    pause_time = time.sleep(ms / 1000)
    return pause_time


def measurement_ESU(single_frequency):
    for x in range(0, len(frequency_band_SMF), 1):
        single_frequency[x] = frequency_band_SMF[x]
        set_single_frequency_SMF(single_frequency[x])
        wait(ms)
        set_single_frequency_ESU(single_frequency)
    return single_frequency


# Connect to the signal generator over LAN
rm = pyvisa.ResourceManager()
rm.list_resources()
SMF100A = rm.open_resource('TCPIP::169.254.2.20::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
print(f"Generator:\n{SMF100A.query('*IDN?')}")

# Connect to the receiver over LAN
rm = pyvisa.ResourceManager()
rm.list_resources()
ESU40 = rm.open_resource('TCPIP::169.254.2.22::INSTR')
print(f"Odbiornik:\n{ESU40.query('*IDN?')}")

file = open('frequencies_txt', 'r')
frequency = file.read().splitlines()
frequency_band_SMF = frequency_band_SMF(frequency)
print(f"{frequency_band_SMF = }")

print("Podaj poziom generowanego sygnału [dBuV]: ")
level = float(input())

print("Czas postoju: ")
ms = int(input())

set_single_frequency_SMF(frequency_band_SMF)
set_single_frequency_ESU(frequency_band_SMF)
set_level_SMF(level)
measurement_ESU(frequency_band_SMF)