import time

import pyvisa

# Preset urządzeń i dodanie własnych nastaw, np. wartość tłumika lub tryb urządzenia
import SMF100A_preset
import ESU40_preset


def set_level_SMF(SMF_lvl):
    SMF100A.write(f":POW {SMF_lvl} dBuV")
    SMF100A.write("OUTP ON")


def wait(milliseconds):  # czas pauzy w milisekundach
    return time.sleep(milliseconds / 1000)


def frequency_band_SMF(frequency_file):
    for x in range(0, len(frequency_file), 1):
        frequency_file[x] = frequency_file[x].replace(",", ".")
    # print(frequency_file)
    frequency_file = [float(x) for x in frequency_file]
    return frequency_file


def set_single_frequency_SMF(single_frequency):
    single_frequency = single_frequency  # zastąpić to 0 zmienną, która będzie czekała na odczyt z ESU
    # print(f"Na generator poszło: {single_frequency = }")
    SMF100A.write(f"FREQ {single_frequency} MHz")
    return single_frequency


# single_frequency = set_single_frequency_SMF(frequency_band_SMF)


def set_single_frequency_ESU(single_frequency):
    # print("Wprowadź częstotliwość: ")
    # frequency = input()
    single_frequency = set_single_frequency_SMF(frequency_band_SMF)
    ESU40.write(f"FREQ:CENT {single_frequency}MHz")
    return single_frequency


def measurement_ESU(single_frequency):
    for x in range(0, len(frequency_band_SMF)):
        single_frequency[x] = set_single_frequency_SMF(frequency_band_SMF)[x]
        set_single_frequency_SMF(single_frequency[x])
        set_single_frequency_ESU(single_frequency[x])
        wait(ms)
        result_ESU = []
        a = ESU40.query('SENSe:FREQuency:CENTer?')  # odczytuje z ESU częstotliwości pomiarowe [Hz]
        # b = ESU40.query("trace:data?")
        print(f"f = {a}")
        result_ESU = result_ESU.append(ESU40.write('SENSe:FREQuency:CENTer?'))
        return result_ESU


# Connect to the signal generator over LAN
rm = pyvisa.ResourceManager()
rm.list_resources()
SMF100A = rm.open_resource('TCPIP::10.0.0.3::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
print(f"Generator:\n{SMF100A.query('*IDN?')}")

# Connect to the receiver over LAN
rm = pyvisa.ResourceManager()
rm.list_resources()
ESU40 = rm.open_resource('TCPIP::10.0.0.4::INSTR')
print(f"Odbiornik:\n{ESU40.query('*IDN?')}")

file = open('../frequencies_txt', 'r')
frequency = file.read().splitlines()
frequency_band_SMF = frequency_band_SMF(frequency)
print(f"{frequency_band_SMF = }")

print("Podaj poziom generowanego sygnału [dBuV]: ")
level = float(input())

print("Czas postoju: ")
ms = int(input())

# set_single_frequency_SMF(frequency_band_SMF)
# set_single_frequency_ESU(frequency_band_SMF)
set_level_SMF(level)
measurement_ESU(frequency_band_SMF)


ESU40.write(f"FREQ:CENT {999}MHz")