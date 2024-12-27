""" 
            STUDENT MANAGEMENT SYSTEM USING CRUD operations
Student Management System using Python and Tkinter,
with features such as user authentication, data entry,
validation,and interaction with a MySQL database
"""
# importing modules 
from tkinter import * 
from tkinter import ttk,messagebox
import mysql.connector 
import re 

# database connection 
def initialize_database_connection():
    global cur,conn
    try:
        # establishing the connection to Mysql Database
        conn = mysql.connector.connect(
            host="localhost",user="root",
            password="mysqlpassword"
        )
        # defining cursor 
        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS STUDENTDB;")
        cur.execute("USE STUDENTDB;")
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS STUDENTS(
                        ROLLNO INT PRIMARY KEY,
                        NAME VARCHAR(255),
                        GENDER VARCHAR(20),
                        CHECK (GENDER IN ('male','female')),
                        AGE INT,
                        DEPARTMENT VARCHAR(100),
                        PROGRAM VARCHAR(100),
                        YEAR_OF_STUDY VARCHAR(100),
                        MOBILE BIGINT,
                        EMAIL VARCHAR(100)
                        );""")
        conn.commit()
    except mysql.connector.Error as db_error:
        messagebox.showerror("Database Error",f"Error: {db_error}")
    except Exception as a:
        messagebox.showerror("Database Error",a)
    else:
        print("Connection is established\nConnected to studentdb database")

#helper functions 
# validates mobile number (must be in 10 digits)
def is_valid_mobile(mobile):
    if len(str(mobile)) != 10 :
        return False 
    return True 
# validating email address using regex 
def is_valid_email(email):
    return bool(re.match(r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$",email))
# checks if rollnumber is unique in database
def is_unique_rollno(rollno):
    cur.execute("select * from students where rollno = %s",(rollno,))
    return cur.fetchone() is None
     
# functionalities 
# inserting the record to the database table 
def add_student_record():
    try:
        rollno = int(e1.get())
        name = e2.get()
        gender = e3.get()
        age = int(e4.get())
        dept = e5.get()
        prg = e6.get()
        study = e7.get()
        mobile = int(e8.get())
        email = e9.get()
        
        if not rollno or not name or not gender or not age or not dept or not prg or not study or not mobile or not email:
            messagebox.showerror("Input Error","Please fill all the fields")
            return 
        if not is_valid_mobile(mobile):
            messagebox.showerror("Input Error","mobile number should must be 10 digits")
            return 
        if age < 0 :
            messagebox.showerror("Input Error","age should be positive integer")
            return 
        if not is_valid_email(email):
            messagebox.showerror("Input Error","Please enter valid email id")
            return 
        if not is_unique_rollno(rollno):
            messagebox.showerror("Input Error",f"Roll number {rollno} already exists")
            return 
        query = "INSERT INTO STUDENTS (ROLLNO,NAME,GENDER,AGE,DEPARTMENT,PROGRAM,YEAR_OF_STUDY,MOBILE,EMAIL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        vals = (rollno,name,gender,age,dept,prg,study,mobile,email)
        cur.execute(query,vals)
        conn.commit()
        show()
        clear()
        messagebox.showinfo("INFO","Student data successfully inserted")
    except Exception as a:
        print("Error",a)
        messagebox.showerror("Database Error",a)
        conn.rollback()
        
# displays all records from the database 
def show():
    listbox.delete(*listbox.get_children())
    cur.execute("SELECT * FROM STUDENTS;")
    records = cur.fetchall()
    for record in records:
        listbox.insert("",END,values=record)
        
# deletes all the student records from database    
def delete_all_student_records():
    res = messagebox.askyesnocancel("Database Deletion","Do you want to delete all the records")
    if res:
        try:
            messagebox.showwarning("Database Warning","It deletes all records permanently!")
            cur.execute("TRUNCATE STUDENTS;")
            conn.commit()
            show()
            messagebox.showinfo("INFO","All the records were deleted successfuly;")
        except Exception as a:
            print(f"Error: {a}")
# deletes a specific student record based on roll number        
def delete_student_record():
    try:
        if e1.get() != "":
            rollno = int(e1.get())
            query = 'SELECT * FROM STUDENTS WHERE ROLLNO=%s'
            cur.execute(query,(rollno,))
            if cur.fetchone() is None:
                messagebox.showinfo("INFO",f"There is no record on {rollno}")
                return 
            query = "DELETE FROM STUDENTS WHERE ROLLNO=%s"
            cur.execute(query,(rollno,))
            conn.commit()
            show()
            clear()
            messagebox.showinfo("INFO",f"{rollno} student record has been deleted")
        else:
            messagebox.showwarning("Database Deletion","enter rollnumber to delete the record")
            return 
    except Exception as a:
        print(f"Error: {a}")
        messagebox.showerror("Database Error",f"Error: {a}")
# updates an existing record based on roll no
def update_student_record():
    try:
        rollno = int(e1.get())
        name = e2.get()
        gender = e3.get()
        age = int(e4.get())
        dept = e5.get()
        prg = e6.get()
        study = e7.get()
        mobile = int(e8.get())
        email = e9.get()
        if not is_valid_mobile(mobile):
            messagebox.showerror("Input Error","mobile number should must be 10 digits")
            return 
        if age < 0 :
            messagebox.showerror("Input Error","age should be positive integer")
            return 
        if not is_valid_email(email):
            messagebox.showerror("Input Error","Please enter valid email id")
            return 
        cur.execute("SELECT * FROM STUDENTS WHERE ROLLNO = %s",(rollno,))
        if cur.fetchone() is None:
            messagebox.showinfo(f"INFO","No student record on rollnumber {rollno}")
            return 
        query = """
        UPDATE STUDENTS SET NAME = %s,GENDER = %s,AGE = %s,
        DEPARTMENT = %s,PROGRAM = %s,YEAR_OF_STUDY = %s,MOBILE = %s,
        EMAIL = %s WHERE rollno = %s;
        """ 
        vals = (name,gender,age,dept,prg,study,mobile,email,rollno)
        cur.execute(query,vals)
        conn.commit()
        show()
        clear()
        messagebox.showinfo("INFO","Record had been updated")
    except Exception as a:
        print(f"Error: {a}")
        messagebox.showerror("Database Error","Student data not been updated : {a}")
        conn.rollback()
# clears all the input fields        
def clear():
    e1.delete(0,END)
    e2.delete(0,END)
    e3.set(gender_options[0])
    e4.delete(0,END)
    e5.set(department_options[0])
    e6.set(degree_options[0])
    e7.set(options_three[0])
    e8.delete(0,END)
    e9.delete(0,END)
# event handler to select an student record from list
def select_row(event):
    selected_item = listbox.selection()
    if selected_item:
        record = listbox.item(selected_item,'values')
        clear()
        e1.insert(0,record[0])
        e2.insert(0,record[1])
        e3.set(record[2])
        e4.insert(0,record[3])
        e5.set(record[4])
        e6.set(record[5])
        e7.set(record[6])
        e8.insert(0,record[7])
        e9.insert(0,record[8])  
    
# GUI setup
root = Tk()
root.title("Student Management System")
root.geometry("900x680+0+0")
root.resizable(0,0)
# running database connection
initialize_database_connection()

# fonts
label_font = ("Arial",16)
title_font = ("Times New Roman",30)
entries_font = ("Arial",12)

# main label
Label(root,text="STUDENT MANAGEMENT\n   SYSTEM",font=title_font,fg="red").place(x=380,y=130)

# labels and entries 
Label(text="Roll.no",font=label_font).place(x=20,y=10)
e1 = Entry(root,borderwidth=3,width=30,font=entries_font)
e1.place(x=170,y=10)
Label(text="Name",font=label_font).place(x=20,y=40)
e2 = Entry(root,borderwidth=3,width=30,font=entries_font)
e2.place(x=170,y=40)
Label(text="Gender",font=label_font).place(x=20,y=70)
gender_options = ['male','female']
e3 = ttk.Combobox(root,values=gender_options,state='readonly',width=15,height=3,font=entries_font)
e3.place(x=170,y=70)
e3.set(gender_options[0])
Label(text="Age",font=label_font).place(x=20,y=100)
e4 = Entry(root,borderwidth=3,width=17,font=entries_font)
e4.place(x=170,y=100)
Label(text="Department",font=label_font).place(x=20,y=130)
department_options = [ 
                  "Computer Science", "Electrical Engineering", "Mechanical Engineering", 
                  "Civil Engineering", "Information Technology", "Biotechnology",
                  "Chemistry", "Mathematics", "Physics", "English Literature", 
                  "Business Administration", "Economics" ]
e5 = ttk.Combobox(root,values=department_options,state='readonly',width=15,font=entries_font)
e5.place(x=170,y=130)
e5.set(department_options[0])
Label(root, text="Program", font=label_font).place(x=20, y=160) 
degree_options = ["B.Tech", "B.Sc", "BA", "BBA", "M.Tech", "M.Sc", "MBA"] 
e6 = ttk.Combobox(root, values=degree_options, state="readonly", width=15,font=entries_font) 
e6.place(x=170, y=160) 
e6.set(degree_options[0])
Label(root, text="Year of Study", font=label_font).place(x=20, y=190) 
options_three = ["1st Year", "2nd Year", "3rd Year", "4th Year"] 
e7 = ttk.Combobox(root, values=options_three, state="readonly", width=15,font=entries_font) 
e7.place(x=170, y=190) 
e7.set(options_three[0])
Label(root, text="Mobile", font=label_font).place(x=20, y=220) 
e8 = Entry(root, borderwidth=3, width=30,font=entries_font) 
e8.place(x=170, y=220) 
Label(root, text="Email", font=label_font).place(x=20, y=250) 
e9 = Entry(root, borderwidth=3, width=30,font=entries_font) 
e9.place(x=170, y=250)

# buttons for each action 
Button(root,text="Add",command=add_student_record,height=1,width=8,bg='black',fg="white",font=label_font).place(x=35,y=300)
Button(root,text="Update",command=update_student_record,height=1,width=8,bg='black',fg="white",font=label_font).place(x=150,y=300)
Button(root,text="Delete",command=delete_student_record,height=1,width=8,bg='black',fg="white",font=label_font).place(x=260,y=300)
Button(root,text="DeleteAll",command=delete_all_student_records,height=1,width=8,bg='red',fg="black",font=label_font).place(x=380,y=300)
Button(root,text="ShowAll",command=show,height=1,width=8,bg='black',fg="white",font=label_font).place(x=490,y=300)

#treeview for displaying student data
cols = ("rollno","name","gender","age","department","program","year","mobile","email")
listbox = ttk.Treeview(root,columns=cols,show="headings",height=10)
listbox.place(x=20,y=380)
listbox.heading("rollno",text="Roll.no")
listbox.heading("name",text="Name")
listbox.heading("gender",text="Gender")
listbox.heading("age",text="Age")
listbox.heading("department",text="Department")
listbox.heading("program",text="Program")
listbox.heading("year",text="Year of study")
listbox.heading("mobile",text="Mobile")
listbox.heading("email",text="Email")
# treeview column setting
listbox.column("rollno", width=75) 
listbox.column("name", width=110) 
listbox.column("gender", width=75) 
listbox.column("age", width=50)
listbox.column("department", width=115)
listbox.column("program", width=90)
listbox.column("year", width=90)
listbox.column("mobile", width=100)
listbox.column("email", width=125)
#scrollbar for the treeview
scrollbar = Scrollbar(root,orient='vertical',command=listbox.yview)
scrollbar.place(x=880,y=380,height=250)
listbox.configure(yscrollcommand=scrollbar.set)
# binding the selected ones 
listbox.bind("<ButtonRelease-1>",select_row)
# start the GUI main loop
root.mainloop()