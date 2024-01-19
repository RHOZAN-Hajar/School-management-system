from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class Evaluation:
    def __init__(self, onglet2):
        self.onglet2 = onglet2
        self.conn = self.connecter()
        self.onglet2.geometry("1100x510+320+230")
        self.onglet2.resizable(False, False)
        self.onglet2.title("Gestion Des Evaluations")

        title1 = Label(self.onglet2, text="Gestion Des Evaluations", font=("goudy old style", 20, "bold"), bg="#092635",
                       fg="white").place(x=0, y=0, width=1100)

        Ec = LabelFrame(self.onglet2, bg="#C3E2C2")
        Ec.place(x=40, y=50, width=1000, height=280)

        # Id_eval=============
        Id_eval = Label(self.onglet2, text="Id Evaluation:", font=("goudy old style", 14, "bold"), fg='black',
                        bg="#C3E2C2")
        Id_eval.place(x=50, y=70)
        self.Id_eval_entrer = Entry(self.onglet2)
        self.Id_eval_entrer.place(x=200, y=70, width=200)
        # date========
        Date_eval = Label(self.onglet2, text="Date:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        Date_eval.place(x=50, y=110)
        self.Date_eval_entrer = Entry(self.onglet2)
        self.Date_eval_entrer.place(x=200, y=110, width=200)

        # Note========
        Note_eval = Label(self.onglet2, text="Note", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        Note_eval.place(x=50, y=150)
        self.Note_eval_entrer = Entry(self.onglet2)
        self.Note_eval_entrer.place(x=200, y=150, width=200)

        # Id eleve=====
        Id_elv = Label(self.onglet2, text="Id Eleve:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        Id_elv.place(x=50, y=190)
        self.Id_elv_entrer = Entry(self.onglet2)
        self.Id_elv_entrer.place(x=200, y=190, width=200)

        # code matiere=========
        Code_mat = Label(self.onglet2, text="Code Matiere:", font=("goudy old style", 14, "bold"), fg='black',
                         bg="#C3E2C2")
        Code_mat.place(x=50, y=230)

        self.Code_mat_entrer = ttk.Combobox(self.onglet2, values=self.code_mat())
        self.Code_mat_entrer.place(x=200, y=230, width=200)

        ##########################################################################################################

        ##########################################################################################################
        recherche = Label(self.onglet2, text="Recherche:", bg="#C3E2C2", font=("goudy old style", 13, "bold"))
        recherche.place(x=800, y=220)

        self.choixp = ttk.Combobox(self.onglet2, values=("Id_elv", "Id_eval","Code_mat"))
        self.choixp.place(x=900, y=220, width=100)

        self.Chercher_entrer = Entry(self.onglet2)
        self.Chercher_entrer.place(x=900, y=250)

        # les boutons---------------------------------------------------

        self.button1 = Button(self.onglet2, text="Enregistrer", bg="#304D30", fg="white", command=self.Enregistrer)
        self.button1.place(x=50, y=295, width=100)

        self.button2 = Button(self.onglet2, text="Modifier", bg="#304D30", fg="white", command=self.Modifier)
        self.button2.place(x=170, y=295, width=100)

        self.button3 = Button(self.onglet2, text="Supprimer", bg="#304D30", fg="white", command=self.Supprimer)
        self.button3.place(x=290, y=295, width=100)

        self.button4 = Button(self.onglet2, text="Chercher", bg="#304D30", fg="white", command=self.Chercher)
        self.button4.place(x=800, y=295, width=100)

        self.actualiser_butto = Button(self.onglet2, text="Actualiser", bg="#304D30", fg="white", command=self.actual)
        self.actualiser_butto.place(x=920, y=295, width=100)

        # Création du treevview pour afficher les données--------------------
        frame_treeview = ttk.Frame(self.onglet2)
        frame_treeview.place(x=0, y=350, relwidth=1, height=170)

        tree_columns = ("Id Evaluation", "Date Evaluation", "Note Evaluation", "Id Eleve", "Code Matiere")
        self.treev = ttk.Treeview(frame_treeview, columns=tree_columns, show="headings")

        # Ajout des colonnes au Treeview
        for col in tree_columns:
            self.treev.heading(col, text=col)
            self.treev.column(col, width=210, stretch=True)

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
                database='ecole prive'
        )
        return connect

    def on_treev_select(self, event):
        # Récupérer l'élément sélectionné dans le treevview
        item = self.treev.selection()[0]
        values = self.treev.item(item, 'values')

        # Mettre à jour les Entry avec les valeurs sélectionnées
        self.Id_eval_entrer.delete(0, END)
        self.Id_eval_entrer.insert(0, values[0])

        self.Date_eval_entrer.delete(0, END)
        self.Date_eval_entrer.insert(0, values[1])

        self.Note_eval_entrer.delete(0, END)
        self.Note_eval_entrer.insert(0, values[2])

        self.Id_elv_entrer.delete(0, END)
        self.Id_elv_entrer.insert(0, values[3])

        self.Code_mat_entrer.delete(0, END)
        self.Code_mat_entrer.insert(0, values[4])

    def remplir_tab(self):

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM evaluation ORDER BY Date_eval")
            results = cursor.fetchall()
            for result in results:
                self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def Enregistrer(self):
        # Récupérer les valeurs des champs
        Id_eval = self.Id_eval_entrer.get()
        Date_eval = self.Date_eval_entrer.get()
        Note_eval = self.Note_eval_entrer.get()
        Id_elv = self.Id_elv_entrer.get()
        Code_mat = self.Code_mat_entrer.get()

        # Exécuter la requête SQL d'insertion
        query = "INSERT INTO evaluation (Id_eval, Date_eval, Note_eval, Id_elv, Code_mat) VALUES (%s, %s, %s, %s, %s) "
        values = (Id_eval, Date_eval, Note_eval, Id_elv, Code_mat)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Évaluation ajouté avec succès")

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

        Id_eval = self.Id_eval_entrer.get()
        Date_eval = self.Date_eval_entrer.get()
        Code_mat = self.Code_mat_entrer.get()
        Note_eval = self.Note_eval_entrer.get()
        Id_elv = self.Id_elv_entrer.get()

        # Exécuter la requête SQL de mise à jour
        query = "UPDATE evaluation SET  Date_eval=%s, Note_eval=%s, Id_elv=%s, Code_mat=%s WHERE Id_eval=%s"
        values = (Date_eval, Note_eval, Id_elv, Code_mat, Id_eval)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Évaluation mis à jour avec succès")
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
        Id_eval = item[0]

        # Exécuter la requête SQL de suppression
        query = "DELETE FROM evaluation WHERE id_eval=%s"
        values = (Id_eval,)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Évaluation supprimé avec succès")
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
            query = f"SELECT * FROM evaluation WHERE {choixp} = '{Chercher}'"
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
    def code_mat(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT Code_mat FROM matiere")
        results = cursor.fetchall()
        return [classe[0] for classe in results]

if __name__ == "__main__":
    onglet = Tk()
    onglet2 = Evaluation(onglet)
    onglet.protocol("WM_DELETE_WINDOW", lambda: (onglet2.conn.close(), onglet.destroy()))
    onglet.mainloop()