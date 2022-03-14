#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
import os
import re

master = Tk()
master.title('Banking App')
master.config(bg="light gray")
master.geometry("300x300")

#Functions
def finish_reg():
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    contact_no = temp_contact_no.get()
    email = temp_email.get()
    password = temp_password.get()
    all_accounts = os.listdir()

    if name == "" or age == "" or gender == "" or password == "":
        notif.config(fg="red",text="All fields requried * ")
        return

    for name_check in all_accounts:
        if name == name_check:
            notif.config(fg="red",text="Account already exists")
            return
        else:
            new_file = open(name,"w")
            new_file.write(name+'\n')
            new_file.write(email+'\n')
            new_file.write(password+'\n')
            new_file.write(age+'\n')
            new_file.write(gender+'\n')
            new_file.write('0')
            new_file.close()
            notif.config(fg="green", text="Account has been created")

def register():
    #Vars
    global temp_name
    global temp_age
    global temp_gender
    global temp_email
    global temp_password
    global notif
    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_email = StringVar()
    temp_password = StringVar()

    #Register Screen
    register_screen = Toplevel(master)
    register_screen.title('Register')
    register_screen.config(bg="light gray")
    register_screen.geometry("300x300")

    #Labels
    Label(register_screen,bg="light gray", text="Please enter your details below to register", font=('Arial',12)).grid(row=0,sticky=N,pady=10)
    Label(register_screen,bg="light gray", text="Name", font=('Arial',12)).grid(row=1,sticky=W)
    Label(register_screen,bg="light gray" ,text="Age", font=('Arial',12)).grid(row=2,sticky=W)
    Label(register_screen,bg="light gray", text="Gender", font=('Arial',12)).grid(row=3,sticky=W)
    Label(register_screen,bg="light gray", text="Email", font=('Arial',12)).grid(row=5,sticky=W)
    Label(register_screen,bg="light gray", text="Password", font=('Arial',12)).grid(row=6,sticky=W)
    notif = Label(register_screen, bg="light gray", font=('Arial',12))
    notif.grid(row=8,sticky=N,pady=10)

    #Entries
    Entry(register_screen,textvariable=temp_name).grid(row=1,column=0)
    Entry(register_screen,textvariable=temp_age).grid(row=2,column=0)
    Entry(register_screen,textvariable=temp_gender).grid(row=3,column=0)
    Entry(register_screen,textvariable=temp_email).grid(row=5,column=0)
    Entry(register_screen,textvariable=temp_password,show="*").grid(row=6,column=0)

    #Buttons
    Button(register_screen, text="Register",bg="light cyan",command = finish_reg, font=('Arial',12)).grid(row=7,sticky=N,pady=10)

def login_session():
    global login_name
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name,"r")
            file_data = file.read()
            file_data = file_data.split('\n')
            password  = login_password

            #Account Dashboard
            if login_password == password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')
                account_dashboard.config(bg="light gray")

                #Labels
                Label(account_dashboard,bg="light gray",text="Account Dashboard", font=('Arial',12)).grid(row=0,sticky=N,pady=10)
                Label(account_dashboard,bg="light gray",text="Welcome "+name, font=('Arial',12)).grid(row=1,sticky=N,pady=5)

                #Buttons
                Button(account_dashboard, text="Personal Details",font=('Arial',12),width=30,bg="light cyan",command=personal_details).grid(row=2,sticky=N,padx=10)
                Button(account_dashboard, text="Deposit",font=('Arial',12),width=30,bg="light cyan",command=deposit).grid(row=3,sticky=N,padx=10)
                Button(account_dashboard, text="Withdraw",font=('Arial',12),width=30,bg="light cyan",command=withdraw).grid(row=4,sticky=N,padx=10)
                Label(account_dashboard).grid(row=5,sticky=N,pady=10)
                return
            else:
                login_notif.config(fg="red",bg="light gray", text="Password incorrect!!")
                return
    login_notif.config(fg="red",bg="light gray",text="No account found !!")

def deposit():
    #Vars
    global amount
    global deposit_notif
    global current_balance_label
    amount = StringVar()
    file   = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]

    #Deposit Screen
    deposit_screen = Toplevel(master)
    deposit_screen.title('Deposit')
    deposit_screen.config(bg="light gray")
    deposit_screen.geometry("300x300")

    #Label
    Label(deposit_screen,bg="light gray", text="Deposit", font=('Arial',12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(deposit_screen,bg="light gray", text="Current Balance : R"+details_balance, font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(deposit_screen,bg="light gray", text="Amount : ", font=('Arial',12)).grid(row=2,sticky=W)
    deposit_notif = Label(deposit_screen,bg="light gray",font=('Arial',12))
    deposit_notif.grid(row=4, sticky=N,pady=5)

    #Entry
    Entry(deposit_screen, textvariable=amount).grid(row=2,column=1)

    #Button
    Button(deposit_screen,text="Finish",font=('Arial',12),bg="light cyan",command=finish_deposit).grid(row=3,sticky=W,pady=5)

def finish_deposit():

    if amount.get() == "":
        deposit_notif.config(bg="light gray",text='Amount is required!',fg="red")
        return
    if float(amount.get()) <=0:
        deposit_notif.config(bg="light gray",text='Negative currency is not accepted', fg='red')
        return

    file = open(login_name, 'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())
    file_data       = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_label.config(text="Current Balance : R"+str(updated_balance),fg="green")
    deposit_notif.config(bg="light gray",text='Balance Updated', fg='green')

def withdraw():
     #Vars
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    withdraw_amount = StringVar()
    file   = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]

    #Deposit Screen
    withdraw_screen = Toplevel(master)
    withdraw_screen.title('Withdraw')
    withdraw_screen.config(bg="light gray")
    withdraw_screen.geometry("300x300")

    #Label
    Label(withdraw_screen,bg="light gray", text="Balance", font=('Arial',12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(withdraw_screen,bg="light gray", text="Current Balance : R"+details_balance, font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(withdraw_screen,bg="light gray", text="Amount : ", font=('Arial',12)).grid(row=2,sticky=W)
    withdraw_notif = Label(withdraw_screen,bg="light gray",font=('Arial',12))
    withdraw_notif.grid(row=4, sticky=N,pady=5)

    #Entry
    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2,column=1)

    #Button
    Button(withdraw_screen,text="Finish",font=('Arial',12),bg="light cyan",command=finish_withdraw).grid(row=3,sticky=W,pady=5)

def finish_withdraw():
    if withdraw_amount.get() == "":
        withdraw_notif.config(bg="light gray",text='Amount is required!',fg="red")
        return
    if float(withdraw_amount.get()) <=0:
        withdraw_notif.config(bg="light gray",text='Negative currency is not accepted', fg='red')
        return

    file = open(login_name, 'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[6]

    if float(withdraw_amount.get()) >float(current_balance):
        withdraw_notif.config(bg="light gray",text='Insufficient Funds!', fg='red')
        return

    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(withdraw_amount.get())
    file_data       = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_label.config(bg="light gray",text="Current Balance : R"+str(updated_balance),fg="green")
    withdraw_notif.config(bg="light gray",text='Balance Updated', fg='green')


def personal_details():
    #Vars
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_name = user_details[0]
    details_email= user_details[1]
    details_age = user_details[2]
    details_gender = user_details[3]
    details_balance = user_details[4]

    #Personal details screen
    personal_details_screen = Toplevel(master)
    personal_details_screen.title('Personal Details')
    personal_details_screen.config(bg="light gray")
    personal_details_screen.geometry("300x300")

    #Labels
    Label(personal_details_screen,bg="light gray", text="Personal Details", font=('Arial',12)).grid(row=0,sticky=N,pady=10)
    Label(personal_details_screen,bg="light gray", text="Name : "+details_name, font=('Arial',12)).grid(row=1,sticky=W)
    Label(personal_details_screen,bg="light gray", text="Age : "+details_age, font=('Arial',12)).grid(row=2,sticky=W)
    Label(personal_details_screen,bg="light gray", text="Email : "+details_email, font=('Arial',12)).grid(row=4,sticky=W)
    Label(personal_details_screen,bg="light gray", text="Gender : "+details_gender, font=('Arial',12)).grid(row=5,sticky=W)
    Label(personal_details_screen,bg="light gray", text="Balance :R"+details_balance, font=('Arial',12)).grid(row=6,sticky=W)

def login():
    #Vars
    global temp_login_name
    global temp_login_password
    global login_notif
    global login_screen
    temp_login_name = StringVar()
    temp_login_password = StringVar()

    #Login Screen
    login_screen = Toplevel(master)
    login_screen.title('Login')
    login_screen.config(bg="light gray")
    login_screen.geometry("300x250")

    #Labels
    Label(login_screen,bg="light gray", text="Login to your account", font=('Arial',12)).grid(row=0,sticky=N,pady=10)
    Label(login_screen,bg="light gray", text="Username", font=('Arial',12)).grid(row=1,sticky=W)
    Label(login_screen,bg="light gray", text="Password", font=('Arial',12)).grid(row=2,sticky=W)
    login_notif = Label(login_screen,bg="light gray", font=('Arial',12))
    login_notif.grid(row=4,sticky=N)

    #Entry
    Entry(login_screen, textvariable=temp_login_name).grid(row=1,column=1,padx=5)
    Entry(login_screen, textvariable=temp_login_password,show="*").grid(row=2,column=1,padx=5)

    #Button
    Button(login_screen, text="Login",bg="light cyan", command=login_session, width=15,font=('Arial',12)).grid(row=3,sticky=W,pady=5,padx=5)

#Labels
Label(master,bg="light gray", text = "Sanda's Bank App", fg="white", font=('verdana bold',18)).grid(row=0,sticky=N,pady=10)
Label(master,bg="light gray", text = "Most secure bank to use!", fg="white", font=('Comic Sans MS italic',16)).grid(row=1,sticky=N)


#Buttons
Button(master, text="Register", font=('Arial',12),width=20,bg="light cyan",command=register).grid(row=3,sticky=N)
Button(master, text="Login", font=('Arial',12),width=20,bg="light cyan",command=login).grid(row=4,sticky=N,pady=10)

master.mainloop()

