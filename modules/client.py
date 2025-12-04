import socket, threading, json, struct
import base64

class RoomClient:
    def __init__(self, name, avatar_path, server_ip, port=5050, callback=None):
        self.name = name
        self.server_ip = server_ip
        self.port = port
        self.callback = callback
        self.running = False
        self.sock = None

        # конвертация аватара в base64
        self.avatar_b64 = None
        if avatar_path:
            with open(avatar_path, "rb") as f:
                self.avatar_b64 = base64.b64encode(f.read()).decode("utf-8")

    def send_json(self, data):
        raw = json.dumps(data).encode("utf-8")
        self.sock.sendall(struct.pack(">I", len(raw)) + raw)

    def recv_json(self):
        try:
            raw_len = self.sock.recv(4)
            if not raw_len:
                return None
            msg_len = struct.unpack(">I", raw_len)[0]
            data = b""
            while len(data) < msg_len:
                chunk = self.sock.recv(msg_len - len(data))
                if not chunk:
                    return None
                data += chunk
            return json.loads(data.decode("utf-8"))
        except:
            return None

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_ip, self.port))
            self.running = True
            join_msg = {"type": "join", "name": self.name, "avatar": self.avatar_b64}
            self.send_json(join_msg)
            threading.Thread(target=self.listen_thread, daemon=True).start()
            return True
        except Exception as e:
            print("Ошибка подключения:", e)
            return False

    def listen_thread(self):
        while self.running:
            msg = self.recv_json()
            if not msg:
                break
            if self.callback:
                self.callback(msg)
        self.running = False
        try: self.sock.close()
        except: pass

    def disconnect(self):
        if self.sock:
            try:
                leave_msg = {"type": "leave", "name": self.name}
                self.send_json(leave_msg)
            except: pass
            try: self.sock.close()
            except: pass
        self.running = False
        self.sock = None
