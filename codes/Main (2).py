import hashlib
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from time import strftime
from ELEVE import Students
from PROF import Professeur
from CLASSE import Classes
from PAIEMENT import Paiement
from EVALUATION import Evaluation
from ABS_ELV import Abscence_elv
from ABS_PR import Abscence

class LoginAdmin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry('390x500+560+200')
        self.root.resizable(False, False)

        # image
        bg_frame = Image.open('sindibad.jpeg')
        self.photo = ImageTk.PhotoImage(bg_frame)
        bg_panel = tk.Label(self.root, image=self.photo)
        bg_panel.image = self.photo
        bg_panel.place(relwidth=1.0, relheight=1.0)

        # Username Label and Entry
        self.label_username = tk.Label(root, text="Username:",font=('goudy old style',25,'bold'),bg="white",fg="black" )
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(root,font=('goudy old style',25,'bold'),bg="white",fg="black")
        self.entry_username.pack(pady=10)

        # Password Label and Entry
        self.label_password = tk.Label(root, text="Password:",font=('goudy old style',25,'bold'),bg="white",fg="black")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(root, show="*",font=('goudy old style',25,'bold'),bg="white",fg="black")
        self.entry_password.pack(pady=10)

        # Login Button
        self.button_login = tk.Button(root, text="Login", command=self.login,font=('goudy old style',25,'bold'),bg="white",fg="black")
        self.button_login.pack(pady=20)

    def login(self):
        #Replace these with your actual username and password
        username = self.entry_username.get()
        password = self.entry_password.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        username1 = "root"
        password1 = "123"

        hashed_password1 =hashlib.sha256(password1.encode()).hexdigest()




        if hashed_password  == hashed_password1 and username == username1:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            # Destroy the login window
            self.root.destroy()
            # Open the main interface directly
            self.open_main_interface()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def open_main_interface(self):
        main_interface = MainInterface()
        main_interface.mainloop()


class MainInterface(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1350x690+100+100")
        self.resizable(False, False)
        self.title("Espace Administrateur ")
        self.config(bg='#C3E2C2')

        nouvelle_taille = (100, 100)

        self.label = Label(self, text="ESPACE SINDIBAD",
                           font=('goudy old style', 45, 'bold'),
                           fg='white',
                           bg='#4F6F52',
                           relief=RAISED,  # ca pour un etre 3d bhal hayt
                           bd=5,  # la taill dyal hayt
                           padx=500,  # ce pad comme margin
                           pady=500,
                           anchor='w',
                           compound=LEFT)
        self.label.place(x=0, y=0, relwidth=1, height=80)
        self.logout = Button(self, text='Se deconnecter', command=self.quit)
        self.logout.place(x=1190, y=15, height=40, width=150)

        # blasa les menu
        self.fram = Frame(self, bd=2, relief=RIDGE)
        self.fram.place(x=0, y=83, width=200, height=600)
        # ====resise image===
        ########################################################

        self.original = Image.open("sindibad.jpeg")
        nouvelle_taille = (200, 95)
        dimonss = self.original.resize(nouvelle_taille)
        self.pho = ImageTk.PhotoImage(dimonss)

        self.fram_photo = Label(self.fram, image=self.pho)
        self.fram_photo.pack(side=TOP, fill=X)
        ##########################################################

        self.menu = Label(self.fram, text="Menu", bg='#739072', fg='white', height=1, font=('Arial', 23, 'bold'))
        self.menu.pack(side=TOP, fill=X)


        self.eleves = Button(self.fram, text="Eleves", bd=2, command=self.students, compound=LEFT, padx=30, anchor='w',height=2, font=('goudy old style', 14, 'bold'))
        self.eleves.pack(side=TOP, fill=X)

        # botona dyal prof
        self.professeur = Button(self.fram, text="Professeur",command=self.prof, bd=2, compound=LEFT, padx=30, anchor='w', height=2, font=('goudy old style', 14, 'bold'))
        self.professeur.pack(side=TOP, fill=X)
        # botona dyal classes
        self.classes = Button(self.fram, text="Classes", bd=2, command=self.classe,compound=LEFT, padx=30, anchor='w', height=2, font=('goudy old style', 14, 'bold'))
        self.classes.pack(side=TOP, fill=X)
        # botona dyal payment
        self.payment = Button(self.fram, text="Evaluation", bd=2,command=self.evaluation, compound=LEFT, padx=30, anchor='w', height=2, font=('goudy old style', 14, 'bold'))
        self.payment.pack(side=TOP, fill=X)
        self.payment = Button(self.fram, text="Paiement", bd=2, compound=LEFT,command=self.paiemant,font=('goudy old style', 14, 'bold'),
                              padx=30, anchor='w', height=2)
        self.payment.pack(side=TOP, fill=X)
        self.payment = Button(self.fram, text="Absence eleves", bd=2, compound=LEFT,command=self.abssence_elv,
                              padx=30, anchor='w', height=2, font=('goudy old style', 14, 'bold'))
        self.payment.pack(side=TOP, fill=X)
        self.payment = Button(self.fram, text="Absence professeur", bd=2, compound=LEFT,command=self.abssences_pr,
                              padx=30, anchor='w', height=2, font=('goudy old style', 14, 'bold'))
        self.payment.pack(side=TOP, fill=X)
        # +++FOOTER+++
        self.footer_label = Label(self, text="Tous Les Droits Sont  Réservés", bg='#739072', height=1,
                                  font=('Arial', 10, 'bold'))
        self.footer_label.pack(side=BOTTOM, fill=X)

        ###eleve####
        self.students_label = Label(self, bg='white', text="le nombre total des eleves /n [0] ", bd=5, relief=RAISED)
        self.students_label.place(x=350, y=300, width=300, height=50)

        #### prof ######
        self.prof_label = Label(self, bg='white', text="le nombre total des professeurs /n [0] ", bd=5, relief=RAISED)
        self.prof_label.place(x=350, y=400, width=300, height=50)

        #### classe ####
        self.class_label = Label(self, bg='white', text="le nombre total des classes /n [0] ", bd=5, relief=RAISED)
        self.class_label.place(x=350, y=500, width=300, height=50)

        # students_label = Label(self.window, bg='white', text="le nombre total \n eleves ", bd=5, relief=RAISED
        ###################################################################################################################
        self.l1 = Label(self, bg="#C3E2C2")
        self.l1.place(x=900, y=400)

        # Créez les widgets pour l'heure, le jour et la date une seule fois
        self.time_label = Label(self, font=("Arial", 50), fg="#00ff00", bg="black")
        self.time_label.place(x=570, y=100)

        self.day_label = Label(self, font=("Ink Free", 25), bg="#C3E2C2")
        self.day_label.place(x=700, y=182)

        self.date_label = Label(self, font=("Ink Free", 35), bg="#C3E2C2")
        self.date_label.place(x=560, y=229)

        # Tableau pour afficher les jours fériés
        self.holidays_frame = Frame(self)
        self.holidays_frame.place(x=880, y=310)

        # Treeview pour afficher le tableau
        self.tree = ttk.Treeview(self.holidays_frame, columns=("Date", "Holiday"), show="headings", height=11)
        self.tree.heading("#1", text="Date")
        self.tree.heading("#2", text="Holiday")
        self.tree.column("#2", width=210)
        self.tree.pack()
        self.my_time()

    def my_time(self):
        # Mettez à jour les widgets avec la nouvelle heure, jour et date
        time_string = strftime("%I:%M:%S %p")
        self.time_label.config(text=time_string)

        day_string = strftime("%A")
        self.day_label.config(text=day_string)

        date_string = strftime("%B %d ,%Y")
        self.date_label.config(text=date_string)
        self.update_contentelv()
        self.update_contentprof()
        self.update_contentclass()
        # Liste estimée de jours fériés au Maroc (à mettre à jour avec les données réelles)
        holidays_list = [
            ("2023-01-01", "New Year's Day"),
            ("2023-03-03", "Independence Manifesto Day"),
            ("2023-05-01", "Labour Day"),
            ("2023-07-30", "Throne Day"),
            ("2023-08-14", "Oued Ed-Dahab Day"),
            ("2023-08-20", "Revolution of the King and the People"),
            ("2023-08-21", "Youth Day"),
            ("2023-08-30", "Feast of the Throne"),
            ("2023-11-06", "Green March Day"),
            ("2023-11-18", "Independence Day"),
            ("2023-12-25", "Christmas Day")
        ]

        # Affichez les jours fériés dans le tableau
        for date, holiday in holidays_list:
            self.tree.insert("", "end", values=(date, holiday))

        # Planifiez la prochaine mise à jour dans 1000 millisecondes (1 seconde)
        self.after(1000, self.my_time)

    def update_contentelv(self):
        self.connect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ecole")
        cursor = self.connect.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM eleve")
            count = cursor.fetchone()[0]
            self.students_label.config(text=f"Le nombre total des élèves :\n[{str(count)}]")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            cursor.close()
            self.connect.close()

    def update_contentprof(self):
        self.connect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ecole")
        cursor = self.connect.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM prof")
            count = cursor.fetchone()[0]
            self.prof_label.config(text=f"Le nombre total des professeurs :\n[{str(count)}]")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            cursor.close()
            self.connect.close()

    def update_contentclass(self):
        self.connect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ecole")
        cursor = self.connect.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM classe")
            count = cursor.fetchone()[0]
            self.class_label.config(text=f"Le nombre total des classes:\n[{str(count)}]")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            cursor.close()
            self.connect.close()

    def students(self):
        self.new_window2 = Toplevel(self)
        self.new_objet2 = Students(self.new_window2)
    def prof(self):
        self.new_window3 = Toplevel(self)
        self.new_objet3 = Professeur(self.new_window3)
    def abssences_pr(self):
        self.new_window4 = Toplevel(self)
        self.new_objet4 = Abscence(self.new_window4)
    def paiemant(self):
        self.new_window5 = Toplevel(self)
        self.new_objet5= Paiement(self.new_window5)

    def abssence_elv(self):
        self.new_window6 = Toplevel(self)
        self.new_objet6 = Abscence_elv(self.new_window6)
    def evaluation(self):
        self.new_window6 = Toplevel(self)
        self.new_objet6 = Evaluation(self.new_window6)
    def classe(self):
        self.new_window7 = Toplevel(self)
        self.new_objet7= Classes(self.new_window7)

if __name__ == "__main__":
    login_root = Tk()
    login_app = LoginAdmin(login_root)
    login_root.mainloop()