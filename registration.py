from tkinter import Tk, simpledialog, filedialog, messagebox
from modules.utils import save_user_data, copy_avatar_to_folder

def start_registration():
    root = Tk()
    root.withdraw()

    # Ввод имени
    name = simpledialog.askstring("Регистрация", "Введите имя игрока:")
    if not name:
        name = "Игрок1"

    # Выбор аватарки
    avatar_path = filedialog.askopenfilename(title="Выберите аватарку", filetypes=[("Images", "*.png *.jpg *.jpeg")])
    if avatar_path:
        avatar_path = copy_avatar_to_folder(avatar_path)
    else:
        avatar_path = "Отсутствует"

    user_data = {"name": name, "avatar": avatar_path}
    save_user_data(user_data)

    root.destroy()
    return user_data
