import pyvisa


# keithley = rm.open_resource('GPIB0::16::INSTR')

class Device:
    def __init__(self, address, name, connected_device_name=None):
        self.connected_device_name = connected_device_name
        self.address = address
        self.name = name

    def connect(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.connected_device_name = rm.open_resource(self.address)
        return self.connected_device_name

    def IDN(self):
        print(f"Dane podłączonego urządzenia:\nNazwa: {self.name}\nIDN: {self.connected_device_name.query('*IDN?')}")


class Voltmeter(Device):
    def __init__(self, address, name):
        super().__init__(address, name)

    def AC_or_DC(self):
        print("Wybierz tryb AC lub DC wpisując opowiednio te skróty")
        choice = input().upper()
        if choice == "AC":
            self.connected_device_name.write('FUNC "VOLT:AC"')
            self.connected_device_name.write("UNIT:VOLT:AC dBm")
        elif choice == "DC":
            self.connected_device_name.write('FUNC "VOLT:DC"')
            self.connected_device_name.write("UNIT:VOLT:DC dBm")
        else:
            print("Dokonano złego wyboru")

    def read_level(self):
        self.connected_device_name.write("INIT:CONT OFF")
        level = float(self.connected_device_name.query("read?"))
        return level


class SignalGenerator(Device):
    def __init__(self, address, name):
        super().__init__(address, name)

    def set_frequency_band(self):
        file = open("frequencies_txt", "r")
        frequencies = file.readlines()
        frequencies = [float(freq.replace(",", ".")) for freq in frequencies]
        print(frequencies)
        return frequencies

    def set_level(self, level):
        self.connected_device_name.write("VOLT:UNIT DBM")
        self.connected_device_name.write(f":VOLT {level}")

    def power_on_off(self, mode):
        self.connected_device_name.write(f"OUTP {mode}")

    def set_single_frequency(self):
        self.connected_device_name.write("FREQ 100")


# keithley2000 = Voltmeter('GPIB0::16::INSTR', "Keithley")
# keithley2000.connect()
# keithley2000.AC_or_DC()
# keithley2000.IDN()
# keithley2000.read_level()

HMF2550 = SignalGenerator("ASRL10::INSTR", "HMF2550")
HMF2550.connect()
HMF2550.IDN()
HMF2550.set_frequency_band()
HMF2550.power_on_off("ON")
HMF2550.set_level(10)
HMF2550.set_single_frequency()
