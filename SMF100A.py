"""
Program do generatora sygnałowego SMF 100A.
Generator powinien ustawiać się na zdefiniowanych przez użytkownika częstotliwościach.
Sposób wprowadzania częstotliwości:
- z pliku TXT
Użytkownik musi mieć możliwość podania poziomu sygnały w dBuV
"""
import time
import pyvisa

print("Podaj poziom generowanego sygnału [dBuV]: ")
level = float(input())


# Funkcja podająca poziom sygnału na SMF 100A [dBuV]
def set_level(level):
    SMF100A.write(f":POW {level} dBuV")
    SMF100A.write("OUTP ON")


# Przestawianie generatora na częstotliwościach podając plik txt z częstotliwościami.
def set_frequency_from_file(frequency_list_formatted=[]):
    file = open('frequencies_txt', 'r')
    frequency = file.read().splitlines()
    print(f"Częstotliwości wysłane na generator: {frequency} MHz")
    print("Podaj czas trwania [ms]: ")
    wait = float(input())
    SMF100A.write("FREQ:MODE CW")  # ustawienie trybu fixed, czyli bez przemiatania częstotliwości

    for x in range(0, len(frequency), 1):
        frequency[x] = frequency[x].replace(",", ".")
        print("f", x + 1, "=", frequency[x].replace(",", "."))
        frequency_list_formatted.append(frequency[x])
        SMF100A.write(f"FREQ {frequency_list_formatted[x]} MHz")
        time.sleep(wait / 1000)
    file.close()
    print(f"Sformatowane częstotliwości: {frequency_list_formatted}")
    return frequency_list_formatted


def set_single_frequency():
    frequency_list = set_frequency_from_file()
    # print(f"Set single frequency list: {frequency_list}")
    return frequency_list


# Connect to the signal generator over LAN
rm = pyvisa.ResourceManager()
rm.list_resources()
SMF100A = rm.open_resource('TCPIP::169.254.2.20::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
print(f"Dane urządzenia:\n{SMF100A.query('*IDN?')}")

SMF100A.write("OUTP:AMOD FIX")  # wyłączenie automatycznego tłumika
SMF100A.write("SOUR:POW:ATT 10dB")  # ustawienie wartości tłumika
"""
# Podanie poziomu sygnału
set_level(level)

set_frequency_from_file()  # zdefiniowanie zakresu częstotliwości na podstawie pliku txt
SMF100A.write("OUTP OFF")  # wyłącza generator po zakończeniu przemiatania

set_single_frequency()

# Close the connection to the instrument
SMF100A.close()
"""