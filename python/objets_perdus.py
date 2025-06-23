from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

class FenetreObjetsPerdus:
    def __init__(self, root):
        self.root = root
        self.root.title('Objets Perdus')
        self.root.geometry('1295x550+230+220')

        # Variables
        self.var_objet_id = StringVar()
        self.var_description = StringVar()
        self.var_personnel_id = StringVar()

        # Titre
        titre = Label(self.root, text='OBJETS PERDUS', font=('times new roman', 18, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1295, height=50)

        # Cadre pour la saisie (à gauche)
        saisie_frame = Frame(self.root, bd=4, relief=RIDGE)
        saisie_frame.place(x=0, y=50, width=400, height=500)

        # Cadre pour l'affichage (à droite)
        affichage_frame = Frame(self.root, bd=4, relief=RIDGE)
        affichage_frame.place(x=400, y=50, width=895, height=500)

        # ==================== Partie Saisie ====================
        # Labels et Entrées
        lbl_description = Label(saisie_frame, text='Description:', font=('times new roman', 12, 'bold'))
        lbl_description.grid(row=0, column=0, padx=10, pady=10)
        entry_description = ttk.Entry(saisie_frame, textvariable=self.var_description, font=('times new roman', 12))
        entry_description.grid(row=0, column=1, padx=10, pady=10)

        lbl_personnel_id = Label(saisie_frame, text='ID Personnel:', font=('times new roman', 12, 'bold'))
        lbl_personnel_id.grid(row=1, column=0, padx=10, pady=10)
        entry_personnel_id = ttk.Entry(saisie_frame, textvariable=self.var_personnel_id, font=('times new roman', 12))
        entry_personnel_id.grid(row=1, column=1, padx=10, pady=10)

        # Boutons
        btn_ajouter = Button(saisie_frame, text='Ajouter', command=self.ajouter_objet, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_ajouter.grid(row=2, column=0, padx=10, pady=10)

        btn_modifier = Button(saisie_frame, text='Modifier', command=self.modifier_objet, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_modifier.grid(row=2, column=1, padx=10, pady=10)

        btn_supprimer = Button(saisie_frame, text='Supprimer', command=self.supprimer_objet, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_supprimer.grid(row=2, column=2, padx=10, pady=10)

        btn_reinitialiser = Button(saisie_frame, text='Réinitialiser', command=self.reinitialiser, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_reinitialiser.grid(row=2, column=3, padx=10, pady=10)

        # ==================== Partie Affichage ====================
        # Tableau pour afficher les objets perdus
        scroll_x = ttk.Scrollbar(affichage_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(affichage_frame, orient=VERTICAL)

        self.table_objet = ttk.Treeview(affichage_frame, columns=('objet_id', 'personnel_id','description'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.table_objet.xview)
        scroll_y.config(command=self.table_objet.yview)

        self.table_objet.heading('objet_id', text='ID')
        self.table_objet.heading('personnel_id', text='ID Personnel')
        self.table_objet.heading('description', text='Description')

        self.table_objet['show'] = 'headings'

        self.table_objet.column('objet_id', width=50)
        self.table_objet.column('personnel_id', width=200)
        self.table_objet.column('description', width=100)

        self.table_objet.pack(fill=BOTH, expand=1)
        self.table_objet.bind("<ButtonRelease-1>", self.get_cursor)

        self.afficher_objets()

    def ajouter_objet(self):
        if self.var_description.get() == '' or self.var_personnel_id.get() == '':
            messagebox.showerror('Erreur', 'Tous les champs doivent être remplis', parent=self.root)
        else:
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='******',
                    database='GestionReservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute(
                    'INSERT INTO objet_perdus (description, employe_id) VALUES (%s, %s)',
                    (
                        self.var_description.get(),
                        self.var_personnel_id.get()
                    )
                )
                conn.commit()
                self.afficher_objets()
                conn.close()
                messagebox.showinfo('Succès', 'Objet ajouté avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_objets(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='******',
                database='GestionReservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM objet_perdus')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.table_objet.delete(*self.table_objet.get_children())
                for i in rows:
                    self.table_objet.insert("", END, values=i)
                conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.table_objet.focus()
        content = self.table_objet.item(cursor_row)
        row = content["values"]

        self.var_objet_id.set(row[0])
        self.var_description.set(row[2])
        self.var_personnel_id.set(row[1])

    def modifier_objet(self):
        if self.var_objet_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner un objet', parent=self.root)
        else:
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='******',
                    database='Gestion_Reservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute(
                    'UPDATE objet_perdus SET description=%s, employe_id=%s WHERE objet_id=%s',
                    (
                        self.var_description.get(),
                        self.var_personnel_id.get(),
                        self.var_objet_id.get()
                    )
                )
                conn.commit()
                self.afficher_objets()
                conn.close()
                messagebox.showinfo('Succès', 'Objet modifié avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def supprimer_objet(self):
        if self.var_objet_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner un objet', parent=self.root)
        else:
            try:
                confirmation = messagebox.askyesno('Confirmation', 'Voulez-vous vraiment supprimer cet objet ?', parent=self.root)
                if confirmation:
                    conn = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        password='******',
                        database='GestionReservation'
                    )
                    con_cursor = conn.cursor()
                    con_cursor.execute('DELETE FROM objet_perdus WHERE id_objet=%s', (self.var_objet_id.get(),))
                    conn.commit()
                    self.afficher_objets()
                    conn.close()
                    messagebox.showinfo('Succès', 'Objet supprimé avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def reinitialiser(self):
        self.var_objet_id.set('')
        self.var_description.set('')
        self.var_personnel_id.set('')

if __name__ == "__main__":
    root = Tk()
    obj = FenetreObjetsPerdus(root)
    root.mainloop()
