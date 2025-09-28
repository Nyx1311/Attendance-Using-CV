import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
window.configure(background="#121212")  # modern dark background

dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"

# --- Modern button styles ---
button_style = {
    "bd": 0,
    "font": ("Segoe UI", 14, "bold"),
    "bg": "#2d2d2d",
    "fg": "#e0e0e0",
    "activebackground": "#00bcd4",
    "activeforeground": "white",
    "height": 2,
    "width": 20,
    "relief": FLAT
}

danger_button_style = button_style.copy()
danger_button_style["bg"] = "#d32f2f"
danger_button_style["fg"] = "white"

view_button_style = button_style.copy()
view_button_style["fg"] = "#00bcd4"


# --- Helpers ---
def del_sc1():
    sc1.destroy()


def err_screen():
    global sc1
    sc1 = tk.Toplevel(window)
    sc1.geometry("400x110")
    sc1.title("Warning!!")
    sc1.configure(background="#121212")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="#ffb300",
        bg="#121212",
        font=("Segoe UI", 14, "bold"),
    ).pack(pady=10)
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="white",
        bg="#d32f2f",
        activebackground="#b71c1c",
        width=9,
        height=1,
        font=("Segoe UI", 12, "bold"),
        relief=FLAT
    ).pack(pady=5)


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)


# --- Header with Logo ---
logo_img = load_image("UI_Image/0001.png", (70, 65))
logo_label = tk.Label(window, image=logo_img, bg="#121212")
logo_label.place(x=350, y=20)

titl = tk.Label(
    window,
    text="CLASS VISION",
    bg="#121212",
    fg="#00bcd4",  # teal accent
    font=("Segoe UI", 36, "bold"),
    pady=20
)
titl.place(x=430, y=20)

a = tk.Label(
    window,
    text="Welcome to CLASS VISION",
    bg="#121212",
    fg="#e0e0e0",
    font=("Segoe UI", 20, "bold"),
)
a.pack(pady=100)


# --- Images ---
register_img = load_image("UI_Image/register.png", (150, 150))
register_label = tk.Label(window, image=register_img, bg="#121212")
register_label.place(x=120, y=360)

attendance_img = load_image("UI_Image/attendance.png", (150, 150))
attendance_label = tk.Label(window, image=attendance_img, bg="#121212")
attendance_label.place(x=1000, y=360)

verify_img = load_image("UI_Image/verifyy.png", (150, 150))
verify_label = tk.Label(window, image=verify_img, bg="#121212")
verify_label.place(x=600, y=360)


# --- Buttons ---
r = tk.Button(window, text="Register a new student", command=lambda: TakeImageUI(), **button_style)
r.place(x=100, y=540)

r = tk.Button(window, text="Take Attendance", command=lambda: automatic_attedance(), **button_style)
r.place(x=600, y=540)

r = tk.Button(window, text="View Attendance", command=lambda: view_attendance(), **view_button_style)
r.place(x=1000, y=540)

r = tk.Button(window, text="EXIT", command=quit, **danger_button_style)
r.place(x=600, y=660)


# ---------------- Take Image UI ----------------
def TakeImageUI():
    ImageUI = tk.Toplevel(window)
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#121212")
    ImageUI.resizable(0, 0)

    titl = tk.Label(
        ImageUI,
        text="Register Your Face",
        bg="#121212",
        fg="#00bcd4",
        font=("Segoe UI", 28, "bold"),
        pady=20
    )
    titl.pack(fill=X)

    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#121212",
        fg="#e0e0e0",
        font=("Segoe UI", 18, "bold"),
    )
    a.pack(pady=10)

    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        bg="#121212",
        fg="#ffb300",
        font=("Segoe UI", 14, "bold"),
    )
    lbl1.place(x=120, y=130)

    txt1 = tk.Entry(
        ImageUI,
        width=20,
        bd=2,
        bg="#2d2d2d",
        fg="#e0e0e0",
        relief=FLAT,
        font=("Segoe UI", 14, "bold"),
        insertbackground="white"
    )
    txt1.place(x=280, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        bg="#121212",
        fg="#ffb300",
        font=("Segoe UI", 14, "bold"),
    )
    lbl2.place(x=120, y=200)

    txt2 = tk.Entry(
        ImageUI,
        width=20,
        bd=2,
        bg="#2d2d2d",
        fg="#e0e0e0",
        relief=FLAT,
        font=("Segoe UI", 14, "bold"),
        insertbackground="white"
    )
    txt2.place(x=280, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        bg="#121212",
        fg="#ffb300",
        font=("Segoe UI", 14, "bold"),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=2,
        bg="#2d2d2d",
        fg="#e0e0e0",
        relief=FLAT,
        font=("Segoe UI", 12, "bold"),
    )
    message.place(x=250, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    takeImg = tk.Button(ImageUI, text="Take Image", command=take_image, **button_style)
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    trainImg = tk.Button(ImageUI, text="Train Image", command=train_image, **button_style)
    trainImg.place(x=360, y=350)


# ------------- Attendance + View Functions -------------
def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


window.mainloop()
