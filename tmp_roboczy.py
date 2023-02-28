import pyvisa

rm = pyvisa.ResourceManager()
SMF100A = rm.open_resource('TCPIP::10.0.0.3::INSTR')
ESU40 = rm.open_resource('TCPIP::10.0.0.4::INSTR', timeout=1000)

# ustawienie częstotliwości na generatorze SMF100A
SMF100A.write(f"FREQ:CW {50}MHz")
ESU40.write(f"FREQ:CENT {50} MHz")

# ustawienie trybu pomiarowego
ESU40.write("CALC:UNIT:POW dBUV")
ESU40.write("CALC:MARK1:FUNC:MAX")

# odczyt wartości mocy na markerze maksymalnym
ESU40.write("CALC:MARK:MAX")
value = ESU40.query_ascii_values('CALC:MARK1:Y?')[0]

print(f"Wartość mocy na markierze maksymalnym: {value} dBuV")


