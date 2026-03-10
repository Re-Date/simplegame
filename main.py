import customtkinter as tk
from PIL import Image
import os

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

logoimg = Image.open("upscaled_logo.png")
logoi = tk.CTkImage(light_image=logoimg, size=(360, 142))

grl = tk.CTkLabel(quest_frame, image=logoi, text="")
grl.pack(pady=10)
greet = tk.CTkLabel(quest_frame, text="Привет, укажи свое имя", font=("Arial", 14))

name = tk.CTkEntry(answer_frame, placeholder_text="Введите имя...", width=200)

userhpbar = tk.CTkEntry(answer_frame, placeholder_text="Введите хп...", width=100)
userpwbar = tk.CTkEntry(answer_frame, placeholder_text="Введите силу...", width=100)

def runfight():
    global userhp, userpower
    if userhpbar.get().strip().isdigit() and userpwbar.get().strip().isdigit():
        userhp = int(userhpbar.get().strip())
        userpower = int(userpwbar.get().strip())
        if 50 <= userhp <= 150 and 2 <= userpower <= 8:
            root.destroy()
            os.system("python fight.py")


def prefight():
    greet.configure(
        text=f"Итак, {user}, пора приготовиться к бою с врагом.\nКоличество ХП врага будут случайно выбраны от\n50 до 150, а силы от 2 до 8.\nСвои же значения ты должен выбрать сам.",
        text_color="white")
    userhpbar.pack(side="left")
    userpwbar.pack(side="right")
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
    ok = tk.CTkButton(button_frame, text="Готово", command=submit_name)
    ok.pack()


start = tk.CTkButton(button_frame, text="Начать", command=nextt)
start.pack(pady=5)

root.mainloop()
