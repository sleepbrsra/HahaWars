from modules.utils import load_user_data
from gui import start_hub
from registration import start_registration
from network import setup_network

def main():
    user_data = load_user_data()
    if not user_data:
        user_data = start_registration()

    network = setup_network(user_data)
    start_hub(user_data, network)

if __name__ == "__main__":
    main()
