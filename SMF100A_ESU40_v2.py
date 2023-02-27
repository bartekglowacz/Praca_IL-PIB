import time
import pyvisa
import SMF100A_preset
import ESU40_preset


def set_frequency():
    file = open('frequencies_txt', 'r')
    frequency = file.read().splitlines()
    # for x in range(0, len(frequency), 1):
    #     frequency[x] = frequency[x].replace(",", ".")
    frequency = [float(x.replace(",", ".")) for x in frequency]
    return frequency


def wait(pause):
    print("Podaj czas pomiaru w milisekundach")
    pause = float(input()) / 1000
    return pause


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
        self.name_connected = rm.open_resource(f'TCPIP::{self.ip_address}::INSTR')

    def IDN(self):
        print(f"Dane podłączonego urządzenia:\nNazwa: {self.name}\nIDN: {self.name_connected.query('*IDN?')}")

    def frequencies_swapping(self):
        self.frequency_band = set_frequency()
        # print(self.frequency_band)


ESU40 = Device("ESU40", "10.0.0.4", "frequencies.txt")
ESU40.connect()
ESU40.IDN()
ESU40.frequencies_swapping()

SMF100A = Device("SMF100A", "10.0.0.3", "frequencies.txt")
SMF100A.connect()
SMF100A.IDN()
SMF100A.frequencies_swapping()

frequency = set_frequency()
print(f"W main: {frequency}")
for x in frequency:
    SMF100A.name_connected.write(f"FREQ {x} MHz")
    SMF100A_freq = float(SMF100A.name_connected.query('FREQ?'))/10**6
    ESU40.name_connected.write(f"FREQ:CENT {x} MHz")
    ESU_freq = float(ESU40.name_connected.query('SENSe:FREQuency:CENTer?'))/10**6
    print(f"poszło na {SMF100A.name}: {x}")
    print(f"Odczytano z ekranu SMF: {SMF100A_freq} MHz")
    print(f"poszło na {ESU40.name}: {x}")
    print(f"Odczytano z ekranu ESU: {ESU_freq} MHz")
    time.sleep(1)
