import pyvisa

# connect to the signal generator over lan
rm = pyvisa.ResourceManager()
rm.list_resources()
SMF100A = rm.open_resource('TCPIP::169.254.2.20::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
# print(f"Generator:\n{SMF100A.query('*IDN?')}")

# wyłączenie automatycznego tłumika
SMF100A.write("OUTP:AMOD FIX")

# ustawienie wartości tłumika
SMF100A.write("SOUR:POW:ATT 0dB")

# wyłączenie generatora
SMF100A.write("OUTP OFF")