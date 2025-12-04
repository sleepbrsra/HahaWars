import socket, threading, json, struct

class RoomServer:
    def __init__(self, host="0.0.0.0", port=5050, room_name="Комната"):
        self.host = host
        self.port = port
        self.room_name = room_name
        self.clients = []
        self.players = []  # список словарей {"name":..., "avatar":...}
        self.running = True

    # --- TCP helper функции ---
    def send_json(self, conn, data):
        raw = json.dumps(data).encode("utf-8")
        conn.sendall(struct.pack(">I", len(raw)) + raw)

    def recv_json(self, conn):
        try:
            raw_len = conn.recv(4)
            if not raw_len:
                return None
            msg_len = struct.unpack(">I", raw_len)[0]
            data = b""
            while len(data) < msg_len:
                chunk = conn.recv(msg_len - len(data))
                if not chunk:
                    return None
                data += chunk
            return json.loads(data.decode("utf-8"))
        except:
            return None

    def start(self):
        print(f"[SERVER] Старт комнаты на {self.host}:{self.port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        threading.Thread(target=self.accept_loop, daemon=True).start()

    def stop(self):
        self.running = False
        for c in self.clients:
            try: c.close()
            except: pass
        try: self.sock.close()
        except: pass
        self.clients.clear()
        self.players.clear()

    def accept_loop(self):
        while self.running:
            try:
                conn, addr = self.sock.accept()
                self.clients.append(conn)
                print(f"[SERVER] Подключился {addr}")
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()
            except:
                break

    def handle_client(self, conn):
        player_name = None
        while self.running:
            msg = self.recv_json(conn)
            if not msg:
                break

            if msg["type"] == "join":
                player_name = msg["name"]
                avatar_b64 = msg.get("avatar")
                print(f"[SERVER] {player_name} вошёл в комнату")
                # проверяем на повторное подключение
                self.players = [p for p in self.players if p["name"] != player_name]
                self.players.append({"name": player_name, "avatar": avatar_b64})
                self.send_state_all()

            elif msg["type"] == "leave":
                player_name = msg["name"]
                print(f"[SERVER] {player_name} вышел из комнаты")
                self.players = [p for p in self.players if p["name"] != player_name]
                self.send_state_all()
                break

            elif msg["type"] == "player_move":
                player = msg["player"]
                card = msg["card"]
                print(f"[SERVER] {player} сыграл карту: {card}")

                # Рассылаем всем клиентам
                for c in self.clients:
                    self.send_json(c, {
                        "type": "player_move",
                        "player": player,
                        "card": card
                    })





        # отключение
        if player_name:
            print(f"[SERVER] {player_name} отключился")
            self.players = [p for p in self.players if p["name"] != player_name]
            self.send_state_all()
        if conn in self.clients:
            self.clients.remove(conn)
        try:
            conn.close()
        except:
            pass


    def send_state_all(self):
        state = {
            "type": "room_state",
            "room_name": self.room_name,
            "players": self.players
        }
        for c in list(self.clients):
            try:
                self.send_json(c, state)
            except:
                pass
