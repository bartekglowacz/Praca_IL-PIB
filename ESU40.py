"""
Program do odbiornika pomiarowego ESU40.
Program musi umożliwiać:
- ustawienie odbiornika na konkretnej częstotliwości
- wybór spanu
- automatyczne przeskalowanie okna (auto reference level)
- wybór RBW
- wybór czasu pomiaru
- wybór detektora
"""
import time
import pyvisa


# Connect to the receiver over LAN
rm = pyvisa.ResourceManager()
rm.list_resources()
('ESU40::INSTR')
ESU40 = rm.open_resource('TCPIP::169.254.2.22::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
print(f"Dane urządzenia:\n{ESU40.query('*IDN?')}")

# reset urządzenia
ESU40.write("*RST")

# wybór trybu IF
ESU40.write("INST:SEL IFAN")

# włączenie wyświetlacza podczas obsługi zdalnej
ESU40.write("SYST:DISP:UPD ON")


# deklaracja wartości częstotliwości
def set_frequency(frequency):
    # print("Wprowadź częstotliwość: ")
    # frequency = input()
    ESU40.write(f"FREQ:CENT {frequency}MHz")


# deklaracja czasu pomiaru
def wait():
    print("Podaj czas pomiaru: [ms]")
    wait = int(input())
    time.sleep(wait)


# deklaracja wartości filtra RBW [kHz]
def set_RBW():
    ESU40.write("BAND:AUTO ON")


# deklaracja wartości spanu [kHz]
def set_span():
    print("Wprowadź span [kHz] (1 kHz <= span <= 1 MHz)")
    span = input()
    ESU40.write(f"FREQ:SPAN {span} kHz")


# deklaracja Ref Level
def set_RefLevel():
    ESU40.write("INP:ATT:AUTO ON")


def set_detector():
    ESU40.write("DET:REC POS, AVER")  # detektor wartości szczytowej i średniej


def set_measurement_time():
    RBW = int(ESU40.query("BAND?"))
    print("Ustawione RBW: [Hz]", RBW)  # zapytanie urządzenia o ustawioną wartość RBW
    if RBW <= 10:
        ESU40.write("SWE:TIME 1s")
    if RBW == 100:
        ESU40.write("SWE:TIME 100ms")
    if 200 <= RBW <= 300:
        ESU40.write("SWE:TIME 50ms")
    if 1000 <= RBW <= 3000:
        ESU40.write("SWE:TIME 10ms")
    if 9000 <= RBW <= 30000:
        ESU40.write("SWE:TIME 1ms")
    if RBW >= 100000:
        ESU40.write("SWE:TIME 0.1ms")


def pause_time(counter):
    print("Ile czasu stać na zadanej częstotliwości? [ms]")
    counter = int(input())
    time.sleep(counter / 1000)

"""
set_frequency(frequency)
set_RBW()
set_span()
set_RefLevel()
set_detector()
set_measurement_time()
"""