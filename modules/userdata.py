import json
import os

USER_DATA_FILE = "user_data.json"

def save_user_data(username, avatar_filename):
    data = {"username": username, "avatar": avatar_filename}
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return None

    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Проверяем только имя
        if "username" in data:
            avatar_path = data.get("avatar", None)
            if avatar_path and not os.path.exists(avatar_path):
                avatar_path = None
            data["avatar"] = avatar_path
            return data
        else:
            return None
    except Exception:
        return None
