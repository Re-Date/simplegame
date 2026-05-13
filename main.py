import customtkinter as tk
from PIL import Image
import os
import json

if os.path.exists('data/data.json') and os.path.getsize('data/data.json') > 0:
    with open("data/data.json", "r") as f:
        userdata = json.load(f)

root = tk.CTk()
root.title("Simple Game")
root.geometry("500x500")

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


class Actions:
    def __init__(self):
        self.user = ""
        self.userhp = 0
        self.userpower = 0
        self.button_frame = button_frame
        self.ok = None

    def runfight(self):
        if userhpbar.get().strip().isdigit() and userpwbar.get().strip().isdigit():
            self.userhp = int(userhpbar.get().strip())
            self.userpower = int(userpwbar.get().strip())
            if 1 <= self.userhp <= 150 and 2 <= self.userpower <= 8:
                root.destroy()
                with open("data/data.json", "w") as f:
                    json.dump({"user": self.user, "userhp": self.userhp, "userpower": self.userpower}, f)
                os.system("python fight.py")

    def prefight(self):
        greet.configure(
            text=f"Итак, {self.user}, пора приготовиться к бою с врагом.\nКурсор мыши - твой враг\nВыбери хп от 1 до 150, а Hitbox Multiplier от 2 до 8.",
            text_color="white")
        userhpbar.pack(side="left")
        userpwbar.pack(side="right")
        if os.path.exists('data/data.json') and os.path.getsize('data/data.json') > 0:
            userhpbar.insert(0, userdata["userhp"])
            userpwbar.insert(0, userdata["userpower"])
            greet.configure(
                text=f"Итак, {self.user}, пора приготовиться к бою с врагом.\nКурсор мыши - твой враг\nВыбери хп 2 до 150, а Hitbox Multiplier от 2 до 8.\nТвои прошлые значения были восстановлены", )
        self.ok.configure(text="Готово", command=self.runfight)

    def submit_name(self):
        self.user = name.get().strip()
        if not self.user:
            return
        greet.configure(text=f"Привет, {self.user}!", text_color="green")
        name.pack_forget()
        self.ok.configure(text="Далее", command=self.prefight)

    def nextt(self):
        self.button_frame.forget()
        self.button_frame = tk.CTkFrame(root)
        self.button_frame.pack(pady=10)
        grl.forget()
        greet.pack()
        name.pack()
        if os.path.exists('data/data.json') and os.path.getsize('data/data.json') > 0:
            name.insert(0, userdata["user"])
        self.ok = tk.CTkButton(self.button_frame, text="Готово", command=self.submit_name)
        self.ok.pack()


ac = Actions()

ac.ok = tk.CTkButton(button_frame, text="Готово", command=ac.submit_name)

start = tk.CTkButton(button_frame, text="Начать", command=ac.nextt)
start.pack(pady=5)

root.mainloop()
