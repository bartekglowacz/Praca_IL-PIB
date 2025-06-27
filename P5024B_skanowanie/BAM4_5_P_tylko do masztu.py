import datetime
import socket
import time


# Musi być włączona aplikacja Maturo i masz w niej podłączony!!!
class Mast:
    def __init__(self, ip, port, buffer, delay):
        self.ip = ip
        self.port = port
        self.buffer = buffer
        self.delay = delay
        self.sock = None

    def write(self, cmd):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        self.sock.send(cmd.encode())
        # print(datetime.datetime.now().time(), "Sent: ", cmd)
        time.sleep(self.delay)
        self.sock.close()

    def query(self, cmd):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        self.sock.send(cmd.encode())
        data = self.sock.recv(self.buffer)
        value = data.decode("utf-8")
        value = value[:-1]
        # print(datetime.datetime.now().time(), "sent: ", cmd)
        # print(datetime.datetime.now().time(), "Receive: ", value)
        self.sock.close()
        return value

bam = Mast("172.16.0.76", 200, 1024, 0.1)
bam.query("*IDN?")

def defining_preset():
    bam.write("LD 0 DV") # 0 - ustawienie masztu jako urządzenia sterowanego
    bam.write("LD 35 SF") # prędkość masztu [cm/s]
    print(f"Pozycja masztu: {bam.query("RP")} cm")
    polarization = input("Jaka polaryzacja?\nH - pozioma\nV - pionowa \n").upper()
    if polarization == "H":
        bam.write("PH")
    elif polarization == "V":
        bam.write("PV")
    else:
        print("Zjebano coś")

def moving_mast():
    # bam.write(f"LD 100 CM NP GO")
    start_position = float(input("Podaj pozycję startową: "))
    end_position = float(input("Podaj pozycję końcową: "))
    step = float(input("Podaj krok: "))
    # time.sleep(3)
    print(f"Pozycja masztu: {bam.query("RP")} cm")
    while start_position <= end_position:
        bam.write(f"LD {start_position} CM NP GO")
        start_position += step

        while True:

            bu = bam.query("BU")
            if bu == "1":
                break
        while True:
            bu = bam.query("BU")
            bam.query("RP")
            if bu == "0":
                break
        print(f"Pozycja masztu: {bam.query("RP")} cm")

if __name__ == "__main__":
    defining_preset()
    moving_mast()


