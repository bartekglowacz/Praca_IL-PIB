import sys
import time
import pyvisa
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QFileDialog, QRadioButton, QMessageBox, QTextEdit


class Receiver:
    def __init__(self, address):
        self.address = address
        self.name = None

    def connect(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.name = rm.open_resource(self.address)
        self.name.write("*RST")
        return self.name

    def IDN(self):
        print(f"Dane podłączonego urządzenia: {self.name.query('*IDN?')}")

    def set_Frequency(self, frequency):  # frequency in MHz
        self.name.write(f"FREQ:CENT {str(frequency)}MHz")

    def input_coupling(self, f):
        if f > 10:
            self.name.write("INP:COUP AC")
        else:
            self.name.write("INP:COUP DC")

    def detector(self, choice):
        if choice == "peak":
            self.name.write("DET:REC POS")
        elif choice == "average":
            self.name.write("DET:REC AVER")
        elif choice == "quasi-peak":
            self.name.write("DET:REC QPE")
        else:
            print("Nieprawidłowy wybór detektora")

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
        det = self.name.query("DET:REC?").strip()
        if det == "QPE":
            print(f"Wykryto detektor {det}, jestem w pętli quasi-peak")
            multiplier = 2
            if f < 0.0001:
                time.sleep(3 * multiplier)
            elif 0.0001 <= f < 0.001:
                time.sleep(2 * multiplier)
            elif f >= 0.001:
                time.sleep(1 * multiplier)
        elif det == "AVER":
            print(f"Wykryto detektor {det}, jestem w pętli aver")
            multiplier = 1
            if f < 0.0001:
                time.sleep(6 * multiplier)
            elif 0.0001 <= f < 0.001:
                time.sleep(1.5 * multiplier)
            elif f >= 0.001:
                time.sleep(0.5 * multiplier)
        else:
            print(f"Wykryto detektor {det}, jestem w pętli peak")
            if f < 0.0001:
                time.sleep(6)
            elif 0.0001 <= f < 0.001:
                time.sleep(1)
            elif f >= 0.001:
                time.sleep(0.5)
        level_tmp = self.name.query("trac? single")
        return level_tmp

class HMF2550:
    def __init__(self, address):
        self.address = address
        self.name = None

    def connect(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.name = rm.open_resource(self.address)
        self.name.write("*RST")
        return self.name

    def IDN(self):
        print(f"Dane podłączonego urządzenia: {self.name.query('*IDN?')}")

    def power_on_off(self, mode):  # ON or OFF
        self.name.write(f"OUTP {mode.upper()}")

    def HighImpedance_or_Xohm(self, impedance_value):
        if impedance_value == "H":
            self.name.write(f"OUTPut:LOAD INF")
        elif impedance_value.isnumeric():
            self.name.write(f"OUTPut:LOAD {impedance_value}")
        else:
            print("Nieprawidłowy wybór")
            exit()

    def set_level(self, unit, gen_level):
        if unit == "V":
            self.name.write("VOLT:UNIT VOLT")
            self.name.write(f":VOLT {gen_level}")
            print(f"Poziom generatora: {gen_level} V")
        elif unit == "dBm":
            self.name.write("VOLT:UNIT DBM")
            self.name.write(f":VOLT {gen_level}")
            print(f"Poziom generatora: {gen_level} dBm")
        else:
            print("Nieprawidłowy wybór")

    def set_single_frequency(self, f):  # w Hz!
        self.name.write(f"FREQ {f * pow(10, 6)}")
        return f

def frequency_table(file_path, unit):
    with open(file_path, "r") as file:
        if unit == "Hz":
            frequencies = [float(line.replace(",", ".")) / pow(10, 6) for line in file]  # displayed in MHz
        elif unit == "MHz":
            frequencies = [float(line.replace(",", ".")) for line in file]  # displayed in MHz
        else:
            raise ValueError("Nieprawidłowa jednostka")
    return frequencies

def result_file_name(file_path, result_list):
    with open(file_path, "w", encoding='utf-8') as result_txt:
        result_txt.write(f"f [Hz];U [dBuV]\n")
        for x in result_list:
            result_txt.write(x.replace(".", ",") + "\n")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("HMF2550 & ESR7 Measurement")
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Detector Selection
        detector_label = QLabel("Wybierz detektor:")
        layout.addWidget(detector_label)
        self.detector_var = "peak"
        peak_radio = QRadioButton("Peak")
        peak_radio.setChecked(True)
        peak_radio.toggled.connect(lambda: self.set_detector("peak"))
        layout.addWidget(peak_radio)
        average_radio = QRadioButton("Average")
        average_radio.toggled.connect(lambda: self.set_detector("average"))
        layout.addWidget(average_radio)
        quasi_peak_radio = QRadioButton("Quasi-peak")
        quasi_peak_radio.toggled.connect(lambda: self.set_detector("quasi-peak"))
        layout.addWidget(quasi_peak_radio)

        # Impedance Entry
        impedance_layout = QHBoxLayout()
        impedance_label = QLabel("Podaj impedancję (H dla High Impedance):")
        impedance_layout.addWidget(impedance_label)
        self.impedance_entry = QLineEdit()
        impedance_layout.addWidget(self.impedance_entry)
        layout.addLayout(impedance_layout)

        # Generator Level Unit
        unit_entry_layout = QHBoxLayout()
        unit_entry_label = QLabel("Wybierz jednostkę poziomu generatora:")
        unit_entry_layout.addWidget(unit_entry_label)
        self.unit_entry_var = "V"
        v_radio = QRadioButton("V")
        v_radio.setChecked(True)
        v_radio.toggled.connect(lambda: self.set_unit("V"))
        unit_entry_layout.addWidget(v_radio)
        dbm_radio = QRadioButton("dBm")
        dbm_radio.toggled.connect(lambda: self.set_unit("dBm"))
        unit_entry_layout.addWidget(dbm_radio)
        layout.addLayout(unit_entry_layout)

        # Generator Level Entry
        level_layout = QHBoxLayout()
        level_label = QLabel("Podaj poziom generatora:")
        level_layout.addWidget(level_label)
        self.level_entry = QLineEdit()
        level_layout.addWidget(self.level_entry)
        layout.addLayout(level_layout)

        # Frequency Unit Selection
        unit_layout = QHBoxLayout()
        unit_label = QLabel("Wybierz jednostkę częstotliwości:")
        unit_layout.addWidget(unit_label)
        self.unit_var = "Hz"
        hz_radio = QRadioButton("Hz")
        hz_radio.setChecked(True)
        hz_radio.toggled.connect(lambda: self.set_frequency_unit("Hz"))
        unit_layout.addWidget(hz_radio)
        mhz_radio = QRadioButton("MHz")
        mhz_radio.toggled.connect(lambda: self.set_frequency_unit("MHz"))
        unit_layout.addWidget(mhz_radio)
        layout.addLayout(unit_layout)

        # Start Button
        start_button = QPushButton("Rozpocznij pomiar")
        start_button.clicked.connect(self.start_measurement)
        layout.addWidget(start_button)

        # Results Text
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        # Save Button
        save_button = QPushButton("Zapisz wyniki")
        save_button.clicked.connect(self.save_results)
        layout.addWidget(save_button)

    def set_detector(self, detector):
        self.detector_var = detector

    def set_unit(self, unit):
        self.unit_entry_var = unit

    def set_frequency_unit(self, unit):
        self.unit_var = unit

    def start_measurement(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik z częstotliwościami", "",
                                                   "All Files (*);;Text Files (*.txt)")
        if not file_path:
            return
        try:
            frequencies = frequency_table(file_path, self.unit_var)
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))
            return

        impedance_value = self.impedance_entry.text()
        gen_level = float(self.level_entry.text())

        receiver = Receiver("TCPIP::172.29.10.158::inst0::INSTR")
        receiver.connect()
        receiver.IDN()
        receiver.detector(self.detector_var)
        receiver.auto_attenuator()

        signal_generator = HMF2550("ASRL5::INSTR")
        signal_generator.connect()
        signal_generator.IDN()
        signal_generator.HighImpedance_or_Xohm(impedance_value)
        signal_generator.set_level(self.unit_entry_var, gen_level)
        signal_generator.power_on_off("ON")

        results = []
        for f in frequencies:
            freq = signal_generator.set_single_frequency(f)
            self.results_text.append(f"Częstotliwość generatora: {freq} MHz")
            receiver.sweep_time(f)
            receiver.input_coupling(f)
            receiver.set_Frequency(f)
            level = '{:.6f}'.format(float(receiver.read_level(f)))
            self.results_text.append(f"Poziom na odbiorniku: {level} dBμV")
            results.append(f"{freq};{level}")

        signal_generator.power_on_off("OFF")

    def save_results(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Zapisz wyniki", "", "CSV files (*.csv)")
        if not file_path:
            return
        try:
            result_file_name(file_path, self.results_text.toPlainText().splitlines())
            QMessageBox.information(self, "Sukces", "Wyniki zostały zapisane")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        mainWindow = QMainWindow()
        mainWindow.show()
        sys.exit(app.exec())

