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

    def set_Frequency(self):
        self.name.write("FREQ:CENT 666MHz")


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
        self.name.write(f"FREQ {f}")
        return f


receiver = Receiver("TCPIP::169.254.10.77::inst0::INSTR", "ESW26")
receiver.connect()
receiver.IDN()
receiver.set_Frequency()

signalGenerator = HMF2550("ASRL5::INSTR", "HMF2550")
signalGenerator.connect()
signalGenerator.IDN()
signalGenerator.HighImpedance_or_Xohm()
signalGenerator.set_level()
signalGenerator.set_single_frequency("100")
