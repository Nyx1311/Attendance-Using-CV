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
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "TrainingImageLabel\\Trainner.yml"
)
trainimage_path = "TrainingImage"
studentdetail_path = (
    "StudentDetails\\studentdetails.csv"
)
attendance_path = "Attendance"
# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found, please train model"
                    Notifica.configure(
                        text=e,
                        bg="#1e1e1e",
                        fg="#ffcc00",
                        font=("Segoe UI", 13, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg="#1e1e1e",
                    fg="#00e676",
                    font=("Segoe UI", 13, "bold"),
                )
                text_to_speech(m)
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="#121212")
                cs = os.path.join(path, fileName)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(
                                root,
                                width=12,
                                height=1,
                                fg="#00bcd4",
                                font=("Segoe UI", 12, "bold"),
                                bg="#121212",
                                text=row,
                                relief=tkinter.FLAT,
                            )
                            label.grid(row=r, column=c, padx=5, pady=5)
                            c += 1
                        r += 1
                root.mainloop()
            except:
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    ### window is frame for subject chooser
    subject = Tk()
    subject.title("Subject Selection")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="#121212")

    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="#121212",
        fg="#00bcd4",
        font=("Segoe UI", 20, "bold"),
    )
    titl.pack(pady=15)

    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="#1e1e1e",
        fg="#00e676",
        font=("Segoe UI", 12, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    sub_lbl = tk.Label(
        subject,
        text="Subject:",
        bg="#121212",
        fg="#e0e0e0",
        font=("Segoe UI", 14),
    )
    sub_lbl.place(x=60, y=110)

    tx = tk.Entry(
        subject,
        width=18,
        bg="#1e1e1e",
        fg="#ffffff",
        insertbackground="white",
        relief=tk.FLAT,
        font=("Segoe UI", 14),
    )
    tx.place(x=180, y=110, height=35)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=0,
        font=("Segoe UI", 12, "bold"),
        bg="#00bcd4",
        fg="white",
        activebackground="#00e5ff",
        activeforeground="black",
        height=2,
        width=15,
        relief=tk.FLAT,
    )
    fill_a.place(x=120, y=200)

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=0,
        font=("Segoe UI", 12, "bold"),
        bg="#4caf50",
        fg="white",
        activebackground="#66bb6a",
        activeforeground="black",
        height=2,
        width=15,
        relief=tk.FLAT,
    )
    attf.place(x=300, y=200)

    subject.mainloop()
