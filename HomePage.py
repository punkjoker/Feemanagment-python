from tkinter import *
from tkinter import ttk

import Login_Employee  # Import only the employee login module

class Main_Page:
    def __init__(self, root, ls):
        self.root = root
        self.ls = ls
        
        # Creating the main frame.
        self.frame = Frame(root, bg='#163148')
        self.frame.place(x=0, y=0, width=ls[0], height=ls[1])

        # Creating a centered frame for login options.
        self.frame1 = Frame(self.frame, bg='#ffffff')
        self.frame1.place(relx=0.5, rely=0.5, anchor=CENTER, width=ls[0]//3, height=ls[1]//2)  # Centered frame

        # Taking the employee image in the variable.
        self.photo_employee = PhotoImage(file=r"Images/employee.png")

        # Resizing the image as per requirement.
        self.photo_employee = self.photo_employee.subsample(4, 4)

        # Labeling the page.
        self.title = Label(self.frame, text='Matendeni ECD Fee Management', font=('Algerian', 25, 'bold'), bg='LightGreen').pack(
            side=TOP)

        # Title for Register/Login.
        self.title1 = Label(self.frame1, text='Login Admin', font=('Algerian', 25, 'bold'), bg='#ffffff').pack(side=TOP, pady=20)

        # Creating a button for employee login only.
        self.employee_btn = Button(self.frame1, text="Faculty", bd=0, bg='#ffffff', image=self.photo_employee,
                                   compound=TOP, command=self.employee)
        self.employee_btn.place(relx=0.5, rely=0.5, anchor=CENTER, width=ls[0]//9, height=ls[1]//3)  # Centered button

    def employee(self):
        self.frame.place_forget()
        employee_menu = Login_Employee.Employee_Show(self.root, self.ls, self.frame)
