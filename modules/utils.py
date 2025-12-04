import os
import json
import shutil

AVATAR_FOLDER = "avatars"
USER_DATA_FILE = "user_data.json"

def ensure_avatar_folder():
    if not os.path.exists(AVATAR_FOLDER):
        os.makedirs(AVATAR_FOLDER)

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return None
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def copy_avatar_to_folder(source_path):
    ensure_avatar_folder()
    filename = os.path.basename(source_path)
    target_path = os.path.join(AVATAR_FOLDER, filename)
    shutil.copyfile(source_path, target_path)
    return target_path
