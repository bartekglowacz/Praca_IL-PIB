# Connect to the receiver over LAN
import pyvisa

rm = pyvisa.ResourceManager()
rm.list_resources()
ESU40 = rm.open_resource(
    'TCPIP::10.0.0.4::INSTR')  # żeby zwiększyć czas na odczyt to dodać timeout=10000 jako drugi argument

# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
# print(f"Dane urządzenia:\n{ESU40.query('*IDN?')}")

# reset urządzenia
ESU40.write("*RST")

# wybór trybu IF
ESU40.write("INST:SEL IFAN")


# włączenie wyświetlacza podczas obsługi zdalnej
def display_on():
    ESU40.write("SYST:DISP:UPD ON")


# Automatyczny tłumik na wejściu
def set_auto_attenuator():
    ESU40.write("INP:ATT:AUTO ON")


# ustawienie couplingu AC lub DC
def select_coupling(AC_DC):  # wpisać AC lub DC
    ESU40.write(f"INP:COUP {AC_DC}")


# Wybór portu wejściowego ESU
def select_RF_input(input_number): # wpisać tylko samą cufrę
    ESU40.write(f"INP:TYPE INPUT{input_number}")


# ustawienie detektora wartości szczytowej, średniej
def set_detector(detector):
    ESU40.write(f"DET:REC {detector}")  # POS - dla szczytowej, AVER dla średniej


# ESU40.write("CALC:MARK ON")
# marker = ESU40.write("CALC:MARK:MAX")


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


def set_measurement_time():
    RBW = int(ESU40.query("BAND?"))
    # print("Ustawione RBW: [Hz]", RBW)  # zapytanie urządzenia o ustawioną wartość RBW
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
        # ESU40.write("SWE:TIME 100ms")

# ESU40.close()
