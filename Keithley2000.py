import pyvisa

# tworzenie zasobu VISA do połączenia z urządzeniem Keithley 2000
rm = pyvisa.ResourceManager()
keithley = rm.open_resource('GPIB0::16::INSTR')

# wysłanie zapytania o błędy
keithley.write('*IDN?')

# odczytanie odpowiedzi
response = keithley.read()
print(response)
