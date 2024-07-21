import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
from tkinter import filedialog
import sqlite3
import csv
import re

class StudentDatabase:
    def __init__(self, db_name="student.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS STUD_REGISTRATION (
               STU_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
               STU_NAME TEXT, STU_CONTACT TEXT, 
               STU_EMAIL TEXT, STU_ROLLNO TEXT, 
               STU_BRANCH TEXT)"""
        )
        self.conn.commit()

    def insert(self, name, contact, email, rollno, branch):
        self.cursor.execute(
            "INSERT INTO STUD_REGISTRATION (STU_NAME, STU_CONTACT, STU_EMAIL, STU_ROLLNO, STU_BRANCH) "
            "VALUES (?, ?, ?, ?, ?)", (name, contact, email, rollno, branch)
        )
        self.conn.commit()

    def delete(self, stu_id):
        self.cursor.execute("DELETE FROM STUD_REGISTRATION WHERE STU_ID = ?", (stu_id,))
        self.conn.commit()

    def update(self, stu_id, name, contact, email, rollno, branch):
        self.cursor.execute(
            """UPDATE STUD_REGISTRATION 
               SET STU_NAME = ?, STU_CONTACT = ?, STU_EMAIL = ?, STU_ROLLNO = ?, STU_BRANCH = ? 
               WHERE STU_ID = ?""", (name, contact, email, rollno, branch, stu_id)
        )
        self.conn.commit()

    def search(self, name=None, email=None, rollno=None):
        query = "SELECT * FROM STUD_REGISTRATION WHERE 1=1"
        params = []
        if name:
            query += " AND STU_NAME LIKE ?"
            params.append('%' + name + '%')
        if email:
            query += " AND STU_EMAIL LIKE ?"
            params.append('%' + email + '%')
        if rollno:
            query += " AND STU_ROLLNO LIKE ?"
            params.append('%' + rollno + '%')
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM STUD_REGISTRATION")
        return self.cursor.fetchall()

    def clear_all(self):
        self.cursor.execute("DELETE FROM STUD_REGISTRATION")
        self.conn.commit()

    def close(self):
        self.conn.close()

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x700")
        self.root.title("Student Management System")
        self.db = StudentDatabase()
        self.setup_ui()

    def setup_ui(self):
        self.setup_frames()
        self.setup_widgets()

    def setup_frames(self):
        self.top_frame = tk.Frame(self.root, width=1200, height=100, bg="#003366")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.left_frame = tk.Frame(self.root, width=400, bg="#e0f7fa")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.mid_frame = tk.Frame(self.root, bg="white")
        self.mid_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self.mid_frame, bg="white")
        self.right_frame.pack(side=tk.TOP, fill=tk.X)

    def setup_widgets(self):
        tk.Label(self.top_frame, text="Student Management System", font=('Helvetica', 24, 'bold'), bg="#003366", fg="white").pack(fill=tk.X)

        self.name = tk.StringVar()
        self.contact = tk.StringVar()
        self.email = tk.StringVar()
        self.rollno = tk.StringVar()
        self.branch = tk.StringVar()
        self.search_var = tk.StringVar()

        tk.Label(self.left_frame, text="Name", font=("Arial", 12), bg="#e0f7fa").pack(pady=5)
        tk.Entry(self.left_frame, font=("Arial", 12), textvariable=self.name).pack(padx=10, fill=tk.X)

        tk.Label(self.left_frame, text="Contact", font=("Arial", 12), bg="#e0f7fa").pack(pady=5)
        tk.Entry(self.left_frame, font=("Arial", 12), textvariable=self.contact).pack(padx=10, fill=tk.X)

        tk.Label(self.left_frame, text="Email", font=("Arial", 12), bg="#e0f7fa").pack(pady=5)
        tk.Entry(self.left_frame, font=("Arial", 12), textvariable=self.email).pack(padx=10, fill=tk.X)

        tk.Label(self.left_frame, text="Rollno", font=("Arial", 12), bg="#e0f7fa").pack(pady=5)
        tk.Entry(self.left_frame, font=("Arial", 12), textvariable=self.rollno).pack(padx=10, fill=tk.X)

        tk.Label(self.left_frame, text="Branch", font=("Arial", 12), bg="#e0f7fa").pack(pady=5)
        radio_frame = tk.Frame(self.left_frame, bg="#e0f7fa")
        radio_frame.pack(fill=tk.X, padx=10)
        ttk.Radiobutton(radio_frame, text="New", value="New", variable=self.branch).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(radio_frame, text="Old", value="Old", variable=self.branch).pack(side=tk.LEFT, padx=5)

        tk.Button(self.left_frame, text="Submit", font=("Arial", 12, "bold"), command=self.register, bg="#004d40", fg="white").pack(pady=10, fill=tk.X)
        tk.Button(self.left_frame, text="Update", font=("Arial", 12, "bold"), command=self.update_record, bg="#004d40", fg="white").pack(pady=10, fill=tk.X)

        tk.Label(self.right_frame, text="Search by Name", font=('Verdana', 12), bg="white").pack(pady=10)
        tk.Entry(self.right_frame, textvariable=self.search_var, font=('Verdana', 12), width=20).pack(pady=10)

        tk.Button(self.right_frame, text="Search", font=("Arial", 12, "bold"), command=self.search_record, bg="#004d40", fg="white").pack(pady=5, fill=tk.X)
        tk.Button(self.right_frame, text="View All", font=("Arial", 12, "bold"), command=self.display_data, bg="#004d40", fg="white").pack(pady=5, fill=tk.X)
        tk.Button(self.right_frame, text="Reset", font=("Arial", 12, "bold"), command=self.reset, bg="#004d40", fg="white").pack(pady=5, fill=tk.X)
        tk.Button(self.right_frame, text="Delete", font=("Arial", 12, "bold"), command=self.delete_record, bg="#004d40", fg="white").pack(pady=5, fill=tk.X)
        tk.Button(self.right_frame, text="Export to CSV", font=("Arial", 12, "bold"), command=self.export_to_csv, bg="#004d40", fg="white").pack(pady=5, fill=tk.X)
        tk.Button(self.right_frame, text="Import from CSV", font=("Arial", 12, "bold"), command=self.import_from_csv, bg="#004d40", fg="white").pack(pady=5, fill=tk.X)
        tk.Button(self.right_frame, text="Clear All Data", font=("Arial", 12, "bold"), command=self.clear_all_data, bg="#004d40", fg="white").pack(pady=5, fill=tk.X)

        self.scrollbarx = tk.Scrollbar(self.mid_frame, orient=tk.HORIZONTAL)
        self.scrollbary = tk.Scrollbar(self.mid_frame, orient=tk.VERTICAL)

        self.tree = ttk.Treeview(self.mid_frame, columns=("Student Id", "Name", "Contact", "Email", "Rollno", "Branch"),
                                selectmode="extended", height=15, yscrollcommand=self.scrollbary.set,
                                xscrollcommand=self.scrollbarx.set)
        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.heading('Student Id', text="Student Id", anchor=tk.W)
        self.tree.heading('Name', text="Name", anchor=tk.W)
        self.tree.heading('Contact', text="Contact", anchor=tk.W)
        self.tree.heading('Email', text="Email", anchor=tk.W)
        self.tree.heading('Rollno', text="Rollno", anchor=tk.W)
        self.tree.heading('Branch', text="Branch", anchor=tk.W)

        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('Student Id', stretch=tk.YES, minwidth=70, width=100)
        self.tree.column('Name', stretch=tk.YES, minwidth=120, width=150)
        self.tree.column('Contact', stretch=tk.YES, minwidth=100, width=150)
        self.tree.column('Email', stretch=tk.YES, minwidth=150, width=200)
        self.tree.column('Rollno', stretch=tk.YES, minwidth=80, width=120)
        self.tree.column('Branch', stretch=tk.YES, minwidth=100, width=150)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def register(self):
        name = self.name.get()
        contact = self.contact.get()
        email = self.email.get()
        rollno = self.rollno.get()
        branch = self.branch.get()

        if not name or not contact or not email or not rollno or not branch:
            tkMessageBox.showerror("Input Error", "All fields are required")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            tkMessageBox.showerror("Input Error", "Invalid email format")
            return

        if not rollno.isdigit():
            tkMessageBox.showerror("Input Error", "Rollno must be numeric")
            return

        self.db.insert(name, contact, email, rollno, branch)
        tkMessageBox.showinfo("Success", "Student registered successfully")
        self.reset()

    def update_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            tkMessageBox.showerror("Selection Error", "Select a record to update")
            return

        stu_id = self.tree.item(selected_item[0])['values'][0]
        name = self.name.get()
        contact = self.contact.get()
        email = self.email.get()
        rollno = self.rollno.get()
        branch = self.branch.get()

        if not name or not contact or not email or not rollno or not branch:
            tkMessageBox.showerror("Input Error", "All fields are required")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            tkMessageBox.showerror("Input Error", "Invalid email format")
            return

        if not rollno.isdigit():
            tkMessageBox.showerror("Input Error", "Rollno must be numeric")
            return

        self.db.update(stu_id, name, contact, email, rollno, branch)
        tkMessageBox.showinfo("Success", "Student updated successfully")
        self.reset()

    def search_record(self):
        search_name = self.search_var.get()
        records = self.db.search(name=search_name)
        self.update_treeview(records)

    def display_data(self):
        records = self.db.fetch_all()
        self.update_treeview(records)

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            tkMessageBox.showerror("Selection Error", "Select a record to delete")
            return

        stu_id = self.tree.item(selected_item[0])['values'][0]
        self.db.delete(stu_id)
        tkMessageBox.showinfo("Success", "Student deleted successfully")
        self.reset()

    def export_to_csv(self):
        records = self.db.fetch_all()
        file_name = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")])
        if not file_name:
            return
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Student Id", "Name", "Contact", "Email", "Rollno", "Branch"])
            for record in records:
                writer.writerow(record)
        tkMessageBox.showinfo("Success", "Data exported to CSV successfully")

    def import_from_csv(self):
        file_name = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_name:
            return
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 6:
                    self.db.insert(row[1], row[2], row[3], row[4], row[5])
        tkMessageBox.showinfo("Success", "Data imported from CSV successfully")
        self.display_data()

    def clear_all_data(self):
        self.db.clear_all()
        tkMessageBox.showinfo("Success", "All data cleared")
        self.reset()

    def reset(self):
        self.name.set("")
        self.contact.set("")
        self.email.set("")
        self.rollno.set("")
        self.branch.set("")
        self.search_var.set("")
        self.display_data()

    def update_treeview(self, records):
        self.tree.delete(*self.tree.get_children())
        for record in records:
            self.tree.insert('', 'end', values=record)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
