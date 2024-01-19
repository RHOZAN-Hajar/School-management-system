import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
import mysql.connector as mysql


# create the classes interface
class Classes:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x510+320+230")
        self.root.resizable(False, False)
        self.root.title("Classes")

        # variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_id_classe = StringVar()
        self.var_nom_classe = StringVar()
        self.var_nombre_elv = StringVar()

        title1 = Label(self.root, text="Gestion Des Classe", font=("goudy old style", 20), bg="#092635",
                       fg="white").place(x=0, y=0, width=1100)

        Ec = LabelFrame(self.root, bg="#C3E2C2")
        Ec.place(x=40, y=50, width=1000, height=280)

        # content
        lbl_id_classe = Label(self.root, text="Id Classe:", font=("goudy old style", 14, "bold"), bg="#C3E2C2").place(
            x=50, y=130)
        lbl_nom_classe = Label(self.root, text="Niveau:", font=("goudy old style", 14, "bold"), bg="#C3E2C2").place(
            x=350, y=130)
        lbl_nombre_elv = Label(self.root, text=" Nombre Des Eleves:", font=("goudy old style", 14, "bold"),
                               bg="#C3E2C2").place(x=670, y=130)

        lbl_id_classe = Entry(self.root, textvariable=self.var_id_classe, font=("goudy old style", 14, "bold"),
                              bg="white").place(x=140, y=130, width=180)
        lbl_nom_classe = Entry(self.root, textvariable=self.var_nom_classe, font=("goudy old style", 14, "bold"),
                               bg="white").place(x=470, y=130, width=180)
        lbl_nombre_elv = Entry(self.root, textvariable=self.var_nombre_elv, font=("goudy old style", 14, "bold"),
                               bg="white").place(x=850, y=130, width=180)

        # buttons
        btn_ajouter = Button(self.root, text="Enregistrer", font=("goudy old style", 14), bg="#304D30", fg="white",
                             cursor="hand2", command=self.add_class)
        btn_ajouter.place(x=300, y=220, width=110, height=30)
        btn_modifier = Button(self.root, text="Modifier ", font=("goudy old style", 14), bg="#304D30", fg="white",
                              cursor="hand2", command=self.update_class).place(x=450, y=220, width=110, height=30)
        btn_supprimer = Button(self.root, text="Supprimer", font=("goudy old style", 14), bg="#304D30", fg="white",
                               cursor="hand2", command=self.delete_class).place(x=600, y=220, width=110, height=30)

        # Classes informations
        classes_frame = ttk.Frame(self.root)
        classes_frame.place(x=0, y=350, relwidth=1, height=170)

        Scroll_x = Scrollbar(classes_frame, orient=HORIZONTAL)
        Scroll_y = Scrollbar(classes_frame, orient=VERTICAL)

        self.ClassesTable = ttk.Treeview(classes_frame, columns=("Id_classe", "Niveau_classe", "Nombre_elv"),
                                         xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)

        Scroll_x.pack(side=BOTTOM, fill=X)
        Scroll_y.pack(side=RIGHT, fill=Y)

        Scroll_x = ttk.Scrollbar(command=self.ClassesTable.xview)
        Scroll_y = ttk.Scrollbar(command=self.ClassesTable.yview)

        self.ClassesTable.heading("Id_classe", text="Classe Id")
        self.ClassesTable.heading("Niveau_classe", text="Nom Classe")
        self.ClassesTable.heading("Nombre_elv", text="Nombre Des Eleves")

        self.ClassesTable["show"] = "headings"

        self.ClassesTable.column("Id_classe", width=40)
        self.ClassesTable.column("Niveau_classe", width=100)
        self.ClassesTable.column("Nombre_elv", width=100)

        self.ClassesTable.pack(fill=BOTH, expand=1)
        self.ClassesTable.bind("<ButtonRelease-1>", self.get_cursor)

        self.affichage()

    # add classe
    def add_class(self):
        try:
            connection = mysql.connect(
                host="localhost",
                user="root",
                password="",
                database="ecole"
            )
            cursor = connection.cursor()

            query = "INSERT INTO classe (Id_cls, Niveau, Nombre_elv) VALUES (%s,%s, %s)"
            data = (self.var_id_classe.get(), self.var_nom_classe.get(), self.var_nombre_elv.get())
            cursor.execute(query, data)

            connection.commit()
            connection.close()
            self.affichage()
            messagebox.showinfo("Success", "Classe ajouté avec succès")
        except mysql.Error as e:
            messagebox.showerror("Erreur", f"Erreur: {e}")

    # update

    def update_class(self):
        try:
            connection = mysql.connect(
                host="localhost",
                user="root",
                password="",
                database="ecole"
            )
            cursor = connection.cursor()

            query = "UPDATE classe SET Niveau = %s, Nombre_elv = %s WHERE Id_cls = %s"
            data = (self.var_nom_classe.get(), int(self.var_nombre_elv.get()), self.var_id_classe.get())
            cursor.execute(query, data)

            connection.commit()
            connection.close()
            self.affichage()
            messagebox.showinfo("Success", "Classe mis à jour avec succès")
        except mysql.Error as e:
            messagebox.showerror("Erreur", f"Erreur: {e}")

    # delete

    def delete_class(self):
        try:
            connection = mysql.connect(
                host="localhost",
                user="root",
                password="",
                database="ecole"
            )
            cursor = connection.cursor()

            query = "DELETE FROM classe WHERE Id_cls = %s"
            data = (self.var_id_classe.get(),)
            cursor.execute(query, data)

            connection.commit()
            connection.close()
            self.affichage()

            messagebox.showinfo("Success", "Classe supprimé avec succès")
        except mysql.Error as e:
            messagebox.showerror("Erreur", f"Erreur : {e}")

    def affichage(self):
        con = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="ecole")
        cur = con.cursor()
        cur.execute("SELECT * FROM classe ")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.ClassesTable.delete(*self.ClassesTable.get_children())
            for i in rows:
                self.ClassesTable.insert("", END, values=i)
            con.commit()
        con.close()

    def get_cursor(self, event=""):
        cursor_row = self.ClassesTable.focus()
        content = self.ClassesTable.item(cursor_row)
        row = content["values"]
        self.var_id_classe.set(row[0])
        self.var_nom_classe.set(row[1])
        self.var_nombre_elv.set(row[2])


if __name__ == "__main__":
    root = Tk()
    root2 = Classes(root)
    root.protocol("WM_DELETE_root", lambda: (root2.conn.close(), root.destroy()))
    root.mainloop()