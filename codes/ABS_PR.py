from tkinter import *
# from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class Abscence:
    def __init__(self, onglet2):
        self.onglet2 = onglet2
        self.conn = self.connecter()
        self.onglet2.geometry("1100x510+320+230")
        self.onglet2.resizable(False, False)
        self.onglet2.title("Gestion Des Absence")
        title1 = Label(self.onglet2, text="Gestion Des Absences", font=("goudy old style", 20), bg="#092635",
                       fg="white").place(x=0, y=0, width=1100)

        Ec = LabelFrame(self.onglet2, bg="#C3E2C2")
        Ec.place(x=40, y=50, width=1000, height=250)

        Id_abs_pr = Label(self.onglet2, text="Id Absence:", font=("goudy old style", 14, "bold"), fg='black',
                          bg="#C3E2C2")
        Id_abs_pr.place(x=50, y=70)
        self.Id_abs_pr_entrer = Entry(self.onglet2)
        self.Id_abs_pr_entrer.place(x=200, y=70, width=200)
        # Date abs==========
        date_abs = Label(self.onglet2, text="Date Absence:", font=("goudy old style", 14, "bold"), fg='black',
                         bg="#C3E2C2")
        date_abs.place(x=50, y=100)
        self.date_abs_entrer = Entry(self.onglet2)
        self.date_abs_entrer.place(x=200, y=100, width=200)
        # Motif=============
        motif = Label(self.onglet2, text="Motif:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        motif.place(x=50, y=140)
        self.motif_entrer = ttk.Combobox(self.onglet2,values=("NULL"))
        self.motif_entrer.place(x=200, y=140, width=200)

        Id_prof = Label(self.onglet2, text="Id Prof:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        Id_prof.place(x=50, y=180)
        self.Id_prof_entrer = Entry(self.onglet2)
        self.Id_prof_entrer.place(x=200, y=180, width=200)

        ##########################################################################################################

        ###########################################################################################################

        recherche = Label(self.onglet2, text="Recherche:", bg="#C3E2C2", font=("goudy old style", 14, "bold"))
        recherche.place(x=820, y=190)
        self.choixp = ttk.Combobox(self.onglet2, values=("Id_abs_pr"))
        self.choixp.place(x=910, y=190, width=100)

        self.Chercher_entrer = Entry(self.onglet2)
        self.Chercher_entrer.place(x=910, y=220)

        # les boutons---------------------------------------------------

        self.button = Button(self.onglet2, text="Enregistrer", bg="#163020", fg="white", font=('Arial', 10, 'bold'),
                             command=self.Enregistrer)
        self.button.place(x=50, y=260, width=100)

        self.button = Button(self.onglet2, text="Modifier", bg="#163020", fg="white", font=('Arial', 10, 'bold'),
                             command=self.Modifier)
        self.button.place(x=170, y=260, width=100)

        self.button = Button(self.onglet2, text="Supprimer", bg="#163020", fg="white", font=('Arial', 10, 'bold'),
                             command=self.Supprimer)
        self.button.place(x=290, y=260, width=100)

        self.button = Button(self.onglet2, text="Chercher", bg="#163020", fg="white", font=('Arial', 10, 'bold'),
                             command=self.Chercher)
        self.button.place(x=820, y=260, width=100)

        self.actualiser_butto = Button(self.onglet2, text="Actualiser", bg="#163020", fg="white",
                                       font=('Arial', 10, 'bold'), command=self.actual)
        self.actualiser_butto.place(x=930, y=260, width=100)
        self.button = Button(self.onglet2, text="Absences justifié", command=self.motif, bg="#163020", fg="white",
                             font=('Arial', 10, 'bold'))
        self.button.place(x=800, y=80)

        self.button = Button(self.onglet2, text="Absences non justifié", command=self.non_motif, bg="#163020",
                             fg="white",
                             font=('Arial', 10, 'bold'))
        self.button.place(x=790, y=120)

        # Création du treevview pour afficher les données en paternelle--------------------
        frame_treeview = ttk.Frame(self.onglet2)
        frame_treeview.place(x=0, y=300, relwidth=1, height=210)

        tree_columns = ("Id Absence", "Date", "Motif", "Id Professeur")
        self.treev = ttk.Treeview(frame_treeview, columns=tree_columns, show="headings")

        # Ajout des colonnes au Treeview
        for col in tree_columns:
            self.treev.heading(col, text=col)
            self.treev.column(col, width=250)
            # Ajout des scrollbars
        y_scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=self.treev.yview)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar = ttk.Scrollbar(frame_treeview, orient="horizontal", command=self.treev.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        # Configuration des scrollbars
        self.treev.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        self.treev.bind("<ButtonRelease-1>", self.on_treev_select)
        self.treev.pack()
        self.treev.bind("<ButtonRelease-1>", self.on_treev_select)
        self.treev.pack()
        self.remplir_tab()

    def effac_tableau(self):
        for item in self.treev.get_children():
            self.treev.delete(item)

    def connecter(self):
        connect = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ecole')
        return connect

    def on_treev_select(self, event):
        # Récupérer l'élément sélectionné dans le treevview
        item = self.treev.selection()[0]
        values = self.treev.item(item, 'values')

        # Mettre à jour les Entry avec les valeurs sélectionnées
        self.Id_abs_pr_entrer.delete(0, END)
        self.Id_abs_pr_entrer.insert(0, values[0])

        self.date_abs_entrer.delete(0, END)
        self.date_abs_entrer.insert(0, values[1])

        self.motif_entrer.delete(0, END)
        self.motif_entrer.insert(0, values[2])

        self.Id_prof_entrer.delete(0, END)
        self.Id_prof_entrer.insert(0, values[3])

    def remplir_tab(self):

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM absence_pr")
            results = cursor.fetchall()
            for result in results:
                self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def Enregistrer(self):
        # Récupérer les valeurs des champs
        Id_abs_pr = self.Id_abs_pr_entrer.get()
        Date_abs = self.date_abs_entrer.get()
        Motif = self.motif_entrer.get()
        Id_pr = self.Id_prof_entrer.get()

        # Exécuter la requête SQL d'insertion
        # Exécuter la requête SQL d'insertion
        query = "INSERT INTO  absence_pr (Id_abs_pr, Date_abs, Motif, Id_pr) VALUES (%s, %s, %s, %s)"
        values = (Id_abs_pr, Date_abs, Motif, Id_pr)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Absence ajouté avec succès")

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

        Id_abs_pr = self.Id_abs_pr_entrer.get()
        Date_abs = self.date_abs_entrer.get()
        Motif = self.motif_entrer.get()
        Id_pr = self.Id_prof_entrer.get()

        # Exécuter la requête SQL de mise à jour
        query = "UPDATE absence_pr SET  Date_abs=%s, Motif=%s, Id_pr=%s WHERE Id_abs_pr=%s"
        values = (Date_abs, Motif, Id_pr, Id_abs_pr)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Absence mis à jour avec succès")
        self.effac_tableau()
        self.remplir_tab()

    def Supprimer(self):
        Id_abs_pr = self.Id_abs_pr_entrer.get()

        # Vérifier si une ligne est sélectionnée dans le Treeview
        selected_item = self.treev.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une ligne à supprimer.")
            return

        # Récupérer le code CNE de l'élève à supprimer depuis la ligne sélectionnée
        item = self.treev.item(selected_item[0], 'values')
        Id_pr = item[0]

        # Exécuter la requête SQL de suppression
        query = "DELETE FROM absence_pr WHERE Id_abs_pr=%s"
        values = (Id_abs_pr,)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Absence supprimé avec succès")
        self.effac_tableau()
        self.remplir_tab()

    def actual(self):
        self.effac_tableau()
        self.remplir_tab()

    def Chercher(self):

        choixp = self.choixp.get()
        Chercher = self.Chercher_entrer.get()

        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM absence_pr WHERE {choixp} = '{Chercher}'"
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

    def motif(self):
        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM absence_pr WHERE Motif != 'NULL'"
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
    def non_motif(self):
        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM absence_pr WHERE Motif = 'NULL'"
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
    onglet2 = Abscence(onglet)
    onglet.protocol("WM_DELETE_WINDOW", lambda: (onglet2.conn.close(), onglet.destroy()))
    onglet.mainloop()
