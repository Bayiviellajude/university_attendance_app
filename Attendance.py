import datetime
from os import name
import tkinter as tk
from tkinter import Label, messagebox, simpledialog
import pyodbc


class CKT_UTAS_AttendanceSystem(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='#F0F0F0')
        self.master = master
        self.pack()
        self.create_widgets()

        # Connect to database
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=E:\#200 sec sem 23\PROJECT WORK\PROJECT WORK RESEARCH\python atten pro 1\Database2.accdb;'
        )
        self.conn = pyodbc.connect(conn_str)
        self.c = self.conn.cursor()
    
        

    def create_login_window(self):
        self.login_window = tk.Toplevel(self)
        self.login_window.title("Login")
        self.login_window.geometry("300x200")
        self.login_window.configure(bg='#F0F0F0')
        self.login_window.iconbitmap('LOGO.ico')
        self.login_window.resizable(True, True)

        # Add username label and input field
        self.username_label = tk.Label(self.login_window, text="Username:", bg='#F0F0F0', fg='#333')
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.login_window, width=45)
        self.username_entry.pack()

        # Add password label and input field
        self.password_label = tk.Label(self.login_window, text="Password:", bg='#F0F0F0', fg='#333')
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.login_window, width=45, show='*')
        self.password_entry.pack()

        # Add login button
        self.login_button = tk.Button(self.login_window, text="Login", bg='#4CAF50', fg='white', command=self.check_credentials)
        self.login_button.pack(pady=10)
        
    def create_widgets(self):
    # Create login window
     self.create_login_window()

    # Add logo label
     self.logo = tk.PhotoImage(file='LOGO.png')
     self.logo_label = tk.Label(self, image=self.logo, bg='#F0F0F0')
     self.logo_label.pack(side="top", pady=10)

    # Disable other buttons and functionality
     self.label = tk.Label(self, text="STUDENTS' ONLY!!!",font=("Arial", 12, "bold"), bg='#F0F0F0', fg='brown')
     self.label.pack(side="top", pady=10)
     
     self.label = tk.Label(self, text="ENTER YOUR ID AND COURSE CODE TO TAKE ATTENDANCE",font=("Arial", 12, "bold"), bg='#F0F0F0', fg='green')
     self.label.pack(side="top", pady=10)
        
     self.scan_button = tk.Button(self, text="Enter ID & Course Code",font=("Arial", 10, "bold"), state='disabled', command=self.scan_student_id, bg='#4CAF50', fg='white', padx=20, pady=10,width=30)
     self.scan_button.pack(side="top", pady=10)
     
     self.label = tk.Label(self, text="STRICTLY FOR LECTURERS ONLY!!!",font=("Arial", 12, "bold"), bg='#F0F0F0', fg='brown')
     self.label.pack(side="top", pady=10)

     self.add_student_button = tk.Button(self, text="Add New Student",font=("Arial", 10, "bold"), state='disabled', command=self.show_add_student_dialog, bg='brown', fg='white', padx=20, pady=10,width=30)
     self.add_student_button.pack(side="top", pady=10)

     self.view_attendance_button = tk.Button(self, text="View Attendance List",font=("Arial", 10, "bold"), state='disabled', command=self.show_view_attendance_dialog, bg='brown', fg='white', padx=20, pady=10,width=30)
     self.view_attendance_button.pack(side="top", pady=10)

     self.search_button = tk.Button(self, text="Search",font=("Arial", 10, "bold"), state='disabled', command=self.show_search_dialog, bg='brown', fg='white', padx=20, pady=10,width=30)
     self.search_button.pack(side="top", pady=10)


    def check_credentials(self):
     username = self.username_entry.get()
     password = self.password_entry.get()

    # Check the database for the entered username and password
     self.c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
     result = self.c.fetchone()

     if result:
        # If the credentials are correct, destroy the login window and enable the main window
        self.login_window.destroy()
        self.scan_button['state'] = 'normal'
        self.add_student_button['state'] = 'normal'
        self.view_attendance_button['state'] = 'normal'
        self.search_button['state'] = 'normal'
     else:
        # If the credentials are incorrect, show an error message
        messagebox.showerror("Error", "Invalid username or password!")

       
    def show_add_student_dialog(self):
     add_student_window = tk.Toplevel(self)
     add_student_window.title("Add New Student")
     add_student_window.geometry("300x200")
     add_student_window.configure(bg='#F0F0F0')
     add_student_window.iconbitmap('LOGO.ico')
     add_student_window.resizable(True, True)

    # Add student ID label and input field
     student_id_label = tk.Label(add_student_window, text="Student ID:", bg='#F0F0F0', fg='#333')
     student_id_label.pack(pady=10)
     student_id_entry = tk.Entry(add_student_window, width=45)
     student_id_entry.pack()

    # Add student name label and input field
     name_label = tk.Label(add_student_window, text="Name:", bg='#F0F0F0', fg='#333')
     name_label.pack(pady=10)
     name_entry = tk.Entry(add_student_window, width=45)
     name_entry.pack()

    # Add submit button
     submit_button = tk.Button(add_student_window, text="Add Student",bg='#4CAF50', fg='white', command=lambda: self.add_student_to_database(student_id_entry.get(), name_entry.get(), add_student_window))
     submit_button.pack(pady=10)
    
    
    def add_student_to_database(self, student_id, name, add_student_window):
     if not student_id:
        messagebox.showerror("Error", "Please enter the student ID!")
        return
     if not name:
        messagebox.showerror("Error", "Please enter the student's name!")
        return
    # Save the new student details to the database
     self.c.execute("INSERT INTO students (student_id, name) VALUES (?, ?)", (student_id, name))
     self.conn.commit()
     messagebox.showinfo("Success", "New student added successfully!")
     add_student_window.destroy()



    def scan_student_id(self):
    # Create a new window for scanning the student ID
     scan_window = tk.Toplevel(self)
     scan_window.title("ATTENDANCE")
     scan_window.geometry("300x200")
     scan_window.configure(bg='#F0F0F0')
     scan_window.iconbitmap('LOGO.ico')
     scan_window.resizable(True, True)

    # Add a label and input field for entering the student ID
     student_id_label = tk.Label(scan_window, text="Enter the student ID:", bg='#F0F0F0', fg='#333')
     student_id_label.pack(pady=10)
     student_id_entry = tk.Entry(scan_window, width=45)
     student_id_entry.pack()

    # Add a label and input field for entering the course code
     course_code_label = tk.Label(scan_window, text="Enter the course code:", bg='#F0F0F0', fg='#333')
     course_code_label.pack(pady=10)
     course_code_entry = tk.Entry(scan_window, width=45)
     course_code_entry.pack()

    # Add a button to scan the student ID
     scan_button = tk.Button(scan_window, text="Verify ID & Course Code",bg='#4CAF50', fg='white', command=lambda: self.process_student_id(student_id_entry.get(), course_code_entry.get(), scan_window))
     scan_button.pack(pady=10)
    
    
     
    def process_student_id(self, student_id, course_code, scan_window):
     if not student_id:
        return

     student = self.c.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
     if student is not None:
        name = student[1]
        verify = messagebox.askyesno("Verification", f"Are you {name}?")
        if verify:
            attendance_date = datetime.date.today().strftime("%Y-%m-%d")
            attendance_status = "present"
            self.c.execute("INSERT INTO attendance (attendance_date, student_id, attendance_status, course_code) VALUES (?, ?, ?, ?)", (attendance_date, student_id, attendance_status, course_code))
            self.conn.commit()
            messagebox.showinfo("PRESENT!")
            scan_window.destroy()  # Close the scan window after successful attendance
        else:
            messagebox.showinfo("Sorry, your identity could not be verified!")
     else:
            messagebox.showinfo("Sorry, your student ID is not registered in the system!")


    
    def show_view_attendance_dialog(self):
     view_attendance_window = tk.Toplevel(self)
     view_attendance_window.title("View Attendance")
     view_attendance_window.geometry("300x200")
     view_attendance_window.configure(bg='#F0F0F0')
     view_attendance_window.iconbitmap('LOGO.ico')
     view_attendance_window.resizable(True, True)

    # Add date label and input field
     date_label = tk.Label(view_attendance_window, text="Select Date (mm-dd-yyyy):", bg='#F0F0F0', fg='#333')
     date_label.pack(pady=10)
     date_entry = tk.Entry(view_attendance_window, width=45)
     date_entry.pack()

    # Add submit button
     submit_button = tk.Button(view_attendance_window, text="View Attendance", bg='#4CAF50', fg='white',command=lambda: self.view_attendance(date_entry.get(), view_attendance_window))
     submit_button.pack(pady=10)

    def view_attendance(self, date, view_attendance_window):
     
    # Fetch attendance data from the database
     attendance_data = self.c.execute("SELECT * FROM attendance WHERE attendance_date=?", (date,)).fetchall()

    # Create a label to display the attendance data
     attendance_label = tk.Label(view_attendance_window, text="Attendance for " + date + ":", bg='#F0F0F0', fg='#333')
     attendance_label.pack(pady=10)

    # Create a text widget to display the attendance data
     text_widget = tk.Text(view_attendance_window)
     text_widget.pack()

    # Display the attendance data in the text widget
     for attendance in attendance_data:
        student_id = attendance[1]
        attendance_status = attendance[2]
        course_code = attendance[3]
        student = self.c.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
        name = student[1]
        text_widget.insert(tk.END, f"{name}  ({student_id}): ({attendance_status}): {course_code}\n")

    # Disable editing of the text widget
     text_widget.configure(state=tk.DISABLED)
    
    def show_search_dialog(self):
     search_window = tk.Toplevel(self)
     search_window.title("Search Student")
     search_window.geometry("300x200")
     search_window.configure(bg='#F0F0F0')
     search_window.iconbitmap('LOGO.ico')
     search_window.resizable(True, True)

    # Add search label and input field
     search_label = tk.Label(search_window, text="Enter Student ID:", bg='#F0F0F0', fg='#333')
     search_label.pack(pady=10)
     search_entry = tk.Entry(search_window, width=45)
     search_entry.pack()
 
    # Add search button
     submit_button = tk.Button(search_window, text="Search Student",bg='#4CAF50', fg='white', command=lambda: self.search_student(search_entry.get(), search_window))
     submit_button.pack(pady=10)
     
    def search_student(self, student_id, search_window):
     if not student_id:
        messagebox.showerror("Error", "Please enter the student ID!")
        return
    
     student = self.c.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
     if student is not None:
        name = student[1]
        
        # Query course codes from the database
        course_codes = self.c.execute("SELECT DISTINCT course_code FROM attendance WHERE student_id=?", (student_id,)).fetchall()
        if course_codes:
            attendance_text = ""
            for code in course_codes:
                attendance_records = self.c.execute("SELECT * FROM attendance WHERE student_id=? AND course_code=?", (student_id, code[0])).fetchall()
                attendance_list = []
                for a in attendance_records:
                    attendance_list.append(f"{a[0]}: {a[2]}")
                attendance_text += f"\nAttendance for {code[0]}:\n" + "\n".join(attendance_list) + "\n"
                
            messagebox.showinfo(f"Attendance for {name}", attendance_text)
        else:
            messagebox.showinfo("No Attendance Found", f"No attendance found for {name}")
        search_window.destroy()
     else:
            messagebox.showinfo("Student Not Found", "The student ID entered could not be found in the database.")
    
    


def __del__(self):
        # Close

        # Close database connection
        self.conn.commit()
        self.conn.close()


root = tk.Tk()  
root.title('CKT UTAS ATTENDANCE SYSTEM')
root.geometry('300x250')
root.configure(bg='#A52A2A')
root.iconbitmap('LOGO.ico')
app = CKT_UTAS_AttendanceSystem(master=root)
app.mainloop()
