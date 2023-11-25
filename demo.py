from tkinter import*
from tkinter import ttk
import random
import time
import datetime
from tkinter import messagebox
import pymysql


class Hospital:
    def _init_(self,root):
        self.root=root
        self.root.title("Hospital Management System")
        self.root.geometry("1540x800+0+0")


root=Tk()
ob=Hospital()
root.mainloop()