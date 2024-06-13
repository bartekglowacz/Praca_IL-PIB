import time

import pyvisa


class Receiver:
    def __init__(self, address, name):
        self.address = address
        self.name = name

    def connect(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.name = rm.open_resource(self.address)
        self.name.write("*RST")
        return self.name

    def IDN(self):
        print(f"Dane podłączonego urządzenia: {self.name.query('*IDN?')}")

    def set_Frequency(self, frequency):  # frequency in MHz
        self.name.write(f"FREQ:CENT {str(frequency)}MHz")

    def input_coupling(self, f):
        if f > 10:
            self.name.write("INP:COUP AC")
        else:
            self.name.write("INP:COUP DC")

    def detector(self):
        print("Jaki detektor wariacie?\n1 - peak\n2 - average\n3 - quasi peak")
        choice = int(input())
        if choice == 1:
            self.name.write("DET:REC POS")
        elif choice == 2:
            self.name.write("DET:REC AVER")
        elif choice == 3:
            self.name.write("DET:REC QPE")
        else:
            print("Nieprawidłowy wybór")

    def sweep_time(self, f):
        if f < 100 / pow(10, 6):
            sweep_time = 1
        elif 100 / pow(10, 6) <= f < 1000 / pow(10, 6):
            sweep_time = 0.1
        elif 1000 / pow(10, 6) <= f < 10000 / pow(10, 6):
            sweep_time = 0.1
        elif 10000 / pow(10, 6) <= f < 100000 / pow(10, 6):
            sweep_time = 0.05
        elif 100000 / pow(10, 6) <= f < 120000 / pow(10, 6):
            sweep_time = 0.05
        elif 120000 / pow(10, 6) <= f < 1000000000 / pow(10, 6):
            sweep_time = 0.01
        elif 1000000000 / pow(10, 6) <= f < 7000000000 / pow(10, 6):
            sweep_time = 0.01
        self.name.write(f"SWE:TIME {sweep_time}s")
        return sweep_time

    def read_RBW(self):
        rbw_value = self.name.query('BAND?')
        print(f"RBW: {rbw_value}")
        return rbw_value


class HMF2550:
    def __init__(self, address, name):
        self.address = address
        self.name = name

    def connect(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.name = rm.open_resource(self.address)
        self.name.write("*RST")
        return self.name

    def IDN(self):
        print(f"Dane podłączonego urządzenia: {self.name.query('*IDN?')}")

    def power_on_off(self, mode):  # ON or OFF
        self.name.write(f"OUTP {mode.upper()}")

    def HighImpedance_or_Xohm(self):
        print("Podaj impedancję generatora\nDla trybu High Impedance wpisz ""H""")
        impedanceValue = input().upper()
        if impedanceValue == "H":
            self.name.write(f"OUTPut:LOAD INF")
        elif impedanceValue.isnumeric():
            self.name.write(f"OUTPut:LOAD {impedanceValue}")
        else:
            print("Nieprawidłowy wybór")
            exit()

    def set_level(self):
        print("Opcje:\n1 - V\n2 - dBm")
        choice = int(input())
        if choice == 1:
            self.name.write("VOLT:UNIT VOLT")
            print("Podaj poziom generatora")
            genLevel = float(input())
            self.name.write(f":VOLT {genLevel}")
            print(f"Poziom generatora: {genLevel} V")
        elif choice == 2:
            self.name.write("VOLT:UNIT DBM")
            print("Podaj poziom generatora")
            genLevel = float(input())
            self.name.write(f":VOLT {genLevel}")
            print(f"Poziom generatora: {genLevel} dBm")
        else:
            print("Nieprawidłowy wybór")

    def set_single_frequency(self, f):  # w Hz!
        self.name.write(f"FREQ {f * pow(10, 6)}")
        return f


def frequency_table(txt_file):
    print("1 - częstotliwości podane w Hz\n2 - częstotlwiości podane w MHz")
    choice = int(input())
    if choice == 1:
        txt_file = open(txt_file, "r")
        txt_file = [float(f.replace(",", ".")) / pow(10, 6) for f in txt_file]  # displayed in MHz
    elif choice == 2:
        txt_file = open(txt_file, "r")
        txt_file = [float(f.replace(",", ".")) for f in txt_file]  # displayed in MHz
    # print(txt_file)
    return txt_file


receiver = Receiver("TCPIP::169.254.10.77::inst0::INSTR", "ESR7")
receiver.connect()
receiver.IDN()
receiver.detector()
# receiver.set_Frequency(999)

#
signalGenerator = HMF2550("ASRL5::INSTR", "HMF2550")
signalGenerator.connect()
signalGenerator.IDN()
signalGenerator.HighImpedance_or_Xohm()
signalGenerator.set_level()
# signalGenerator.set_single_frequency("1000")
signalGenerator.power_on_off("ON")
# frequency_sweep("frequencies_txt")

for f in frequency_table("frequencies_txt"):
    print(f"f = {f}")
    signalGenerator.set_single_frequency(f)
    time.sleep(1)
    receiver.sweep_time(float(f))
    receiver.input_coupling(f)
    receiver.set_Frequency(f)
    receiver.read_RBW()
    time.sleep(1)
signalGenerator.power_on_off("OFF")
