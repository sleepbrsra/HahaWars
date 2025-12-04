import json
import os
from PIL import Image

DATA_DIR = "data"
CARDS_DIR = os.path.join(DATA_DIR, "cards")
SITUATIONS_FILE = os.path.join(DATA_DIR, "situations.json")

def load_situations():
    with open(SITUATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_cards():
    cards = []
    for file in os.listdir(CARDS_DIR):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            cards.append(os.path.join(CARDS_DIR, file))
    return cards
