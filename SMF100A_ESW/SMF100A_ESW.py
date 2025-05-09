import datetime
import time
import pyvisa


class SMF100A:
    def __init__(self, address, name):
        self.address = address
        self.name = name

    def connect(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.name = rm.open_resource(self.address)
        # self.name.timeout = 10000
        self.name.write("*RST")
        self.name.write("OUTP:AMOD AUTO")
        return self.name

    def idn(self):
        print(f"Dane podłączonego urządzenia: {self.name.query('*IDN?')}")

    def power_on_off(self, mode):
        self.name.write(f"OUTP {mode}")

    def select_unit(self, unit):
        self.name.write(f"UNIT:POW {unit}")
        return str(unit)

    def which_unit(self):
        return self.name.query("UNIT:POW?")

    def set_level(self, level):
        self.name.write(f":POW {level}")

    def set_frequency(self, f):
        self.name.write(f"FREQ {f} MHz")
        return f


class ESW:
    def __init__(self, address, name):
        self.address = address
        self.name = name

    def connect(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.name = rm.open_resource(self.address)
        # self.name.timeout = 10000
        self.name.write("*RST")
        return self.name

    def idn(self):
        print(f"Dane podłączonego urządzenia: {self.name.query('*IDN?')}")

    def set_Frequency(self, frequency):  # frequency in MHz
        self.name.write(f"FREQ:CENT {str(frequency)}MHz")

    def input_coupling(self, f):
        if f > 10:
            self.name.write("INP:COUP AC")
        else:
            self.name.write("INP:COUP DC")

    def detector(self):
        print("Jaki detektor wariacie?\n1 - peak\n2 - average\n3 - quasi peak (dostępny od 100 Hz)")
        choice = int(input())
        if choice == 1:
            self.name.write("DET:REC POS")
        elif choice == 2:
            self.name.write("DET:REC AVER")
        elif choice == 3:
            self.name.write("DET:REC QPE")
        else:
            print("Nieprawidłowy wybór")

    def auto_attenuator(self):
        self.name.write("INP:ATT:AUTO ON")

    def sweep_time(self, f):
        if f < 100 / pow(10, 6):
            sweep_time = 1
        elif 100 / pow(10, 6) <= f < 1000 / pow(10, 6):
            sweep_time = 0.1
        elif 1000 / pow(10, 6) <= f < 10000 / pow(10, 6):
            sweep_time = 0.1
        elif 10000 / pow(10, 6) <= f < 100000 / pow(10, 6):
            sweep_time = 0.05
        elif 100000 / pow(10, 6) <= f < 120000 / pow(10, 6):
            sweep_time = 0.05
        elif 120000 / pow(10, 6) <= f < 1000000000 / pow(10, 6):
            sweep_time = 0.01
        elif 1000000000 / pow(10, 6) <= f < 7000000000 / pow(10, 6):
            sweep_time = 0.01
        self.name.write(f"SWE:TIME {sweep_time}s")
        return sweep_time

    def read_RBW(self):
        rbw_value = self.name.query('BAND?')
        print(f"RBW: {rbw_value}")
        return rbw_value

    def read_level(self, f):
        self.name.write(":DISP:BARG:PHOL:RES")
        if str(self.name.query("DET:REC?")).strip() == "QPE":
            print(f"Wykryto detektor {self.name.query('DET:REC?')}, jestem w pętli quasi-peak")
            multiplier = 2
            if f < 0.0001:
                time.sleep(3 * multiplier)
                level_tmp = self.name.query("trac? single")
            elif 0.0001 <= f < 0.001:
                time.sleep(2 * multiplier)
                level_tmp = self.name.query("trac? single")
            elif f >= 0.001:
                time.sleep(1 * multiplier)
                level_tmp = self.name.query("trac? single")
            return level_tmp
        elif str(self.name.query("DET:REC?")).strip() == "AVER":
            print(f"Wykryto detektor {self.name.query('DET:REC?')}, jestem w pętli aver")
            multiplier = 1
            if f < 0.0001:
                time.sleep(6 * multiplier)
                level_tmp = self.name.query("trac? single")
            elif 0.0001 <= f < 0.001:
                time.sleep(1.5 * multiplier)
                level_tmp = self.name.query("trac? single")
            elif f >= 0.001:
                time.sleep(0.5 * multiplier)
                level_tmp = self.name.query("trac? single")
            return level_tmp
        else:
            print(f"Wykryto detektor {self.name.query('DET:REC?')}, jestem w pętli peak")
            if f < 0.0001:
                time.sleep(10)
                level_tmp = self.name.query("trac? single")
            elif 0.0001 <= f < 0.001:
                time.sleep(2)
                level_tmp = self.name.query("trac? single")
            elif f >= 0.001:
                time.sleep(0.5)
                level_tmp = self.name.query("trac? single")
            return level_tmp


ESW = ESW("TCPIP::169.254.10.77::inst0::INSTR", "ESW")
ESW.connect()
ESW.idn()

SMF100A = SMF100A("TCPIP::169.254.10.80::inst0::INSTR", "SMF100A")
SMF100A.connect()
SMF100A.idn()

print("Wybierz jednostkę generatora\n1 - dBuV\n2 - dBm\n3 - V")
choice = int(input())
if choice == 1:
    SMF100A.select_unit("dBuV")
elif choice == 2:
    SMF100A.select_unit("dBm")
elif choice == 3:
    SMF100A.select_unit("V")
else:
    print("Niepoprawny wybór")


print("Podaj poziom generatora:")
choice = float(str(input()).replace(",", "."))
SMF100A.set_level(choice)


def frequency_table(txt_file):
    txt_file = open(txt_file, "r")
    txt_file = [float(f.replace(",", ".")) for f in txt_file]  # displayed in MHz
    return txt_file


# print("Podaj częstotliwość:")
# choice = float(str(input()).replace(",", "."))
# SMF100A.set_frequency(choice)

results = []
# Zrobić przypadki dla poziomu w dBm i V, bo zapisuje tylko dBuV!
for f in frequency_table("frequencies_txt"):
    SMF100A.power_on_off("ON")
    freq = SMF100A.set_frequency(f)
    print(f"Częstotliwość generatora: {freq} MHz")
    ESW.sweep_time(float(f))
    ESW.input_coupling(f)
    ESW.set_Frequency(f)
    level = '{:.6f}'.format(float(ESW.read_level(f)))
    print(f"Poziom na odbiorniku: {level} dBμV")
    results.append(str(freq) + ";" + str(level) + "\n")
SMF100A.power_on_off("OFF")


def result_file_name(name, result_list):
    now = datetime.datetime.now()
    year = str(now.year)
    month = "%02d" % now.month
    day = "%02d" % now.day
    hour = "%02d" % now.hour
    minute = "%02d" % now.minute
    second = "%02d" % now.second
    prefix_name = year + month + day + "_" + hour + minute + second + "_"
    full_name_of_file = prefix_name + name + ".csv"
    result_txt = open(f"C:\\Users\\bglowacz\\PycharmProjects\\Praca IL-PIB\\pliki wynikowe txt\\{full_name_of_file}",
                      "w")
    result_txt.write(f"f [MHz];U [{SMF100A.which_unit()}]\n")
    for x in result_list:
        result_txt.write(x.replace(".", ","))
    result_txt.close()

print("Nazwa pliku:")
file_name = input()
result_file_name(file_name, results)
