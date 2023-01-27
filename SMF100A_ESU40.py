import pyvisa

# Connect to the signal generator over LAN
rm = pyvisa.ResourceManager()
rm.list_resources()
SMF100A = rm.open_resource('TCPIP::169.254.2.20::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
print(f"Generator:\n{SMF100A.query('*IDN?')}")

# Connect to the receiver over LAN
rm = pyvisa.ResourceManager()
rm.list_resources()
('ESU40::INSTR')
ESU40 = rm.open_resource('TCPIP::169.254.2.22::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
print(f"Odbiornik:\n{ESU40.query('*IDN?')}")