"""
Program do generatora sygnałowego SMF 100A.
Generator powinien ustawiać się na zdefiniowanych przez użytkownika częstotliwościach.
Sposób wprowadzania częstotliwości:
- podając star, stop i step
- z pliku TXT
Użytkownik musi mieć możliwość podania poziomu sygnały w dBuV
"""
import time
import numpy as np
import pyvisa

print("Podaj poziom generowanego sygnału [dBuV]: ")
level = float(input())


# Funkcja podająca poziom sygnału na SMF 100A [dBuV]
def set_level(level):
    SMF100A.write(f":POW {level} dBuV")
    SMF100A.write("OUTP ON")


# Connect to the signal generator over LAN
rm = pyvisa.ResourceManager()
rm.list_resources()
('SMF 100A::INSTR')
SMF100A = rm.open_resource('TCPIP::169.254.2.20::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
print(f"Dane urządzenia:\n{SMF100A.query('*IDN?')}")

SMF100A.write("OUTP:AMOD FIX")  # wyłączenie automatycznego tłumika
SMF100A.write("SOUR:POW:ATT 0dB")  # ustawienie wartości tłumika

# Podanie poziomu sygnału
set_level(level)


# Przestawianie generatora na częstotliwościach
def set_frequency():
    print("Wprowadź początkową częstotliwość: ")
    start_freq = int(input())
    print("Podaj końcową częstotliwość: ")
    stop_freq = int(input())
    print("Podaj krok częstotliwości: ")
    step = int(input())
    SMF100A.write("FREQ:MODE CW")
    for frequency in range(start_freq, stop_freq + step, step):
        SMF100A.write(f"FREQ {frequency} MHz")
        time.sleep(0.5)
    # SMF100A.write("FREQ 15GHz")


def set_frequency_from_file():
    file = open('frequencies_txt', 'r')
    frequency = file.read().splitlines()
    print(f"Częstotliwości wysłane na generator: {frequency} MHz")

    for x in range(0, len(frequency), 1):
        print(f"Częstotliwość nr {x + 1}: {frequency[x]}")
        SMF100A.write(f"FREQ {frequency[x]} MHz")
        time.sleep(1)

    file.close()


# set_frequency() # zdefiniowanie zakresu częstotliwości jako start, stop, step
set_frequency_from_file() # zdefiniowanie zakresu częstotliwości na podstawie pliku txt

# Close the connection to the instrument
SMF100A.close()
