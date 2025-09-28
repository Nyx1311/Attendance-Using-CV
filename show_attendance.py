import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)

        filenames = glob(
            f"Attendance\\{Subject}\\{Subject}*.csv"
        )
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf.loc[i, "Attendance"] = str(
                int(round(newdf.iloc[i, 2:-1].mean() * 100))
            ) + '%'

        newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

        root = tkinter.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="#121212")

        cs = f"Attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
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
        print(newdf)

    subject = Tk()
    subject.title("Subject Selection")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="#121212")

    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="#121212",
        fg="#00bcd4",
        font=("Segoe UI", 20, "bold"),
    )
    titl.pack(pady=15)

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
        text="View Attendance",
        command=calculate_attendance,
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
