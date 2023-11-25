from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error','Fields cannot be empty')
    elif usernameEntry.get() == 'Prachi' and passwordEntry.get() == '12345':
        messagebox.showinfo('Success','Welcome')
        window.destroy()
        import sms


    else:
        messagebox.showerror('Error','Please enter correct cordential')


window = Tk()

window.geometry('1530x900+0+0')

window.resizable(False,False)

window.title('Login')
#
# backgroundImage = ImageTk.PhotoImage(file='bgImg.jpg')
#
# bglabel = Label(window,image=backgroundImage)
#
# bglabel.place(x=0,y=0)

loginFrame = Frame(window,bg='white')

loginFrame.place(x=500,y=250)

logoImage = PhotoImage(file='logo.png')

logoLabel = Label(loginFrame,image=logoImage)

logoLabel.grid(row=0,column=0,columnspan=2,pady=10)

usernameImage = PhotoImage(file='user.png')
usernameLabel = Label(loginFrame,image=usernameImage,text='Username',compound=LEFT
                      ,font=('times new roman',20,'bold'),bg='white')
usernameLabel.grid(row=1,column=0,pady=10)

usernameEntry = Entry(loginFrame,font=('times new roman',20,'bold'),bd=5,fg='royalblue')
usernameEntry.grid(row=1,column=1,pady=10,padx=20)



passwordImage = PhotoImage(file='password.png')
passwordLabel = Label(loginFrame,image=passwordImage,text='Password',compound=LEFT
                      ,font=('times new roman',20,'bold'),bg='white')
passwordLabel.grid(row=2,column=0,pady=10)

passwordEntry = Entry(loginFrame,font=('times new roman',20,'bold'),bd=5,fg='royalblue')
passwordEntry.grid(row=2,column=1,pady=10,padx=20)


loginButton = Button(loginFrame,text='Login',font=('times new roman',14,'bold')
                     ,width=15,bg='cornflowerblue',fg='white',activebackground='cornflowerblue',
                     activeforeground='white',cursor='hand2',command=login)
loginButton.grid(row=3,column=1,pady=10,)

window.mainloop()