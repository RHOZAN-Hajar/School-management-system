from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from hhhhh import Evaluation_elv
from time import strftime
import mysql.connector

class LoginPage:
    def __init__(self, root,users):
        self.root = root
        self.users=users
        self.root.title("Login Page")
        self.root.geometry('750x518')

        # Username Label and Entry
        self.label_username = Label(root, text="Username:", font=("goudy old style", 25, "bold"), bg='white',fg='black')
        self.label_username.place(x=200, y=100, width=400, height=50)
        self.entry_username = Entry(root,font=("goudy old style", 25, "bold"))
        self.entry_username.place(x=200, y=190, width=400, height=50)

        # Password Label and Entry
        self.label_password = Label(root, text="Password:", font=("goudy old style", 25, "bold"), bg='white',
                                       fg='black')
        self.label_password.place(x=200, y=280, width=400, height=50)
        self.entry_password = Entry(root, show="*",bg='white', fg='black', font=("goudy old style", 25, "bold"))
        self.entry_password.place(x=200, y=370, width=400, height=50)

        # Login Button
        self.button_login = Button(root, text="Login", command=self.login,font=("goudy old style", 25, "bold"),bg='white', fg='black')
        self.button_login.place(x=350, y=440, width=100, height=35)

        self.student_id = None

    def login(self):
     

        entered_username = self.entry_username.get()
        entered_password = self.entry_password.get()

        if entered_username in self.users and self.users[entered_username] == entered_password:
            messagebox.showinfo("Login Successful", "Welcome, " + entered_username + "!")
            # Store correct_username in student_id
            self.student_id = entered_username
            # Destroy the login window
            self.root.destroy()
            # Open the main interface directly
            self.open_main_interface()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def open_main_interface(self):
        # Pass the student_id to the MainInterface
        main_interface = MainInterface(self.student_id)
        main_interface.mainloop()

class MainInterface(Tk):
    def __init__(self, student_id):
        super().__init__()
        self.geometry("1350x700+0+0")
        self.student_id = student_id 
        self.resizable(False, False)
        self.title("Espace Eleve ")
        self.config(bg='#C3E2C2')

        nouvelle_taille = (100, 100)

        self.label = Label(self, text="ESPACE  SINDIBAD",
                           font=('goudy old style', 45, 'bold'),
                           fg='white',
                           bg='#4F6F52',

                           relief=RAISED,  
                           bd=5, 
                           padx=500,  
                           pady=500,
                           anchor='w',
                           compound=LEFT)
        self.label.place(x=0, y=0, relwidth=1, height=70)
        self.logout = Button(self, text='Se deconnecter',command=self.quit)
        self.logout.place(x=1190, y=15, height=40, width=150)





        

        self.evaluation = Button(self, text="Evaluations",  command=self.Evaluation_elv, compound=LEFT,font=('goudy old style', 14, 'bold'),width=30,anchor="center", justify=CENTER)
        self.evaluation.place(x=600,y=400)

        # +++FOOTER+++
        self.footer_label = Label(self, text="Tous Les Droits Sont  Réservés", bg='#739072', height=1,
                                  font=('Arial', 10, 'bold'))
        self.footer_label.pack(side=BOTTOM, fill=X)

        #self.l1 = Label(self, bg="#C3E2C2")
        #self.l1.place(x=900, y=400)

        # Créez les widgets pour l'heure, le jour et la date une seule fois
        self.time_label = Label(self, font=("Arial", 50), fg="#00ff00", bg="black")
        self.time_label.place(x=570, y=100)

        self.day_label = Label(self, font=("Ink Free", 25), bg="#C3E2C2")
        self.day_label.place(x=700, y=182)

        self.date_label = Label(self, font=("Ink Free", 35), bg="#C3E2C2")
        self.date_label.place(x=560, y=229)

        
        self.my_time()

    def my_time(self):
        # Mettez à jour les widgets avec la nouvelle heure, jour et date
        time_string = strftime("%I:%M:%S %p")
        self.time_label.config(text=time_string)

        day_string = strftime("%A")
        self.day_label.config(text=day_string)

        date_string = strftime("%B %d ,%Y")
        self.date_label.config(text=date_string)




        # Planifiez la prochaine mise à jour dans 1000 millisecondes (1 seconde)
        self.after(1000, self.my_time)




    def Evaluation_elv(self):
        self.evaluation_window = Toplevel(self)
        # Pass the student_id to the Evaluation_elv
        self.new_objet2 = Evaluation_elv(self.evaluation_window, self.student_id)
if __name__ == "__main__":
    # User data with 10 users
    users_data = {
        "mm": "11",
        "oo": "22",
        "ooo": "33",
        "user4": "password4",
        "user5": "password5",
        "user6": "password6",
        "user7": "password7",
        "user8": "password8",
        "user9": "password9",
        "user10": "password10",
    }

    login_root = Tk()
    login_app = LoginPage(login_root, users_data)
    login_root.mainloop()