# Connect to the receiver over LAN
import enums as enums
import pyvisa

rm = pyvisa.ResourceManager()
rm.list_resources()
ESU40 = rm.open_resource('TCPIP::10.0.0.4::INSTR') # żeby zwiększyć czas na odczyt to dodać timeout=10000 jako drugi argument

# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
# print(f"Dane urządzenia:\n{ESU40.query('*IDN?')}")

# reset urządzenia
ESU40.write("*RST")

# wybór trybu IF
ESU40.write("INST:SEL IFAN")

# włączenie wyświetlacza podczas obsługi zdalnej
ESU40.write("SYST:DISP:UPD ON")

# Automatyczny tłumik na wejściu
ESU40.write("INP:ATT:AUTO ON")

# ustawienie couplingu AC lub DC
ESU40.write("INP:COUP AC")

# Wybór portu wejściowego ESU
ESU40.write("INP:TYPE INPUT1")

# ustawienie detektora wartości szczytowej, średniej
ESU40.write("DET:REC AVER") # POS - dla szczytowej, AVER dla średniej

ESU40.write("CALC:MARK ON")
marker = ESU40.write("CALC:MARK:MAX")

ESU40.close()


# print(marker)
# ESU40.query()
