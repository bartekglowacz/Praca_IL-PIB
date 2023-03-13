import pyvisa


class Device:
    def __init__(self, name, ip_address):
        self.connected_device = None
        self.name = name
        self.ip_address = ip_address

    def connect(self):
        # Connect to the device over LAN
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.connected_device = rm.open_resource(f'TCPIP::{self.ip_address}::INSTR')

    def IDN(self):
        print(f"Dane podłączonego urządzenia:\nNazwa: {self.name}\nIDN: {self.connected_device.query('*IDN?')}")


class RohdeSchwarzGenerator(Device):
    def __init__(self, frequency_band, name, ip_address):
        super().__init__(name, ip_address)
        self.frequency_band = frequency_band


# tworzenie klasy ESU 40
ESU40 = Device("ESU40", "10.0.0.4")
ESU40.connect()
ESU40.IDN()

# tworzenie klasy SMF 100A
SMF100A = Device("SMF100A", "10.0.0.3")
SMF100A.connect()
SMF100A.IDN()
