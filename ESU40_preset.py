# Connect to the receiver over LAN
import pyvisa

rm = pyvisa.ResourceManager()
rm.list_resources()
ESU40 = rm.open_resource('TCPIP::169.254.2.22::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
# print(f"Dane urządzenia:\n{ESU40.query('*IDN?')}")

# reset urządzenia
ESU40.write("*RST")

# wybór trybu IF
ESU40.write("INST:SEL IFAN")

# włączenie wyświetlacza podczas obsługi zdalnej
ESU40.write("SYST:DISP:UPD ON")