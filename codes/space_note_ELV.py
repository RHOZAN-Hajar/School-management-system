from tkinter import *
from tkinter import ttk
from tkinter import ttk, messagebox
import mysql.connector as mysql


class Evaluation_elv:
    
    def __init__(self, root,student_id):
        self.root = root
        self.student_id = student_id 
        # self.root.geometry("1920*1080+0+0")
        self.root.title("gestion d'une ecole privee ")
        self.title = Label(self.root, text="Gestion des Evaluations", font=("times new roman", 40, "bold"), bg='#010c48',
                      fg='white').place(x=0, y=0, relwidth=1, height=70)
        self.root.geometry("1100x500+220+130")

        self.searchby = StringVar()
        self.searchtxt = StringVar()

        self.var_eva_date = StringVar()
        self.var_nommat = StringVar()
        self.var_eva_note = StringVar()
        self.var_Niveau = StringVar()


        

        self.lbl_clock = Label(self.root, text="\t\t Date: DD-MM-YYYY\t\t Temps: HH:MM:SS ")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        eva_frame = Frame(self.root, bd=3, relief=RIDGE)
        eva_frame.place(x=0, y=80, relwidth=1, height=1000)

        scrolly = Scrollbar(eva_frame, orient=VERTICAL)
        scrollx = Scrollbar(eva_frame, orient=HORIZONTAL)

        self.EvaluationTable = ttk.Treeview(eva_frame, columns=(
       "Date_eval", "Nom_mat", "Note_eval", "Niveau"), yscrollcommand=scrolly.set,
                                            xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EvaluationTable.xview)
        scrolly.config(command=self.EvaluationTable.yview)

        self.EvaluationTable.heading("Date_eval", text="Date de l'evaluation")
        self.EvaluationTable.heading("Nom_mat", text="Nom mat")
        self.EvaluationTable.heading("Note_eval", text="Note de l'evaluation")
        self.EvaluationTable.heading("Niveau", text="Niveau de classe")

        self.EvaluationTable["show"] = "headings"

        self.EvaluationTable.column("Date_eval", width=100)
        self.EvaluationTable.column("Nom_mat", width=100)
        self.EvaluationTable.column("Note_eval", width=100)
        self.EvaluationTable.column("Niveau", width=100)

        self.EvaluationTable.pack(fill=BOTH, expand=1)
        # bach katkhtar mn list lta7t achno bghiti y3amro beh les infos f case
        self.EvaluationTable.bind("<ButtonRelease-1>",self.get_cursor)

        self.affichage()

    def affichage(self):
        con = mysql.connect(host='127.0.0.1', user='root', password='', port='3306', database='ecole prive')
        cur = con.cursor()
        cur.execute(f"SELECT ev.Date_eval, m.Nom_mat, ev.Note_eval,e.Niveau "
                    f"FROM evaluation ev "
                    f"JOIN eleve e ON ev.Id_elv = e.Id_elv "
                    f"JOIN matiere m ON ev.Code_mat = m.Code_mat "
        
              
                    f"WHERE e.Id_elv = '{self.student_id}' "
                    f"ORDER BY ev.Date_eval")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.EvaluationTable.delete(*self.EvaluationTable.get_children())
            for i in rows:
                self.EvaluationTable.insert("", END, values=i)
            con.commit()
        con.close()

    # bach katkhtar mn list lta7t achno bghiti y3amro beh les infos f case
    def get_cursor(self, event=""):
        cursor_row = self.EvaluationTable.focus()
        content = self.EvaluationTable.item(cursor_row)
        row = content["values"]
        self.var_eva_date.set(row[0])
        self.var_nommat.set(row[1])
        self.var_eva_note.set(row[2])
        self.var_Niveau.set(row[3])




if __name__ == "__main__":
    root = Tk()
    student_id = "your_student_id_here"  # Replace with the actual student_id
    obj4 = Evaluation_elv(root, student_id)
    root.mainloop()


