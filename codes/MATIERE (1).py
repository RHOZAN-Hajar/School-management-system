from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class Matiere:
    def __init__(self, onglet2, callback_function=None):
        self.onglet2 = onglet2
        self.callback_function = callback_function
        self.conn = self.connecter()
        self.onglet2.geometry("1100x300+320+230")
        self.onglet2.resizable(False, False)
        self.onglet2.title("Gestion Des Matieres")

        title1 = Label(self.onglet2, text="Gestion Des Matieres", font=("goudy old style", 20), bg="#092635",
                       fg="white").place(x=0, y=0, width=1100)

        mat_fram = LabelFrame(self.onglet2, font=('Arial', 10, 'bold'), bg="#C3E2C2")
        mat_fram.place(x=40, y=50, width=600, height=230)

        Code_mat = Label(self.onglet2, text="Code Matiere:", font=("goudy old style", 14, "bold"), bg="#C3E2C2")
        Code_mat.place(x=50, y=80)
        self.Code_mat_entrer = Entry(self.onglet2)
        self.Code_mat_entrer.place(x=200, y=90, width=200)
        # nom==========
        Nom_mat = Label(self.onglet2, text="Nom Matiere:", bg="#C3E2C2", font=("goudy old style", 14, "bold")
                        )
        Nom_mat.place(x=50, y=120)
        self.Nom_mat_entrer = Entry(self.onglet2)
        self.Nom_mat_entrer.place(x=200, y=130, width=200)

        # les bouton---------------------------------------------

        self.button = Button(self.onglet2, text="Enregistrer", command=lambda :self.Ajouter(callback_function), font=('Arial', 10, 'bold'),
                             bg="#163020", fg="white")
        self.button.place(x=170, y=230, width=100)

        self.button = Button(self.onglet2, text="Modifier", command=self.Modifier, font=('Arial', 10, 'bold'),
                             bg="#163020", fg="white")
        self.button.place(x=290, y=230, width=100)

        self.button = Button(self.onglet2, text="Supprimer", command=lambda :self.Supprimer(callback_function), font=('Arial', 10, 'bold'),
                             bg="#163020", fg="white")
        self.button.place(x=410, y=230, width=100)

        # Création du treevview pour afficher les données en paternelle--------------------
        frame_treeview = ttk.Frame(self.onglet2)
        frame_treeview.place(x=680, y=50, height=1000)

        tree_columns = ("Code Matiere", "Nom Matiere")

        self.treev = ttk.Treeview(frame_treeview, columns=tree_columns, show="headings")

        # Ajout des colonnes au Treeview
        for col in tree_columns:
            self.treev.heading(col, text=col)
            self.treev.column(col, width=200, stretch=True)

        # Ajout des scrollbars
        y_scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=self.treev.yview)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar = ttk.Scrollbar(frame_treeview, orient="horizontal", command=self.treev.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        # Configuration des scrollbars
        self.treev.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        self.treev.bind("<ButtonRelease-1>", self.on_treev_select)
        self.treev.pack()
        self.remplir_tab()

    def effac_tableau(self):
        for item in self.treev.get_children():
            self.treev.delete(item)

    def connecter(self):
        connect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ecole")
        return connect

    def on_treev_select(self, event):
        # Récupérer l'élément sélectionné dans le treevview
        item = self.treev.selection()[0]
        values = self.treev.item(item, 'values')

        # Mettre à jour les Entry avec les valeurs sélectionnées

        self.Code_mat_entrer.delete(0, END)
        self.Code_mat_entrer.insert(0, values[0])

        self.Nom_mat_entrer.delete(0, END)
        self.Nom_mat_entrer.insert(0, values[1])

    def remplir_tab(self):

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM matiere")
            results = cursor.fetchall()
            for result in results:
                self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def Ajouter(self,callback_function):
        # Récupérer les valeurs des champs

        Code_mat_entrer = self.Code_mat_entrer.get()
        Nom_mat = self.Nom_mat_entrer.get()

        # Exécuter la requête SQL d'insertion
        query = "INSERT INTO matiere (Code_mat,Nom_mat) VALUES (%s, %s)"
        values = (Code_mat_entrer, Nom_mat)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Matiere ajouté avec succès")

            # Vider le Treeview
            for item in self.treev.get_children():
                self.treev.delete(item)

            # Remplir le Treeview avec les nouvelles données
            self.remplir_tab()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            cursor.close()
        if callback_function:
            callback_function()
    def Modifier(self):

        Code_mat = self.Code_mat_entrer.get()
        Nom_mat = self.Nom_mat_entrer.get()

        # Exécuter la requête SQL de mise à jour
        query = "UPDATE matiere SET Nom_mat=%s WHERE Code_mat=%s"
        values = (Nom_mat, Code_mat)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Matiere mis à jour avec succès")
        self.effac_tableau()
        self.remplir_tab()

    def Supprimer(self,callback_function):
        # Vérifier si une ligne est sélectionnée dans le Treeview
        selected_item = self.treev.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une ligne à supprimer.")
            return

        # Récupérer le code CNE de l'élève à supprimer depuis la ligne sélectionnée
        item = self.treev.item(selected_item[0], 'values')
        nom = item[0]

        # Exécuter la requête SQL de suppression
        query = "DELETE FROM matiere WHERE Code_mat=%s"
        values = (nom,)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Matiere supprimé avec succès")
        self.effac_tableau()
        self.remplir_tab()
        if callback_function:
            callback_function()
    def actual(self):
        self.effac_tableau()
        self.remplir_tab()


if __name__ == "__main__":
    onglet = Tk()
    onglet2 = Matiere(onglet)
    onglet.protocol("WM_DELETE_WINDOW", lambda: (onglet2.conn.close(), onglet.destroy()))
    onglet.mainloop()