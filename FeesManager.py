from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkinter import filedialog

class ClassFees:
    def __init__(self, root, ls, frame_old):
        self.ls = ls
        self.root = root
        self.frame_old = frame_old
        self.Roll_No_var = StringVar()
        self.fees_paid_var = IntVar()
        self.receipt_no_var = StringVar()  # Variable for receipt_no

        # Creating the main frame.
        self.frame = Frame(root, bg='#163148')
        self.frame.place(x=0, y=0, width=ls[0], height=ls[1])

        # Creating a back button.
        exit_btn = Button(self.frame, text="Back", relief=RAISED, bg='#fbf8e6', command=self.exiting)
        exit_btn.place(x=10, y=10, width=100, height=40)

        # Labeling the title
        title = Label(self.frame, text='Manage Student Fees', font=('Algerian', 25, 'bold'), bg='lightgreen')
        title.pack(side=TOP)

        # Creating a frame for student list.
        Student_Frame = Frame(self.frame, bd=4, relief=RIDGE, bg='LightBlue')
        Student_Frame.place(x=10, y=100, width=ls[0] - 20, height=ls[1] // 3)

        # Table for displaying student list.
        self.Student_table = ttk.Treeview(Student_Frame, columns=("Roll", "Name", "Class", "Fees Paid", "Fees Due"))
        self.Student_table.heading("Roll", text="Roll No.")
        self.Student_table.heading("Name", text="Name")
        self.Student_table.heading("Class", text="Class")  # Added Class column
        self.Student_table.heading("Fees Paid", text="Fees Paid")
        self.Student_table.heading("Fees Due", text="Fees Due")
        self.Student_table['show'] = 'headings'
        self.Student_table.column("Roll", width=100)
        self.Student_table.column("Name", width=150)
        self.Student_table.column("Class", width=100)  # Column for class
        self.Student_table.column("Fees Paid", width=150)
        self.Student_table.column("Fees Due", width=150)
        self.Student_table.pack(fill=BOTH, expand=1)
        self.Student_table.bind("<ButtonRelease-1>", self.get_cursor)

        # Creating a frame for fee management.
        Manage_Frame = Frame(self.frame, bd=4, relief=RIDGE, bg="cornsilk")
        Manage_Frame.place(x=10, y=ls[1] // 2, width=ls[0] - 20, height=ls[1] // 4)

        # Label and Entry for payment amount.
        lbl_fees = Label(Manage_Frame, text="Enter Payment Amount:", bg="cornsilk", fg="blue", font=("times new roman", 16, "bold"))
        lbl_fees.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        txt_fees = Entry(Manage_Frame, textvariable=self.fees_paid_var, font=("times new roman", 14), bd=5, relief=GROOVE)
        txt_fees.grid(row=0, column=1, pady=20, padx=20, sticky="w")

        # Label and Entry for receipt number.
        lbl_receipt = Label(Manage_Frame, text="Enter Receipt No.:", bg="cornsilk", fg="blue", font=("times new roman", 16, "bold"))
        lbl_receipt.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        txt_receipt = Entry(Manage_Frame, textvariable=self.receipt_no_var, font=("times new roman", 14), bd=5, relief=GROOVE)
        txt_receipt.grid(row=1, column=1, pady=20, padx=20, sticky="w")

        # Submit Button
        submit_btn = Button(Manage_Frame, text="Submit Payment", bg='black', fg='white', width=20, command=self.add_payment)
        submit_btn.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        # View Payment History Button
        view_history_btn = Button(Manage_Frame, text="View Payment History", bg='blue', fg='white', width=20, command=self.view_payment_history)
        view_history_btn.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # Print Payment History Button
        print_history_btn = Button(Manage_Frame, text="Print/Save Payment History", bg='green', fg='white', width=20, command=self.print_payment_history)
        print_history_btn.grid(row=2, column=2, pady=10, padx=10, sticky="w")

        # Print Fee Balances Button
        print_fee_balances_btn = Button(Manage_Frame, text="Print/Save Fee Balances", bg='orange', fg='white', width=20, command=self.print_fee_balances)
        print_fee_balances_btn.grid(row=2, column=3, pady=10, padx=10, sticky="w")

        # Fetch and display students.
        self.fetch_students()

    def fetch_students(self):
        """Fetch and display the list of students and their fees, sorted by class."""
        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()
        cur.execute("""
            SELECT sd.Roll_No, sd.Name, sd.email, IFNULL(sf.fees_paid, 0), IFNULL(sf.fees_rem, 3500)
            FROM student_data sd 
            LEFT JOIN student_fees sf ON sd.Roll_No = sf.Roll_No
            ORDER BY sd.email ASC
        """)
        rows = cur.fetchall()
        self.Student_table.delete(*self.Student_table.get_children())
        for row in rows:
            self.Student_table.insert('', END, values=row)
        conn.close()

    def get_cursor(self, ev):
        """Handle the event when a student is selected from the list."""
        cursor_row = self.Student_table.focus()
        contents = self.Student_table.item(cursor_row)
        row = contents['values']
        self.Roll_No_var.set(row[0])

    def add_payment(self):
        """Add payment to the selected student and update the database."""
        if not self.Roll_No_var.get() or not self.receipt_no_var.get():
            messagebox.showerror("Error", "Please select a student and enter a receipt number.")
            return

        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()

        payment = self.fees_paid_var.get()
        roll_no = self.Roll_No_var.get()
        receipt_no = self.receipt_no_var.get()

        # Fetch current fees details.
        cur.execute("SELECT fees_paid, fees_rem FROM student_fees WHERE Roll_No = ?", (roll_no,))
        fees = cur.fetchone()

        if fees:
            new_paid = fees[0] + payment
            new_due = max(fees[1] - payment, 0)

            # Update student_fees table.
            cur.execute("UPDATE student_fees SET fees_paid = ?, fees_rem = ? WHERE Roll_No = ?", 
                        (new_paid, new_due, roll_no))
        else:
            new_paid = payment
            new_due = max(3500 - payment, 0)

            # Insert into student_fees table.
            cur.execute("INSERT INTO student_fees (Roll_No, fees_paid, fees_rem) VALUES (?, ?, ?)", 
                        (roll_no, new_paid, new_due))

        # Insert payment record into payments table with receipt_no.
        cur.execute("INSERT INTO payments (Roll_No, payment_amount, payment_date, receipt_no) VALUES (?, ?, ?, ?)", 
                    (roll_no, payment, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), receipt_no))

        conn.commit()
        conn.close()

        self.fetch_students()
        self.fees_paid_var.set(0)
        self.receipt_no_var.set("")

    def view_payment_history(self):
        """View the payment history for the selected student."""
        if not self.Roll_No_var.get():
            messagebox.showerror("Error", "Please select a student to view payment history.")
            return

        roll_no = self.Roll_No_var.get()

        # Create a new window to display the payment history
        history_win = Toplevel(self.root)
        history_win.title("Payment History")
        history_win.geometry("500x400")

        # Fetch payment history from the database
        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()
        cur.execute("SELECT payment_date, payment_amount, receipt_no FROM payments WHERE Roll_No = ?", (roll_no,))
        rows = cur.fetchall()
        conn.close()

        # Display the payment history in the new window
        history_label = Label(history_win, text=f"Payment History for Roll No: {roll_no}", font=("Arial", 12, "bold"))
        history_label.pack()

        history_frame = Frame(history_win)
        history_frame.pack(fill=BOTH, expand=True)

        history_table = ttk.Treeview(history_frame, columns=("Date", "Amount", "Receipt No"))
        history_table.heading("Date", text="Date")
        history_table.heading("Amount", text="Amount")
        history_table.heading("Receipt No", text="Receipt No")
        history_table['show'] = 'headings'

        history_table.column("Date", width=150)
        history_table.column("Amount", width=100)
        history_table.column("Receipt No", width=100)

        history_table.pack(fill=BOTH, expand=True)

        for row in rows:
            history_table.insert('', END, values=row)

    def print_payment_history(self):
        """Export the payment history to a text file."""
        if not self.Roll_No_var.get():
            messagebox.showerror("Error", "Please select a student to print payment history.")
            return

        roll_no = self.Roll_No_var.get()

        # Fetch payment history from the database
        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()
        cur.execute("SELECT payment_date, payment_amount, receipt_no FROM payments WHERE Roll_No = ?", (roll_no,))
        rows = cur.fetchall()
        conn.close()

        # Export payment history to a text file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(f"Payment History for Roll No: {roll_no}\n")
                f.write(f"{'Date':<20} {'Amount':<10} {'Receipt No':<10}\n")
                f.write("=" * 40 + "\n")
                for row in rows:
                    f.write(f"{row[0]:<20} {row[1]:<10} {row[2]:<10}\n")

            messagebox.showinfo("Success", "Payment history exported successfully.")

    def print_fee_balances(self):
        """Export the current fee balances to a text file."""
        conn = sqlite3.connect('employee.db')
        cur = conn.cursor()
        cur.execute("""
            SELECT sd.Roll_No, sd.Name, sd.email, IFNULL(sf.fees_paid, 0), IFNULL(sf.fees_rem, 3500)
            FROM student_data sd 
            LEFT JOIN student_fees sf ON sd.Roll_No = sf.Roll_No
            ORDER BY sd.email ASC
        """)
        rows = cur.fetchall()
        conn.close()

        # Export fee balances to a text file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(f"{'Roll No.':<10} {'Name':<20} {'Class':<10} {'Fees Paid':<10} {'Fees Due':<10}\n")
                f.write("=" * 60 + "\n")
                for row in rows:
                    f.write(f"{row[0]:<10} {row[1]:<20} {row[2]:<10} {row[3]:<10} {row[4]:<10}\n")

            messagebox.showinfo("Success", "Fee balances exported successfully.")

    def exiting(self):
        self.frame.destroy()
        self.frame_old.deiconify()

def login(root, ls):
    frame = Frame(root, bg='#163148')
    frame.place(x=0, y=0, width=ls[0], height=ls[1])

    Label(frame, text="Login", font=("Arial", 24), bg='#163148', fg='white').pack(pady=50)

    username_var = StringVar()
    password_var = StringVar()

    Label(frame, text="Username:", font=("Arial", 14), bg='#163148', fg='white').pack(pady=10)
    Entry(frame, textvariable=username_var, font=("Arial", 14)).pack(pady=10)

    Label(frame, text="Password:", font=("Arial", 14), bg='#163148', fg='white').pack(pady=10)
    Entry(frame, textvariable=password_var, font=("Arial", 14), show="*").pack(pady=10)

    def attempt_login():
        # In a real application, replace this with actual login validation
        if username_var.get() == "admin" and password_var.get() == "password":
            frame.destroy()
            ClassFees(root, ls, root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    Button(frame, text="Login", font=("Arial", 14), command=attempt_login).pack(pady=20)

if __name__ == "__main__":
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}")
    root.title("Fees Management System")

    login(root, (width, height))

    root.mainloop()
