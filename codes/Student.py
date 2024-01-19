from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class Students:
    def __init__(self, window):
        self.window = window
        self.conn = self.connecter()
        self.window.geometry("1100x510+320+230")
        self.window.resizable(False, False)
        self.window.title("Gestion Des Eleve")

        # les tab-----------------------------------------
        notebook = ttk.Notebook(self.window)
        self.onglet1 = Frame(notebook)
        self.onglet2 = Frame(notebook)
        notebook.add(self.onglet1, text="Informations Sur Eleve")
        notebook.add(self.onglet2, text="Informations Sur Tuteur")
        notebook.pack(expand=True, fill=BOTH)

        # tab dyal etudiant---------------------------------------------
        eleve_fram = LabelFrame(self.onglet1, text="Détails Personnel", bg="#C3E2C2")
        eleve_fram.place(x=40, y=20, width=420, height=278)

        Id_elv = Label(self.onglet1, text="Id Eleve:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        Id_elv.place(x=50, y=40)
        self.Id_elv_entrer = Entry(self.onglet1)
        self.Id_elv_entrer.place(x=200, y=40, width=200)

        Nom_elv = Label(self.onglet1, text="Nom Eleve:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        Nom_elv.place(x=50, y=80)
        self.Nom_elv_entrer = Entry(self.onglet1)
        self.Nom_elv_entrer.place(x=200, y=80, width=200)

        prenom = Label(self.onglet1, text="Prenom Eleve:", font=("goudy old style", 14, "bold"), fg='black',
                       bg="#C3E2C2")
        prenom.place(x=50, y=120)
        self.prenom_entrer = Entry(self.onglet1)
        self.prenom_entrer.place(x=200, y=120, width=200)

        date_naiss = Label(self.onglet1, text="Date De Naissance:", font=("goudy old style", 14, "bold"), fg='black',
                           bg="#C3E2C2")
        date_naiss.place(x=50, y=160)
        self.date_naiss_entrer = Entry(self.onglet1)
        self.date_naiss_entrer.place(x=200, y=160, width=200)

        lieu_naiss = Label(self.onglet1, text="Lieu De Naissance:", font=("goudy old style", 14, "bold"), fg='black',
                           bg="#C3E2C2")
        lieu_naiss.place(x=50, y=200)
        self.lieu_naiss_entrer = Entry(self.onglet1)
        self.lieu_naiss_entrer.place(x=200, y=200, width=200)

        sex = Label(self.onglet1, text="Genre:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        sex.place(x=50, y=240)
        self.sex_entrer = ttk.Combobox(self.onglet1, values=("Masculin", "Feminin"))
        self.sex_entrer.place(x=200, y=240, width=200)

        eleve_fram = LabelFrame(self.onglet1, text="Détails personnel", bg="#C3E2C2")
        eleve_fram.place(x=500, y=20, width=570, height=278)

        niveau = Label(self.onglet1, text="Niveau:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        niveau.place(x=530, y=40)
        self.niveau_entrer = ttk.Combobox(self.onglet1)
        self.niveau_entrer.place(x=700, y=40, width=100)

        self.bouton_selection_niveau = Button(self.onglet1, text="Sélect Niveau", font=("goudy old style", 9, "bold"),
                                              command=self.votre_methode_apres_la_selection_du_niveau)
        self.bouton_selection_niveau.place(x=810, y=39, width=90)
        self.charger_niveau()

        id_classe = Label(self.onglet1, text="Id Classe:", font=("goudy old style", 14, "bold"), fg='black',
                          bg="#C3E2C2")
        id_classe.place(x=530, y=80)
        self.id_classe_entrer = ttk.Combobox(self.onglet1, values=self.charger_classe(niveau))
        self.id_classe_entrer.place(x=700, y=80)

        adresse = Label(self.onglet1, text="Adresse", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        adresse.place(x=530, y=120)
        self.adresse_entrer = Entry(self.onglet1)
        self.adresse_entrer.place(x=700, y=120, width=200)

        nationalite = Label(self.onglet1, text="Nationalité :", font=("goudy old style", 14, "bold"), fg='black',
                            bg="#C3E2C2")
        nationalite.place(x=530, y=160)
        self.nationalite_entrer = Entry(self.onglet1)
        self.nationalite_entrer.place(x=700, y=160, width=200)

        cin = Label(self.onglet1, text="Cin :", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        cin.place(x=530, y=200)
        self.cin_entrer = Entry(self.onglet1)
        self.cin_entrer.place(x=700, y=200, width=200)

        self.choix = ttk.Combobox(self.onglet1, values=("select", "Id_elv", "Nom_elv"), state='readonly')
        self.choix.place(x=530, y=260, width=100)
        self.choix.current(0)

        self.chercher_entrer = Entry(self.onglet1)
        self.chercher_entrer.place(x=700, y=260)

        # Configurer les boutons pour appeler les fonctions correspondantes
        self.button_affich = Button(self.onglet1, text="Actualiser", command=self.actual)
        self.button_affich.place(x=960, y=80, width=100)

        self.button_save = Button(self.onglet1, text="Enregistrer", command=self.inserer_eleve)
        self.button_save.place(x=960, y=120, width=100)

        self.button_update = Button(self.onglet1, text="Modifier", command=self.mettre_a_jour_eleve)
        self.button_update.place(x=960, y=160, width=100)

        self.button_delete = Button(self.onglet1, text="Supprimer", command=self.supprimer_eleve)
        self.button_delete.place(x=960, y=200, width=100)

        self.button = Button(self.onglet1, text="Rechercher", command=self.chercher)
        self.button.place(x=890, y=260, width=100)

        # Création du Treeview pour afficher les données eleve------------------------------
        # ------------------------------------------------------------------------------------------
        frame_treeview = ttk.Frame(self.onglet1)
        frame_treeview.place(x=0, y=300, relwidth=1, height=210)

        # pour un affichage le colonne
        tree_columns = (
        "Id", "Nom", "prenom", "date_naissance", "lieu_naissance", "Genre", "Niveau", "Id_classe", "Adresse",
        "Nationalité", "cin")
        self.tree = ttk.Treeview(frame_treeview, columns=tree_columns, show="headings")

        # Ajout des colonnes au Treeview
        for col in tree_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        # Ajouter une liaison entre l'événement de clic sur le Treeview et la fonction on_tree_select
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.remplir_tableau()
        self.tree.pack()
        parent_fram = LabelFrame(self.onglet2, text="Détails De Tuteur", bg="#C3E2C2")
        parent_fram.place(x=40, y=20, width=1000, height=250)

        cine = Label(self.onglet2, text="CIN De Tuteur:", font=("goudy old style", 14, "bold"), fg='black',
                     bg="#C3E2C2")
        cine.place(x=50, y=40)
        self.cine_entrer = Entry(self.onglet2)
        self.cine_entrer.place(x=200, y=40, width=200)
        # CIN=============
        nome = Label(self.onglet2, text="Nom Tuteur:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        nome.place(x=50, y=80)
        self.nome_entrer = Entry(self.onglet2)
        self.nome_entrer.place(x=200, y=80, width=200)
        # nom==========
        prenome = Label(self.onglet2, text="Prenom Tuteur:", font=("goudy old style", 14, "bold"), fg='black',
                        bg="#C3E2C2")
        prenome.place(x=50, y=120)
        self.prenome_entrer = Entry(self.onglet2)
        self.prenome_entrer.place(x=200, y=120, width=200)

        adress = Label(self.onglet2, text="Adresse:", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        adress.place(x=50, y=160)
        self.adress_entrer = Entry(self.onglet2)
        self.adress_entrer.place(x=200, y=160, width=200)
        # tel profession========
        profession = Label(self.onglet2, text="Profession:", font=("goudy old style", 14, "bold"), fg='black',
                           bg="#C3E2C2")
        profession.place(x=50, y=200)
        self.profession_entrer = Entry(self.onglet2)
        self.profession_entrer.place(x=200, y=200, width=200)

        email = Label(self.onglet2, text="Email  :", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        email.place(x=530, y=40)
        self.email_entrer = Entry(self.onglet2)
        self.email_entrer.place(x=700, y=40, width=200)

        tele = Label(self.onglet2, text="Num Tel :", font=("goudy old style", 14, "bold"), fg='black', bg="#C3E2C2")
        tele.place(x=530, y=80)
        self.tele_entrer = Entry(self.onglet2)
        self.tele_entrer.place(x=700, y=80, width=200)

        self.choixp = ttk.Combobox(self.onglet2, values=("select", "Cin_tut"))
        self.choixp.place(x=530, y=160, width=100)
        self.choixp.current(0)

        self.chercherp_entrer = Entry(self.onglet2)
        self.chercherp_entrer.place(x=530, y=200)

        # les bouton-dyal parent---------------------------------------------------

        self.button = Button(self.onglet2, text="Enregistrer", command=self.inserer_parent)
        self.button.place(x=700, y=160, width=100)

        self.button = Button(self.onglet2, text="Modifier", command=self.mettre_a_jour_parent)
        self.button.place(x=750, y=230, width=100)

        self.button = Button(self.onglet2, text="Supprimer", command=self.supprimer_parent)
        self.button.place(x=900, y=230, width=100)

        self.button = Button(self.onglet2, text="Chercher", command=self.chercherp)
        self.button.place(x=530, y=240, width=200)

        self.button_affich = Button(self.onglet2, text="Actualiser", command=self.actualiserp)
        self.button_affich.place(x=870, y=160, width=100)

        # Création du treevview pour afficher les données en paternelle--------------------
        frame_treeview = ttk.Frame(self.onglet2)
        frame_treeview.place(x=0, y=280, relwidth=1, height=210)

        tree_columns = ("CIN", "Nom", "Prenom", "Adresse", "Tel", "Profession", "Email")
        self.treev = ttk.Treeview(frame_treeview, columns=tree_columns, show="headings")

        # Ajout des colonnes au Treeview
        for col in tree_columns:
            self.treev.heading(col, text=col)
            self.treev.column(col, width=100)
        self.treev.bind("<ButtonRelease-1>", self.on_treev_select)
        self.treev.pack()
        self.remplir_tab()

    # foction pour eleve
    def effacer_tableau(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def on_tree_select(self, event):
        # Récupérer l'élément sélectionné dans le Treeview
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')

        # Mettre à jour les Entry avec les valeurs sélectionnées
        self.Id_elv_entrer.delete(0, END)
        self.Id_elv_entrer.insert(0, values[0])

        self.Nom_elv_entrer.delete(0, END)
        self.Nom_elv_entrer.insert(0, values[1])

        self.prenom_entrer.delete(0, END)
        self.prenom_entrer.insert(0, values[2])

        self.date_naiss_entrer.delete(0, END)
        self.date_naiss_entrer.insert(0, values[3])

        self.lieu_naiss_entrer.delete(0, END)
        self.lieu_naiss_entrer.insert(0, values[4])

        self.sex_entrer.set(values[5])

        self.niveau_entrer.delete(0, END)
        self.niveau_entrer.insert(0, values[6])

        self.id_classe_entrer.delete(0, END)
        self.id_classe_entrer.insert(0, values[7])

        self.nationalite_entrer.delete(0, END)
        self.nationalite_entrer.insert(0, values[9])

        self.adresse_entrer.delete(0, END)
        self.adresse_entrer.insert(0, values[8])

        self.cin_entrer.delete(0, END)
        self.cin_entrer.insert(0, values[10])

    def remplir_tableau(self):

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM eleve")
            results = cursor.fetchall()
            for result in results:
                self.tree.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def connecter(self):
        connect = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ecole')
        return connect

    def inserer_eleve(self):
        # Récupérer les valeurs des champs
        code_CNE = self.Id_elv_entrer.get()
        nom = self.Nom_elv_entrer.get()
        prenom = self.prenom_entrer.get()
        date_naissance = self.date_naiss_entrer.get()
        lieu_naissance = self.lieu_naiss_entrer.get()
        sex = self.sex_entrer.get()
        niveau = self.niveau_entrer.get()
        id_classe = self.id_classe_entrer.get()

        natio = self.nationalite_entrer.get()
        adrs = self.adresse_entrer.get()
        cin = self.cin_entrer.get()

        # Exécuter la requête SQL d'insertion
        query = "INSERT INTO eleve (Id_elv, Nom_elv, Prenom_elv,Genre_elv,Adrs_elv ,Natio_elv,Date_naiss,Lieu_naiss, Niveau,Id_cls, Cin_tut) VALUES (%s,  %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"
        values = (code_CNE, nom, prenom, sex, adrs, natio, date_naissance, lieu_naissance, niveau, id_classe, cin)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Élève ajouté avec succès")

            # Vider le Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.remplir_tableau()
            # Remplir le Treeview avec les nouvelles données

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            cursor.close()

    def mettre_a_jour_eleve(self):
        # Récupérer le code CNE de l'élève à mettre à jour
        code_CNE = self.Id_elv_entrer.get()
        nom = self.Nom_elv_entrer.get()
        prenom = self.prenom_entrer.get()
        date_naissance = self.date_naiss_entrer.get()
        lieu_naissance = self.lieu_naiss_entrer.get()
        sex = self.sex_entrer.get()
        niveau = self.niveau_entrer.get()
        id_classe = self.id_classe_entrer.get()

        natio = self.nationalite_entrer.get()
        adrs = self.adresse_entrer.get()
        cin = self.cin_entrer.get()

        # Exécuter la requête SQL de mise à jour
        query = "UPDATE eleve SET Nom_elv=%s, Prenom_elv=%s, Date_naiss=%s, Lieu_naiss=%s, Genre_elv=%s, Niveau=%s, Id_cls=%s,Cin_tut=%s,Natio_elv=%s,Adrs_elv=%s WHERE Id_elv=%s"
        values = (nom, prenom, date_naissance, lieu_naissance, sex, niveau, id_classe, cin, natio, adrs, code_CNE)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Élève mis à jour avec succès")
        self.effacer_tableau()
        self.remplir_tableau()

    def supprimer_eleve(self):
        # Récupérer le code CNE de l'élève à supprimer
        code_CNE = self.Id_elv_entrer.get()

        # Exécuter la requête SQL de suppression
        query = "DELETE FROM eleve WHERE Id_elv=%s"
        values = (code_CNE,)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Élève supprimé avec succès")
        self.effacer_tableau()
        self.remplir_tableau()

    def chercher(self):

        choix = self.choix.get()
        chercher = self.chercher_entrer.get()

        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM eleve WHERE {choix} ='{chercher}'"
            cursor.execute(query)
            results = cursor.fetchall()
            if len(results) != 0:
                self.tree.delete(*self.tree.get_children())
            for result in results:
                self.tree.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    # fonction pour parn

    def effac_tableau(self):
        for item in self.treev.get_children():
            self.treev.delete(item)

    def actual(self):
        self.effacer_tableau()
        self.remplir_tableau()
    def on_treev_select(self, event):
        # Récupérer l'élément sélectionné dans le treevview
        item = self.treev.selection()[0]
        values = self.treev.item(item, 'values')

        # Mettre à jour les Entry avec les valeurs sélectionnées
        self.cine_entrer.delete(0, END)
        self.cine_entrer.insert(0, values[0])

        self.nome_entrer.delete(0, END)
        self.nome_entrer.insert(0, values[1])

        self.prenome_entrer.delete(0, END)
        self.prenome_entrer.insert(0, values[2])

        self.adress_entrer.delete(0, END)
        self.adress_entrer.insert(0, values[3])

        self.profession_entrer.delete(0, END)
        self.profession_entrer.insert(0, values[5])

        self.email_entrer.delete(0, END)
        self.email_entrer.insert(0, values[6])

        self.tele_entrer.delete(0, END)
        self.tele_entrer.insert(0, values[4])

    def remplir_tab(self):

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tuteur")
            results = cursor.fetchall()
            for result in results:
                self.treev.insert('', END, values=result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        finally:
            self.conn.commit()

    def inserer_parent(self):
        # Récupérer les valeurs des champs

        CIN = self.cine_entrer.get()
        nom = self.nome_entrer.get()
        prenom = self.prenome_entrer.get()
        profession = self.profession_entrer.get()
        email = self.email_entrer.get()
        tele = self.tele_entrer.get()
        adresse = self.adress_entrer.get()

        # Exécuter la requête SQL d'insertion
        query = "INSERT INTO tuteur (Cin_tut, Nom_tut, Prenom_tut ,Profession, Email_tut, Tele_tut, Adrs_tut) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (CIN, nom, prenom, profession, email, tele, adresse)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Tuteur ajouté avec succès")

            # Vider le Treeview
            for item in self.treev.get_children():
                self.treev.delete(item)

            # Remplir le Treeview avec les nouvelles données
            self.remplir_tab()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        self.effac_tableau()
        self.remplir_tab()

    def mettre_a_jour_parent(self):

        CIN = self.cine_entrer.get()
        nom = self.nome_entrer.get()
        prenom = self.prenome_entrer.get()
        profession = self.profession_entrer.get()
        email = self.email_entrer.get()
        tele = self.tele_entrer.get()
        adresse = self.adress_entrer.get()
        # Exécuter la requête SQL de mise à jour
        query = "UPDATE tuteur SET  Nom_tut=%s, Prenom_tut=%s, Profession=%s, Email_tut=%s, Tele_tut=%s, Adrs_tut=%s WHERE Cin_tut=%s"
        values = (nom, prenom, profession, email, tele, adresse, CIN)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Tuteur mis à jour avec succès")
        self.effac_tableau()
        self.remplir_tab()

    def supprimer_parent(self):
        # Vérifier si une ligne est sélectionnée dans le Treeview
        selected_item = self.treev.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une ligne à supprimer.")
            return

        # Récupérer le code CNE de l'élève à supprimer depuis la ligne sélectionnée
        item = self.treev.item(selected_item[0], 'values')
        self.CIN = item[0]

        # Exécuter la requête SQL de suppression
        query = "DELETE FROM tuteur WHERE Cin_tut=%s"
        values = (self.CIN,)
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        messagebox.showinfo("Success", "Tuteur supprimé avec succès")
        self.effac_tableau()
        self.remplir_tab()

    def chercherp(self):

        choixp = self.choixp.get()
        chercherp = self.chercherp_entrer.get()

        try:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM tuteur WHERE {choixp} ='{chercherp}'"
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

    def charger_cin(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT Cin_tut FROM tuteur")
        results = cursor.fetchall()
        return [classe[0] for classe in results]

    def charger_niveau(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT Niveau FROM classe ")
        results = cursor.fetchall()
        niveaux = [classe[0] for classe in results]

        if not self.niveau_entrer['values']:
            self.niveau_entrer['values'] = niveaux
            if niveaux:
                self.niveau_entrer.set(niveaux[0])

    def charger_classe(self, niveau):
        niveau = self.niveau_entrer.get()

        cursor = self.conn.cursor()
        q = f"SELECT Id_cls FROM classe WHERE Niveau =%s"

        cursor.execute(q, (niveau,))
        results = cursor.fetchall()
        return [classe[0] for classe in results]

    def votre_methode_apres_la_selection_du_niveau(self):
        self.charger_niveau()
        self.charger_classes()

    def charger_classes(self):
        niveau = self.niveau_entrer.get()
        if niveau:
            classes = self.charger_classe(niveau)
            self.id_classe_entrer['values'] = classes
            if classes:
                self.id_classe_entrer.set(classes[0])
    def actualiserp(self):
        self.effac_tableau()
        self.remplir_tab()

if __name__ == "__main__":
    window = Tk()
    window2 = Students(window)
    window.protocol("WM_DELETE_WINDOW", lambda: (window2.conn.close(), window.destroy()))
    window.mainloop()