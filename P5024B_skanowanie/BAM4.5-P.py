import socket
import time

class Mast:
    def __init__(self, ip, port, timeout=2):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.ip, self.port))

    def send_command(self, command):
        # Wysyła komendę z bajtem 0x00 na końcu
        self.sock.sendall(command.encode() + b'\x00')

    def receive_response(self):
        data = b''
        while True:
            try:
                chunk = self.sock.recv(1024)
                data += chunk
                if not chunk or chunk.endswith(b'\x00'):
                    break
            except socket.timeout:
                break
        return data.rstrip(b'\x00').decode(errors='ignore')

    def query(self, command):
        self.send_command(command)
        time.sleep(0.1)  # mała pauza dla urządzenia
        return self.receive_response()

    def idn(self):
        self.send_command("*RST")
        print("Dane podłączonego urządzenia:", self.query("*IDN?"))

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

bam = Mast("172.16.0.76", 200)
bam.connect()
bam.idn()
bam.close()
#