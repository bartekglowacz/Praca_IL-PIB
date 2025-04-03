import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import datetime
import time
import pyvisa


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


def main():
    def start_measurement():
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        unit = unit_var.get()
        try:
            frequencies = frequency_table(file_path, unit)
        except Exception as e:
            messagebox.showerror("Błąd", str(e))
            return

        detector_choice = detector_var.get()
        impedance_value = impedance_entry.get()
        unit_choice = unit_entry_var.get()
        gen_level = float(level_entry.get())

        receiver = Receiver("TCPIP::172.29.10.158::inst0::INSTR")
        receiver.connect()
        receiver.IDN()
        receiver.detector(detector_choice)
        receiver.auto_attenuator()

        signal_generator = HMF2550("ASRL5::INSTR")
        signal_generator.connect()
        signal_generator.IDN()
        signal_generator.HighImpedance_or_Xohm(impedance_value)
        signal_generator.set_level(unit_choice, gen_level)
        signal_generator.power_on_off("ON")

        results = []
        for f in frequencies:
            freq = signal_generator.set_single_frequency(f)
            print(f"Częstotliwość generatora: {freq} MHz")
            receiver.sweep_time(f)
            receiver.input_coupling(f)
            receiver.set_Frequency(f)
            level = '{:.6f}'.format(float(receiver.read_level(f)))
            print(f"Poziom na odbiorniku: {level} dBμV")
            results.append(f"{freq};{level}")

        signal_generator.power_on_off("OFF")

        results_text.delete("1.0", tk.END)
        results_text.insert(tk.END, "\n".join(results))

    def save_results():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            result_file_name(file_path, results_text.get("1.0", tk.END).splitlines())
            messagebox.showinfo("Sukces", "Wyniki zostały zapisane")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    root = tk.Tk()
    root.title("HMF2550 & ESR7 Measurement")

    # Detector Selection
    detector_label = tk.Label(root, text="Wybierz detektor:")
    detector_label.pack()
    detector_var = tk.StringVar(value="peak")
    tk.Radiobutton(root, text="Peak", variable=detector_var, value="peak").pack()
    tk.Radiobutton(root, text="Average", variable=detector_var, value="average").pack()
    tk.Radiobutton(root, text="Quasi-peak", variable=detector_var, value="quasi-peak").pack()

    # Impedance Entry
    impedance_label = tk.Label(root, text="Podaj impedancję (H dla High Impedance):")
    impedance_label.pack()
    impedance_entry = tk.Entry(root)
    impedance_entry.pack()

    # Generator Level Unit
    unit_entry_label = tk.Label(root, text="Wybierz jednostkę poziomu generatora:")
    unit_entry_label.pack()
    unit_entry_var = tk.StringVar(value="V")
    tk.Radiobutton(root, text="V", variable=unit_entry_var, value="V").pack()
    tk.Radiobutton(root, text="dBm", variable=unit_entry_var, value="dBm").pack()

    # Generator Level Entry
    level_label = tk.Label(root, text="Podaj poziom generatora:")
    level_label.pack()
    level_entry = tk.Entry(root)
    level_entry.pack()

    # Frequency Unit Selection
    unit_label = tk.Label(root, text="Wybierz jednostkę częstotliwości:")
    unit_label.pack()
    unit_var = tk.StringVar(value="Hz")
    tk.Radiobutton(root, text="Hz", variable=unit_var, value="Hz").pack()
    tk.Radiobutton(root, text="MHz", variable=unit_var, value="MHz").pack()

    # Start Button
    start_button = tk.Button(root, text="Rozpocznij pomiar", command=start_measurement)
    start_button.pack()

    # Results Text
    results_text = ScrolledText(root, height=10, width=50)
    results_text.pack()

    # Save Button
    save_button = tk.Button(root, text="Zapisz wyniki", command=save_results)
    save_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
