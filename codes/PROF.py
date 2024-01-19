from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from MATIERE import Matiere


class Professeur:
    def __init__(self, onglet2, callback_function=None):
        self.onglet2 = onglet2
        self.callback_function=callback_function
        self.conn = self.connecter()
        self.onglet2.geometry("1100x510+320+230")
        self.onglet2.resizable(False, False)
        self.onglet2.title("Gestion Des Professeurs")
        title1 = Label(self.onglet2, text="Gestion Des Professeurs", font=("goudy old style", 20, "bold"), bg="#092635",
                       fg="white").place(x=0, y=0, width=1100)

        parent_fram = LabelFrame(self.onglet2, bg="#C3E2C2")
        parent_fram.place(x=40, y=50, width=1000, height=300)

        # Id prof=============
        Id_prof = Label(self.onglet2, text="Id Prof:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        Id_prof.place(x=50, y=60)
        self.Id_prof_entrer = Entry(self.onglet2)
        self.Id_prof_entrer.place(x=200, y=60, width=200)
        # nom==========
        Nom_pr = Label(self.onglet2, text="Nom:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        Nom_pr.place(x=50, y=90)
        self.Nom_pr_entrer = Entry(self.onglet2)
        self.Nom_pr_entrer.place(x=200, y=90, width=200)

        Prenom_pr = Label(self.onglet2, text="Prenom :", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        Prenom_pr.place(x=50, y=120)
        self.Prenom_pr_entrer = Entry(self.onglet2)
        self.Prenom_pr_entrer.place(x=200, y=120, width=200)
        # tel profession========

        Genre_pr = Label(self.onglet2, text="Genre :", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        Genre_pr.place(x=50, y=160)
        self.Genre_pr_entrer = ttk.Combobox(self.onglet2, values=("Masculin", "Feminin"))
        self.Genre_pr_entrer.place(x=200, y=160, width=200)

        Natio_pr = Label(self.onglet2, text="Nationalité :", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        Natio_pr.place(x=50, y=200)
        self.Natio_pr_entrer = Entry(self.onglet2)
        self.Natio_pr_entrer.place(x=200, y=200, width=200)

        Adrs_pr = Label(self.onglet2, text="Adresse:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        Adrs_pr.place(x=50, y=240)
        self.Adrs_pr_entrer = Entry(self.onglet2)
        self.Adrs_pr_entrer.place(x=200, y=240, width=200)

        Salaire = Label(self.onglet2, text="Salaire:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        Salaire.place(x=50, y=280)
        self.Salaire_entrer = Entry(self.onglet2)
        self.Salaire_entrer.place(x=200, y=280, width=200)

        Situation = Label(self.onglet2, text="Situation:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        Situation.place(x=530, y=60)
        self.Situation_entrer = Entry(self.onglet2)
        self.Situation_entrer.place(x=650, y=60, width=200)

        Emai = Label(self.onglet2, text="Email:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        Emai.place(x=530, y=90)
        self.Emai_entrer = Entry(self.onglet2)
        self.Emai_entrer.place(x=650, y=90, width=200)

        date_embauche = Label(self.onglet2, text="Date Embauche:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        date_embauche.place(x=530, y=120)
        self.date_embauche_entrer = Entry(self.onglet2)
        self.date_embauche_entrer.place(x=650, y=120, width=200)

        date_sortie = Label(self.onglet2, text="Date Sortie", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        date_sortie.place(x=530, y=160)
        self.date_sortie_entrer = Entry(self.onglet2)
        self.date_sortie_entrer.place(x=650, y=160, width=200)

        code_matirer = Label(self.onglet2, text="Code Matiere:", font=("goudy old style", 12, "bold"), bg="#C3E2C2")
        code_matirer.place(x=530, y=200)
        self.code_matirer_entrer = ttk.Combobox(self.onglet2, values=self.code_mat())
        self.code_matirer_entrer.place(x=650, y=200, width=200)

        # le recherche de prof

        recherche = Label(self.onglet2, text="Recherche:", bg="#C3E2C2", font=("goudy old style", 13, "bold"))
        recherche.place(x=530, y=260)

        self.choix = ttk.Combobox(self.onglet2, values=("Id_pr", "Nom_pr"))
        self.choix.place(x=650, y=260, width=100)

        self.chercher_entrer = Entry(self.onglet2)
        self.chercher_entrer.place(x=650, y=290)

        # les boutons---------------------------------------------------

        self.button = Button(self.onglet2, text="Enregistrer", bg="#304D30", fg="white", command=self.Ajouter)
        self.button.place(x=50, y=320, width=100)

        self.button = Button(self.onglet2, text="Modifier", bg="#304D30", fg="white", command=self.Modifier)
        self.button.place(x=170, y=320, width=100)

        self.button = Button(self.onglet2, text="Supprimer", bg="#304D30", fg="white", command=self.Supprimer)
        self.button.place(x=290, y=320, width=100)

        self.button = Button(self.onglet2, text="Chercher", bg="#304D30", fg="white", command=self.chercher)
        self.button.place(x=650, y=320, width=100)

        self.button_affich = Button(self.onglet2, text="Actualiser", bg="#304D30", fg="white", command=self.actual)
        self.button_affich.place(x=770, y=320, width=100)

        self.button = Button(self.onglet2, text="Matieres", command=self.mat, bg="#C6CF9B", fg="black")
        self.button.place(x=920, y=320, width=100)

        # Création du treevview pour afficher les données en paternelle--------------------
        frame_treeview = ttk.Frame(self.onglet2)
        frame_treeview.place(x=0, y=350, relwidth=1, height=210)

        tree_columns = (
        "Id Prof", "Nom", "Prenom", "Genre", "Nationalité", "Adresse", "Salaire", "Situation", "Email", "Date Embauche",
        "Date Sortie", "Code Matiere")
        self.treev = ttk.Treeview(frame_treeview, columns=tree_columns, show="headings")

        # Ajout des colonnes au Treeview
        for col in tree_columns:
            self.treev.heading(col, text=col)
            self.treev.column(col, width=90)
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

        self.Id_prof_entrer.delete(0, END)
        self.Id_prof_entrer.insert(0, values[0])

        self.Nom_pr_entrer.delete(0, END)
        self.Nom_pr_entrer.insert(0, values[1])

        self.Prenom_pr_entrer.delete(0, END)
        self.Prenom_pr_entrer.insert(0, values[2])

        self.Genre_pr_entrer.delete(0, END)
        self.Genre_pr_entrer.insert(0, values[3])

        self.Natio_pr_entrer.delete(0, END)
        self.Natio_pr_entrer.insert(0, values[4])

        self.Adrs_pr_entrer.delete(0, END)
        self.Adrs_pr_entrer.insert(0, values[5])

        self.Salaire_entrer.delete(0, END)
        self.Salaire_entrer.insert(0, values[6])

        self.Situation_entrer.delete(0, END)
        self.Situation_entrer.insert(0, values[7])

        self.Emai_entrer.delete(0, END)
        self.Emai_entrer.insert(0, values[8])

        self.date_embauche_entrer.delete(0, END)
        self.date_embauche_entrer.insert(0, values[9])

        self.date_sortie_entrer.delete(0, END)
        self.date_sortie_entrer.insert(0, values[10])

        self.code_matirer_entrer.delete(0, END)
        self.code_matirer_entrer.insert(0, values[11])

    def remplir_tab(self):

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM prof")
            results = cursor.fetchall()
            for result in results:
                self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def Ajouter(self):
        # Récupérer les valeurs des champs

        id_prof = self.Id_prof_entrer.get()
        Nom_pr = self.Nom_pr_entrer.get()
        Prenom_pr = self.Prenom_pr_entrer.get()
        Genre_pr = self.Genre_pr_entrer.get()
        Natio_pr = self.Natio_pr_entrer.get()
        Adrs_pr = self.Adrs_pr_entrer.get()
        Salaire = self.Salaire_entrer.get()

        situation = self.Situation_entrer.get()
        email = self.Emai_entrer.get()
        dateb = self.date_embauche_entrer.get()
        dates = self.date_sortie_entrer.get()
        code = self.code_matirer_entrer.get()

        # Exécuter la requête SQL d'insertion
        query = "INSERT INTO prof (Id_pr, Nom_pr,Prenom_pr ,Genre_pr, Natio_pr, Adrs_pr, Salaire,Situation,Email_pr,Date_emb,Date_sort,Code_mat) VALUES ( %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)"
        values = (
        id_prof, Nom_pr, Prenom_pr, Genre_pr, Natio_pr, Adrs_pr, Salaire, situation, email, dateb, dates, code)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Professeur ajouté avec succès")

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

        Id_prof = self.Id_prof_entrer.get()
        Nom_pr = self.Nom_pr_entrer.get()
        Prenom_pr = self.Prenom_pr_entrer.get()
        Genre_pr = self.Genre_pr_entrer.get()
        Natio_pr = self.Natio_pr_entrer.get()
        Adrs_pr = self.Adrs_pr_entrer.get()
        Salaire = self.Salaire_entrer.get()
        situation = self.Situation_entrer.get()
        email = self.Emai_entrer.get()
        dateb = self.date_embauche_entrer.get()
        dates = self.date_sortie_entrer.get()
        code = self.code_matirer_entrer.get()

        # Exécuter la requête SQL de mise à jour
        query = "UPDATE prof SET  Nom_pr=%s,Prenom_pr=%s, code_mat=%s, Natio_pr=%s, Adrs_pr=%s, Salaire=%s,Situation=%s,Email_pr=%s,Date_emb=%s,Date_sort=%s,Code_mat=%s WHERE Id_pr=%s"
        values = (
        Nom_pr, Prenom_pr, Genre_pr, Natio_pr, Adrs_pr, Salaire, situation, email, dateb, dates, code, Id_prof)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Professeur mis à jour avec succès")
        self.effac_tableau()
        self.remplir_tab()

    def Supprimer(self):

        selected_item = self.treev.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une ligne à supprimer.")
            return

        item = self.treev.item(selected_item[0], 'values')
        Id_prof = item[0]

        # Exécuter la requête SQL de suppression
        query = "DELETE FROM prof WHERE Id_pr=%s"
        values = (Id_prof,)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Professeur supprimé avec succès")
        self.effac_tableau()
        self.remplir_tab()

    def chercher(self):
        choix = self.choix.get()
        chercherP = self.chercher_entrer.get()

        try:
            cursor = self.conn.cursor()
            query = f"SELECT * from prof  WHERE {choix} = %s"
            cursor.execute(query, (f"{chercherP}",))
            results = cursor.fetchall()

            # Clear the Treeview
            self.effac_tableau()

            if len(results) != 0:
                for result in results:
                    self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def actual(self):
        self.effac_tableau()
        self.remplir_tab()

    def code_mat(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT Code_mat FROM matiere")
        results = cursor.fetchall()
        return [classe[0] for classe in results]

    def mat(self):
        self.new_window3 = Toplevel(self.onglet2)
        self.new_objet3 = Matiere(self.new_window3, callback_function=self.update_mat_options)

    def update_code_mat_options(self):
        # Update the options of the combobox with the latest subject codes
        self.code_matirer_entrer['values'] = self.code_mat()

    def update_mat_options(self):
        if self.callback_function:
            self.callback_function()
if __name__ == "__main__":
    onglet = Tk()
    onglet2 = Professeur(onglet)
    onglet.protocol("WM_DELETE_WINDOW", lambda: (onglet2.conn.close(), onglet.destroy()))
    onglet.mainloop()
