import customtkinter as tk
from PIL import Image
import os
import json

if os.path.exists('data.json') and os.path.getsize('data.json') > 0:
    with open("data.json", "r") as f:
        userdata = json.load(f)


root = tk.CTk()
root.title("Simple Game")
root.geometry("500x500")


user = ""
userhp = 0
userpower = 0

quest_frame = tk.CTkFrame(root)
quest_frame.pack(pady=10)

button_frame = tk.CTkFrame(root)
button_frame.pack(pady=10)

answer_frame = tk.CTkFrame(root)
answer_frame.pack(pady=10)

logoimg = Image.open("assets/upscaled_logo.png")
logoi = tk.CTkImage(light_image=logoimg, size=(360, 142))

grl = tk.CTkLabel(quest_frame, image=logoi, text="")
grl.pack(pady=10)
greet = tk.CTkLabel(quest_frame, text="Привет, укажи свое имя", font=("Arial", 14))

name = tk.CTkEntry(answer_frame, placeholder_text="Введите имя...", width=200)

userhpbar = tk.CTkEntry(answer_frame, placeholder_text="Введите хп...", width=100)
userpwbar = tk.CTkEntry(answer_frame, placeholder_text="Введите хитбоксы кнопки...", width=100)

def runfight():
    global userhp, userpower
    if userhpbar.get().strip().isdigit() and userpwbar.get().strip().isdigit():
        userhp = int(userhpbar.get().strip())
        userpower = int(userpwbar.get().strip())
        if 1 <= userhp <= 150 and 2 <= userpower <= 8:
            root.destroy()
            with open("data.json", "w") as f:
                json.dump({"user": user, "userhp": userhp, "userpower": userpower}, f)
            os.system("python fight.py")


def prefight():
    greet.configure(
        text=f"Итак, {user}, пора приготовиться к бою с врагом.\nКурсор мыши - твой враг\nВыбери хп от 1 до 150, а Hitbox Multiplier от 2 до 8.",
        text_color="white")
    userhpbar.pack(side="left")
    userpwbar.pack(side="right")
    if os.path.exists('data.json') and os.path.getsize('data.json') > 0:
        userhpbar.insert(0, userdata["userhp"])
        userpwbar.insert(0, userdata["userpower"])
        greet.configure(text=f"Итак, {user}, пора приготовиться к бою с врагом.\nКурсор мыши - твой враг\nВыбери хп 2 до 150, а Hitbox Multiplier от 2 до 8.\nТвои прошлые значения были восстановлены",)

    ok.configure(text="Готово", command=runfight)


def submit_name():
    global user
    user = name.get().strip()
    if not user:
        return
    greet.configure(text=f"Привет, {user}!", text_color="green")
    name.pack_forget()
    ok.configure(text="Далее", command=prefight)


ok = tk.CTkButton(button_frame, text="Готово", command=submit_name)


def nextt():
    global ok
    global button_frame
    button_frame.forget()
    button_frame = tk.CTkFrame(root)
    button_frame.pack(pady=10)
    grl.forget()
    greet.pack()
    name.pack()
    if os.path.exists('data.json') and os.path.getsize('data.json') > 0:
        name.insert(0, userdata["user"])
    ok = tk.CTkButton(button_frame, text="Готово", command=submit_name)
    ok.pack()


start = tk.CTkButton(button_frame, text="Начать", command=nextt)
start.pack(pady=5)

root.mainloop()
#