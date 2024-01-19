from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class Paiement:
    def __init__(self, onglet2):
        self.onglet2 = onglet2
        self.conn = self.connecter()
        self.onglet2.geometry("1100x510+320+230")
        self.onglet2.resizable(False, False)
        self.onglet2.title("Gestion Des Paiements")

        title1 = Label(self.onglet2, text="Gestion Des Paiements", font=("goudy old style", 20, "bold"), bg="#092635",
                       fg="white").place(x=0, y=0, width=1100)

        paiement_fram = LabelFrame(self.onglet2, bg="#C3E2C2")
        paiement_fram.place(x=40, y=50, width=1000, height=250)

        id_pai = Label(self.onglet2, text="Id De Paiement:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        id_pai.place(x=50, y=70)
        self.id_pai_entrer = Entry(self.onglet2)
        self.id_pai_entrer.place(x=200, y=70, width=200)

        type = Label(self.onglet2, text="Type De Paiement:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        type.place(x=50, y=110)
        self.type_entrer = Entry(self.onglet2)
        self.type_entrer.place(x=200, y=110, width=200)

        date = Label(self.onglet2, text="Date De Paiement:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        date.place(x=50, y=150)
        self.date_entrer = Entry(self.onglet2)
        self.date_entrer.place(x=200, y=150, width=200)

        montant = Label(self.onglet2, text="Montant De Paiement:", font=("goudy old style", 11, "bold"), bg="#C3E2C2")
        montant.place(x=50, y=190)
        self.montant_entrer = Entry(self.onglet2)
        self.montant_entrer.place(x=200, y=190, width=200)

        Versement = Label(self.onglet2, text="Versement:", font=("goudy old style", 13, "bold"), bg="#C3E2C2")
        Versement.place(x=50, y=220)
        self.Versement_entrer = Entry(self.onglet2)
        self.Versement_entrer.place(x=200, y=220, width=200)

        rest = Label(self.onglet2, text="Le Reste :", font=("goudy old style", 13, "bold"), bg="#C3E2C2")
        rest.place(x=620, y=70)
        self.rest_entrer = Entry(self.onglet2)
        self.rest_entrer.place(x=700, y=70, width=200)

        id_elv = Label(self.onglet2, text="Id Eleve :", font=("goudy old style", 13, "bold"), bg="#C3E2C2")
        id_elv.place(x=620, y=100)
        self.id_elv_entrer = Entry(self.onglet2)
        self.id_elv_entrer.place(x=700, y=100, width=200)

        recherche = Label(self.onglet2, text="Recherche:", font=("goudy old style", 13, "bold"), bg="#C3E2C2")
        recherche.place(x=800, y=190)

        self.choixp = ttk.Combobox(self.onglet2, values=("Id_elv", "Id_pai"))
        self.choixp.place(x=900, y=200, width=100)

        self.chercher_entrer = Entry(self.onglet2)
        self.chercher_entrer.place(x=900, y=230)

        self.button = Button(self.onglet2, text="Paye", command=self.paye, bg="#C6CF9B", fg="black", width=10).place(
            x=955, y=90)
        self.button = Button(self.onglet2, text="Non Paye", command=self.non_paye, bg="#C6CF9B", fg="black",
                             width=10).place(x=955, y=60)

        # les bouttons---------------------------------------------------

        self.button = Button(self.onglet2, text="Enregistrer", bg="#163020", fg="white", command=self.Ajouter)
        self.button.place(x=50, y=270, width=100)

        self.button = Button(self.onglet2, text="Modifier", bg="#163020", fg="white", command=self.Modifier)
        self.button.place(x=170, y=270, width=100)

        self.button = Button(self.onglet2, text="Supprimer", bg="#163020", fg="white", command=self.Supprimer)
        self.button.place(x=290, y=270, width=100)

        self.button = Button(self.onglet2, text="Chercher", bg="#163020", fg="white", command=self.Chercher)
        self.button.place(x=820, y=270, width=100)

        self.button_affich = Button(self.onglet2, text="Actualiser", bg="#163020", fg="white", command=self.Actualiser)
        self.button_affich.place(x=930, y=270, width=100)

        # Création du treevview pour afficher les données en paternelle--------------------
        frame_treeview = ttk.Frame(self.onglet2)
        frame_treeview.place(x=0, y=300, relwidth=1, height=210)

        tree_columns = ("Id Paiement", "Type", "Date", "Montant", "Versement", "reste", "Id Eleve")
        self.treev = ttk.Treeview(frame_treeview, columns=tree_columns, show="headings")

        # Ajout des colonnes au Treeview
        for col in tree_columns:
            self.treev.heading(col, text=col)
            self.treev.column(col, width=150, stretch=True)
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
                            host='127.0.0.1',
                user='root',
                password='',
                database='ecole prive')
        return connect

    def on_treev_select(self, event):
        # Récupérer l'élément sélectionné dans le treevview
        item = self.treev.selection()[0]
        values = self.treev.item(item, 'values')

        # Mettre à jour les Entry avec les valeurs sélectionnées
        self.id_pai_entrer.delete(0, END)
        self.id_pai_entrer.insert(0, values[0])

        self.type_entrer.delete(0, END)
        self.type_entrer.insert(0, values[1])

        self.date_entrer.delete(0, END)
        self.date_entrer.insert(0, values[2])

        self.montant_entrer.delete(0, END)
        self.montant_entrer.insert(0, values[3])

        self.Versement_entrer.delete(0, END)
        self.Versement_entrer.insert(0, values[4])

        self.rest_entrer.delete(0, END)
        self.rest_entrer.insert(0, values[5])

        self.id_elv_entrer.delete(0, END)
        self.id_elv_entrer.insert(0, values[6])

    def remplir_tab(self):

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM paiement")
            results = cursor.fetchall()
            for result in results:
                self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def Ajouter(self):
        # Récupérer les valeurs des champs
        id_pai = self.id_pai_entrer.get()
        type = self.type_entrer.get()
        nom = self.date_entrer.get()
        prenom = self.montant_entrer.get()
        Versement = self.Versement_entrer.get()
        rest = self.rest_entrer.get()
        id_elv = self.id_elv_entrer.get()

        # Exécuter la requête SQL d'insertion
        query = "INSERT INTO paiement(Id_pai,Type_pai,Date_pai,Montant_pai,Versement,Reste,Id_elv) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        values = (id_pai, type, nom, prenom, Versement, rest, id_elv)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Paiement ajouté avec succès")

            # Vider le Treeview
            for item in self.treev.get_children():
                self.treev.delete(item)

            # Remplir le Treeview avec les nouvelles données
            self.remplir_tab()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            cursor.close()

    def Modifier(self):

        id_pai = self.id_pai_entrer.get()
        type = self.type_entrer.get()
        nom = self.date_entrer.get()
        prenom = self.montant_entrer.get()
        Versement = self.Versement_entrer.get()
        rest = self.rest_entrer.get()
        id_elv = self.id_elv_entrer.get()
        # Exécuter la requête SQL de mise à jour
        query = "UPDATE paiement SET Type_pai=%s,Date_pai=%s, Montant_pai=%s, Versement=%s,Reste=%s, Id_elv=%s WHERE Id_pai=%s"
        values = (type, nom, prenom, Versement, rest, id_elv, id_pai)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Paiement mis à jour avec succès")
        self.effac_tableau()
        self.remplir_tab()

    def Supprimer(self):
        # Vérifier si une ligne est sélectionnée dans le Treeview
        selected_item = self.treev.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une ligne à supprimer.")
            return

        # Récupérer le code CNE de l'élève à supprimer depuis la ligne sélectionnée
        item = self.treev.item(selected_item[0], 'values')
        id_pai = item[0]

        # Exécuter la requête SQL de suppression
        query = "DELETE FROM paiement WHERE Id_pai=%s"
        values = (id_pai,)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Paiement supprimé avec succès")
        self.effac_tableau()
        self.remplir_tab()

    def Actualiser(self):
        self.effac_tableau()
        self.remplir_tab()

    def Chercher(self):

        choixp = self.choixp.get()
        chercher = self.chercher_entrer.get()

        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM paiement WHERE {choixp} = '{chercher}'"
            cursor.execute(query)
            results = cursor.fetchall()
            if len(results) != 0:
                self.treev.delete(*self.treev.get_children())
            for result in results:
                self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def paye(self):
        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM paiement WHERE Montant_pai = Versement "
            cursor.execute(query)
            results = cursor.fetchall()
            if len(results) != 0:
                self.treev.delete(*self.treev.get_children())
            for result in results:
                self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def non_paye(self):
        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM paiement WHERE Montant_pai != Versement"
            cursor.execute(query)
            results = cursor.fetchall()
            if len(results) != 0:
                self.treev.delete(*self.treev.get_children())
            for result in results:
                self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()


if __name__ == "__main__":
    onglet = Tk()
    onglet2 = Paiement(onglet)
    onglet.protocol("WM_DELETE_WINDOW", lambda: (onglet2.conn.close(), onglet.destroy()))
    onglet.mainloop()