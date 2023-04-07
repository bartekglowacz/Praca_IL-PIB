import pyvisa


# keithley = rm.open_resource('GPIB0::16::INSTR')

class Device:
    def __init__(self, address, name):
        self.connected_device_name = None
        self.address = address
        self.name = name

    def connect(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.connected_device_name = rm.open_resource(self.address)

    def IDN(self):
        print(f"Dane podłączonego urządzenia:\nNazwa: {self.name}\nIDN: {self.connected_device_name.query('*IDN?')}")


class Voltmeter(Device):
    def __init__(self, address, name):
        super().__init__(address, name)

    def read_level(self):
        print("Wpisz AC - dla pomiaru napięcia przemiennego\nWpisz DC - dla pomiaru napięcia stałego")
        choice = input()
        if choice == "ac".upper():
            self.connected_device_name.write(":CONF:VOLT:AC")
            level = self.connected_device_name.query(":MEAS:VOLT:DC?")
        if choice == "dc".upper():
            self.connected_device_name.write(":CONF:VOLT:AC")
            level = self.connected_device_name.query(":MEAS:VOLT:DC?")
        else:
            print("Dokonano złego wyboru")
        level = float(self.connected_device_name.query("read?"))
        print(level)


keithley2000 = Voltmeter('GPIB0::16::INSTR', "Keithley")
keithley2000.connect()
keithley2000.IDN()
keithley2000.read_level()
