import pyvisa

# connect to the signal generator over lan
rm = pyvisa.ResourceManager()
rm.list_resources()
SMF100A = rm.open_resource('TCPIP::10.0.0.3::INSTR')


# SMF100A.write("*RST") # ustawia wartości domyśne generatora i WYŁĄCZA poziom
# print(f"Generator:\n{SMF100A.query('*IDN?')}")

# wyłączenie automatycznego tłumika
def set_auto_attenuator():
    SMF100A.write("OUTP:AMOD FIX")


# ustawienie wartości tłumika
def set_attenuator(value):
    SMF100A.write(f"SOUR:POW:ATT {value}dB")


# wyłączenie generatora
def output_on_off(mode):
    SMF100A.write(f"OUTP {mode}")


# ustawia jednostkę domyślną urządzenia
def select_unit(unit):
    SMF100A.write(f"UNIT:POW {unit}")


def set_level(level):
    SMF100A.write(f":POW {level} dBuV")
    # SMF100A.write("OUTP ON")


# SMF100A.close()

SMF100A.write(f":POW {50} dBuV")
# SMF100A.write("OUTP ON")
# print(SMF100A.query("POW?"))
set_auto_attenuator()
set_attenuator(10)
