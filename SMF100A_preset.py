import pyvisa

# connect to the signal generator over lan
rm = pyvisa.ResourceManager()
rm.list_resources()
SMF100A = rm.open_resource('TCPIP::10.0.0.3::INSTR')
# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
# print(f"Generator:\n{SMF100A.query('*IDN?')}")

# wyłączenie automatycznego tłumika
SMF100A.write("OUTP:AMOD FIX")

# ustawienie wartości tłumika
SMF100A.write("SOUR:POW:ATT 0dB")

# wyłączenie generatora
SMF100A.write("OUTP OFF")

# ustawia jednostkę domyślną urządzenia
SMF100A.write("UNIT:POW dBuV")

SMF100A.close()

# SMF100A.write(f":POW {50} dBuV")
# SMF100A.write("OUTP ON")
# print(SMF100A.query("POW?"))