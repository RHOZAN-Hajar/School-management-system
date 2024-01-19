from tkinter import *
from main_elv import LoginPage
from projet import LoginAdmin


class Main_Interface:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1350x700+0+0")
        self.window.title("Welcome to gestion school ")
        self.window.config(bg='#C3E2C2')

        self.label = Label(self.window, text="ESPACE SINDIBAD",
                           font=('goudy old style', 45, 'bold'),
                           fg='white',
                           bg='#4F6F52',
                           relief=RAISED,
                           bd=5,
                           padx=500,
                           pady=500,
                           anchor='w',
                           compound=LEFT)
        self.label.place(x=0, y=0, relwidth=1, height=80)
        self.logout = Button(self.window, text='Se deconnecter', command=self.window.destroy)
        self.logout.place(x=1190, y=15, height=40, width=150)

        self.button1 = Button(self.window, text="Administration",command=self.open_admin_login, bg="#304D30", fg="white",
                              font=("goudy old style", 14, "bold"))
        self.button1.place(x=500, y=295, width=400)

        self.button2 = Button(self.window, text="Eleve", bg="#304D30", fg="white",
                              font=("goudy old style", 14, "bold"), command=self.open_eleve_login)
        self.button2.place(x=500, y=350, width=400)

    def open_eleve_login(self):
        # Pass the users data to the LoginPage
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

        login_window = Toplevel(self.window)
        login_eleve = LoginPage(login_window, users_data)


    def open_admin_login(self):

     login_admin_window = Toplevel(self.window)
     login_admin = LoginAdmin(login_admin_window)
     login_admin_window.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = Main_Interface(root)
    root.mainloop()
