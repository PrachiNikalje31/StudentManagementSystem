from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas as pd
# Functionality part

def toplevel_data(title,button_text,command):
    global idEntry,nameEntry,phoneEntry,emailEntry,addressEntry,genderEntry,dobEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, padx=10, pady=15)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'))
    nameEntry.grid(row=1, column=1, padx=10, pady=15)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'))
    phoneEntry.grid(row=2, column=1, padx=10, pady=15)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'))
    emailEntry.grid(row=3, column=1, padx=10, pady=15)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'))
    addressEntry.grid(row=4, column=1, padx=10, pady=15)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'))
    genderEntry.grid(row=5, column=1, padx=10, pady=15)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'))
    dobEntry.grid(row=6, column=1, padx=10, pady=15)

    update_student_button = ttk.Button(screen, text=button_text, command=command)
    update_student_button.grid(row=7, columnspan=2, pady=15)

    if title=='Update Student':
        indexing = studentTable.focus()
        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])

def iexit():
    result = messagebox.askyesno('Confirm','Do you want to exit')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist=[]
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pd.DataFrame(newlist,columns=['ID','Name','Mobile No','Email','Address','Gender','DOB'])
    print(table)
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved succesfully')
def update_data():
    Query = 'update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s where id=%s'
    mycursor.execute(Query,(nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),
                            genderEntry.get(),dobEntry.get(),idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'ID {idEntry.get()} is modified successfully',parent=screen)
    screen.destroy()
    show_student()

def show_student():
    Query = 'select * from student'
    mycursor.execute(Query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def delete_student():
    indexing = studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id = content['values'][0]
    Query = 'delete from student where id=%s'
    mycursor.execute(Query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'This {content_id} is deleted succesfully')
    Query = 'select * from student'
    mycursor.execute(Query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def search_data():
    Query = 'select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(Query,(idEntry.get(),nameEntry.get(),emailEntry.get(),phoneEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def add_data():
    if idEntry.get() =='' or nameEntry.get()=='' or phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()=='':
        messagebox.showerror('Error','All Fields are required',parent=screen)
    else:
        try:
            Query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(Query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))

            con.commit()
            result=messagebox.askyesno('Comfirm','Data added successfully, Do you want to clean the form?',parent=screen)

            if result:
                idEntry.delete(0,END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error','Id cannot be duplicate',parent=screen)
            return

        Query='select * from student'
        mycursor.execute(Query)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('',END,values=data)

def connect_database():
    def connect():
        global mycursor, con
        try:
            #con = pymysql.connect(host='localhost',user='root',password='Prachi@1131')
            con = pymysql.connect(host=hostEntry.get(),user=userEntry.get(),password=passwordEntry.get())
            mycursor = con.cursor()

        except:
            messagebox.showerror('Error','Invalid Details',parent=connectWindow)
            return

        try:
            Query = 'create database studentmanagementsystem'
            mycursor.execute(Query)

            Query = 'use studentmanagementsystem'
            mycursor.execute(Query)

            Query = 'create table student (id int not null primary key , name varchar(30),mobile varchar(10),email varchar(30),address varchar(100),gender varchar(20),dob varchar(50))'
            mycursor.execute(Query)

        except:
            Query = 'use studentmanagementsystem'
            mycursor.execute(Query)

        messagebox.showinfo('Success', 'Database Connection is Successful', parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+1040+150')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    hostnameLabel = Label(connectWindow,text='Host Name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0)

    hostEntry = Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0)

    userEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    userEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)

count = 0
text = ''
def slider():
    global text,count
    if count == len(s):
        count = 0
        text = ''
    text = text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)

def clock():
    date = time.strftime('%d/%m/%Y')
    curTime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {curTime}')
    datetimeLabel.after(1000,clock)



# GUI part

root = ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('radiance')

root.geometry('1517x780+0+0')
root.resizable(0,0)
root.title('Student Management System')

datetimeLabel = Label(root,font=('times new roman',18,'bold'),fg='Indianred4')
datetimeLabel.place(x=5,y=5)
clock()

s = 'Student Management System'
sliderLabel = Label(root,font=('arial',30,'italic bold'),fg='red4',width = 30)
sliderLabel.place(x=600,y=0)
slider()

connectButton = ttk.Button(root,text='Connect Database',command=connect_database)
connectButton.place(x=1300,y=0)

leftFrame = Frame(root)
leftFrame.place(x=50,y=80,width=300,height=670)

logo_image = PhotoImage(file='stud_Img.png')
logo_Label = Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)

addstudentButton = ttk.Button(leftFrame,text='Add Student',width=25,state=DISABLED,command=lambda :toplevel_data('Add Student','Add',add_data))
addstudentButton.grid(row=1,column=0,pady=20)

searchstudentButton = ttk.Button(leftFrame,text='Search Student',width=25,state=DISABLED,command=lambda :toplevel_data('Search Student','Search',search_data))
searchstudentButton.grid(row=2,column=0,pady=20)

deletestudentButton = ttk.Button(leftFrame,text='Delete Student',width=25,state=DISABLED,command=delete_student)
deletestudentButton.grid(row=3,column=0,pady=20)

updatestudentButton = ttk.Button(leftFrame,text='Update Student',width=25,state=DISABLED,command=lambda :toplevel_data('Update Student','Updata',update_data))
updatestudentButton.grid(row=4,column=0,pady=20)

showstudentButton = ttk.Button(leftFrame,text='Show Student',width=25,state=DISABLED,command=show_student)
showstudentButton.grid(row=5,column=0,pady=20)

exportstudentButton = ttk.Button(leftFrame,text='Export Student',width=25,state=DISABLED,command=export_data)
exportstudentButton.grid(row=6,column=0,pady=20)

exitButton = ttk.Button(leftFrame,text='Exit Student',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350,y=80,width=1150,height=670)

scrollBarX = Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame,orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame,columns=('ID','Name','Mobile No.','Email address','Address','Gender','D.O.B')
                            ,xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)
scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('ID',text='Roll No')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile No.',text='Mobile No.')
studentTable.heading('Email address',text='Email address')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')

studentTable.column('ID',width=100,anchor=CENTER)
studentTable.column('Name',width=300,anchor=CENTER)
studentTable.column('Mobile No.',width=300,anchor=CENTER)
studentTable.column('Email address',width=200,anchor=CENTER)
studentTable.column('Address',width=300,anchor=CENTER)
studentTable.column('Gender',width=100,anchor=CENTER)
studentTable.column('D.O.B',width=100,anchor=CENTER)

style = ttk.Style()
style.configure('Treeview',rowheight=40,font=('arial',12,'bold'),background='white')
style.configure('Treeview.Heading',font=('arial',14,'bold'))
studentTable.config(show='headings')

root.mainloop()