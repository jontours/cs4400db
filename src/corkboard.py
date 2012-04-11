#Geoffrey Horton
#gthorton13@gatech.edu
#"I worked on the homework assignment alone, using only this semester's 
#course materials.

import urllib.request
from tkinter import *
import base64
import pymysql


class myGUI:

    #Starts the process by calling the LoginPage method.
    def __init__(self):
        self.LoginPage()

    #Connects to the database. Messagebox will appear if error occurs. Returns the
    #database connection object if no error is found.
    def Connect(self):
        try:
            db = pymysql.connect(host = 'academic-mysql.cc.gatech.edu', passwd = 'q8tRegu5', user = 'cs2316', db='cs2316db')
            return db
        except:
            messagebox.showwarning('Error', 'Please check your internet connection')





    #Helper method that destroys the LoginPage GUI & calls register method.
    def destroyer1(self):
        self.win.destroy()
        self.win2=Tk()
        self.register()

    #Helper method that destroys the LoginPage GUI & calls LoginCheck method.
    def destroyer2(self):
        self.usern1 = self.E1.get()
        self.passw1 = self.E2.get()
        self.LoginCheck()

    #Helper method that destroys the register GUI & calls LoginPage method.
    def destroyer3(self):      
        self.win2.destroy()
        self.LoginPage()

    #Helper method that gets all of the registration info and call RegisterNew method.
    def destroyer4(self):
        self.firstn = self.E1.get()
        self.usern = self.E2.get()
        self.passw = self.E3.get()
        self.confpass = self.E4.get()
        self.RegisterNew()

    #Helper method that destroys register GUI & calls LoginPage method.
    def destroyer5(self):
        self.win2.destroy()
        self.LoginPage()

    #Helper method that checks to see if a Username already exsists in the database.
    def helper1(self,name):
        #A try statement will be used to see if data can actually be retrieved. 
       # try:
            #The connect method will be called to connect to the database. It
            #will then retrieve the first name and password of the provided username.
            db = self.Connect()
            cursor = db.cursor()
            sql = "SELECT FirstName,Password FROM User WHERE Username= %s"
            cursor.execute(sql, (name))
            cursor.close()
            db.commit()
            
            #Goes through every username checking to see if it is the same. Also
            #records the person's name and password.Returns False if the username is found,
            #returns True if it is not found.
            self.person=''
            for person in cursor:
                if person[0] == name:
                    self.person = person[0]
                    
                self.password = person[1]
                return False
            else:
                return True



            
    #Checks to see if info passed into login page is currently in database.
    def LoginCheck(self):
        answer = self.helper1(self.usern1)
        if answer==True:
            messagebox.showwarning('Error', 'You entered an unrecognizable username/password combination')
        else:
            #Tests to see if the passwords are the same.
            if self.password == self.passw1:
                messagebox.showwarning('Success', ' You logged in successfully!')
                self.win.destroy()

            else:
                messagebox.showwarning('Error', 'You entered an unrecognizable username/password combination')



        
    #Will take entries from register page and enter them into the database.
    def RegisterNew(self):

        #Checks to see if a Username is entered.
        if len(self.usern)==0:
            messagebox.showwarning('Error', 'Please enter a Username')
        else:
            answer = self.helper1(self.usern)
            
            #Checks if a password is entered.
            if len(self.passw)==0:
                messagebox.showwarning('Error', 'Please enter a Password')
                
            #Checks if the passwords entered are the same.
            elif self.passw != self.confpass:
                messagebox.showwarning('Error', 'The Passwords you entered do not match')
                
            #Checks to see if the username already exsists in the database.
            elif answer==False:
                messagebox.showwarning('Error', 'This username already exsists in the database')

            #Add the user's Username, Name, and Password into the database.
            else:
                db = self.Connect()
                cursor = db.cursor()

                #If the First Name is left blank, NULL will be used instead.
                if self.firstn == '':
                    sql = "INSERT INTO User (Username,Password) VALUES (%s,%s)"
                    cursor.execute(sql, (self.usern,self.passw))

                else:
                    sql = "INSERT INTO User (Username,FirstName,Password) VALUES (%s,%s,%s)"
                    cursor.execute(sql, (self.usern,self.firstn,self.passw))

                cursor.close()
                db.commit()

                #Notfies the user that they have been registered. Then calls another helper method.
                messagebox.showwarning('Success', 'You are now registered!')
                self.destroyer5()



    

    #Creates the first GUI that will allow the user to sign in or register. 
    def LoginPage(self):
        #Creates the GUI window. Adds a title and changes background color.
        win = Tk()
        win.title('Login')
        win.config(bg='white')

        #Downloads GT Buzz picture and places it in GUI window.
        URL = "http://th965.photobucket.com/albums/ae134/wgyouree/th_gatech_buzz.gif"
        u = urllib.request.urlopen(URL)
        raw_data = u.read()
        u.close()
        self.rawdata = raw_data
        newdata = base64.encodebytes(raw_data)
        gt_pic = PhotoImage(data=newdata)
        self.L1 = Label(win,image=gt_pic,bg='white')
        self.L1.image = gt_pic
        self.L1.grid(row=0,column=0,columnspan=2,sticky=NE)

        #Username label.
        self.L2 = Label(win,text='Username',bg='white')
        self.L2.grid(row=2,column=0,sticky=E)

        #Password label.
        self.L3 = Label(win,text='Password',bg='white')
        self.L3.grid(row=3,column=0,sticky=E)

        #Empty label for spacing purposes.
        self.L4 = Label(win,text='',bg='white')
        self.L4.grid(row=4,column=0)

        #Empty label for spacing purposes.
        self.L5 = Label(win,text='',bg='white')
        self.L5.grid(row=1,column=0)

        #Entry box for the Username.
        self.E1 = Entry(win,width=30)
        self.E1.grid(row=2,column=1)

        #Entry box for the Password.
        self.E2 = Entry(win,width=30)
        self.E2.grid(row=3,column=1)

        #Button for the Logining in.
        self.B1 = Button(win,text='Login',command=self.destroyer2,width=8)
        self.B1.grid(row=5,column=2)

        #Button for the Registering.
        self.B2 = Button(win,text='Register',command=self.destroyer1,width=8)
        self.B2.grid(row=5,column=1,sticky=E)

        #Create instance of win so it can be destroyed later.
        self.win = win
        win.mainloop()




    #Creates a GUI that will allow the user to input info for registering.   
    def register(self):
        #Creates the GUI window. Adds a title and changes background color.
        win2 = self.win2
        win2.title('GtChat New User Registration')
        win2.config(bg='white')

        #Using instance from first GUI, inserts GT Buzz pic into GUI.
        newdata = base64.encodebytes(self.rawdata)
        gt_pic = PhotoImage(data=newdata)
        self.L1 = Label(win2,image=gt_pic,bg='white')
        self.L1.image = gt_pic
        self.L1.grid(row=0,column=0,columnspan=2,sticky=NE)

        #First Name label.
        self.L2 = Label(win2,text='First Name',bg='white')
        self.L2.grid(row=2,column=0,sticky=W)

        #Username label.
        self.L3 = Label(win2,text='Username',bg='white')
        self.L3.grid(row=3,column=0,sticky=W)

        #Password label.
        self.L4 = Label(win2,text='Password',bg='white')
        self.L4.grid(row=4,column=0,sticky=W)

        #Confirm Password label.
        self.L5 = Label(win2,text='Confirm Password',bg='white')
        self.L5.grid(row=5,column=0,sticky=W)

        #Empty label for spacing pursposes.
        self.L6 = Label(win2,text='',bg='white')
        self.L6.grid(row=6,column=0)

        #Entry for First Name.
        self.E1 = Entry(win2,width=30)
        self.E1.grid(row=2,column=1)

        #Entry for Username.
        self.E2 = Entry(win2,width=30)
        self.E2.grid(row=3,column=1)

        #Entry for Password.
        self.E3 = Entry(win2,width=30)
        self.E3.grid(row=4,column=1)

        #Entry for Confirm Password.
        self.E4 = Entry(win2,width=30)
        self.E4.grid(row=5,column=1)

        #Button for Canceling the process.
        self.B1 = Button(win2,text='Cancel',command=self.destroyer3,width=8)
        self.B1.grid(row=7,column=1,sticky=E)

        #Button for finalizing registration.
        self.B2 = Button(win2,text='Register',command=self.destroyer4,width=8)
        self.B2.grid(row=7,column=2,sticky=E)

        #Mainloop for th GUI.
        self.win2.mainloop()
    
app = myGUI()
