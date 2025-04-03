import pyvisa


class VNA:
    def __init__(self, address, name):
        self.address = address
        self.name = name

    def connect(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.name = rm.open_resource(self.address)
        # self.name.timeout = 1000
        self.name.write("*RST")
        return self.name

    def idn(self):
        print(f"Dane podłączonego urządzenia: {self.name.query('*IDN?')}")

    def set_Sparameters(self):  # ustawianie mierzonego parametru S
        # wybór portów: S12, S43 itp.
        print("Jakie parametry przejściowe S chcesz zmierzyć?\nWpisz w formacie: 11, 21, 43 itp.")
        choice = input()
        self.name.write(f"calc:meas:par s{choice}")

    def set_format(self):  # format log-mag
        self.name.write("calc:meas:form mlog")

    def frequency_range(self):  # ustawienie zakresu częstotliwości
        print("1 - stały krok częstotliwości\n2 - tablica częstotliwości")
        choice = int(input())
        if choice == 1:
            self.name.write("sens:swe:type lin")

            print("Po cyfrze dodaje przedrostek: k - KHz, M - MHz, G - GHz")
            print("Podaj początek zakresu:")
            f_start = input()
            if f_start.endswith("k"):
                f_start = float(f_start.rstrip("k").replace(",", ".")) * 1000
            elif f_start.endswith("M"):
                f_start = float(f_start.rstrip("M").replace(",", ".")) * 1000000
            elif f_start.endswith("G"):
                f_start = float(f_start.rstrip("G").replace(",", ".")) * 1000000000
            else:
                print("Zjebałeś")
            print(f"start = {f_start / 1000000} MHz")
            self.name.write(f"sens:freq:star {f_start}")

            print("Podaj koniec zakresu:")
            f_end = input()
            if f_end.endswith("k"):
                f_end = float(f_end.rstrip("k").replace(",", ".")) * 1000
            elif f_end.endswith("M"):
                f_end = float(f_end.rstrip("M").replace(",", ".")) * 1000000
            elif f_end.endswith("G"):
                f_end = float(f_end.rstrip("G").replace(",", ".")) * 1000000000
            else:
                print("Zjebałeś")
            print(f"koniec = {f_end / 1000000} MHz")
            self.name.write(f"sens:freq:stop {f_end}")

            print("Podaj krok częstotliwości:")
            f_step = input()
            if f_step.endswith("k"):
                f_step = float(f_step.rstrip("k").replace(",", ".")) * 1000
            elif f_step.endswith("M"):
                f_step = float(f_step.rstrip("M").replace(",", ".")) * 1000000
            elif f_step.endswith("G"):
                f_step = float(f_step.rstrip("G").replace(",", ".")) * 1000000000
            else:
                f_step = float(f_step)
            print(f"krok = {f_step / 1000000} MHz")
            self.name.write(f"sens:swe:step {f_step}")

            print("Podaj szerokość filtra BW:")
            f_BW = input()
            if f_BW.endswith("k"):
                f_BW = float(f_BW.rstrip("k").replace(",", ".")) * 1000
            elif f_BW.endswith("M"):
                f_BW = float(f_BW.rstrip("M").replace(",", ".")) * 1000000
            elif f_BW.endswith("G"):
                f_BW = float(f_BW.rstrip("G").replace(",", ".")) * 1000000000
            else:
                f_BW = float(f_BW)
            print(f"BW = {f_BW / 1000000} MHz")
            self.name.write(f"sens:bwid:res {f_BW}")

            print("Podaj moc portu generującego:")
            power = input()
            self.name.write(f"sour:pow:lev:imm:ampl {power}")

        elif choice == 2:
            self.name.write("sens:swe:type seg")
        else:
            print("Gówno")

    def get_trace(self):  # dodanie nowego trace'a
        self.name.write("calc:meas:math:new 0,act")

class Mast:
    def set_hight_step(self):
        print("Jaki krok zmiany wysokości [cm]?")
        step = input()
        for h in range(1, 4, step):
            print(f"Jestem na wysokości {h+step}")

# VNA = VNA("TCPIP::169.254.140.230::5025::SOCKET", "P5024B")
VNA = VNA("TCPIP::169.254.140.230::hislip1::INSTR", "P5024B")
VNA.connect()
VNA.idn()
VNA.set_Sparameters()
VNA.set_format()
VNA.frequency_range()
for i in range(0, 18):
    VNA.get_trace()
