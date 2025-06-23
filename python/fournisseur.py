from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

class FenetreFournisseur:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestion des Fournisseurs')
        self.root.geometry('1295x550+230+220')

        # Variables
        self.var_fournisseur_id = StringVar()
        self.var_nom = StringVar()
        self.var_adresse = StringVar()
        self.var_telephone = StringVar()
        self.var_email = StringVar()

        # Titre
        titre = Label(self.root, text='GESTION DES FOURNISSEURS', font=('times new roman', 18, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1295, height=50)

        # Main Frame
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=50, width=1295, height=500)

        # Labels et Entrées
        lbl_nom = Label(main_frame, text='Nom:', font=('times new roman', 12, 'bold'))
        lbl_nom.grid(row=0, column=0, padx=10, pady=10)
        entry_nom = ttk.Entry(main_frame, textvariable=self.var_nom, font=('times new roman', 12))
        entry_nom.grid(row=0, column=1, padx=10, pady=10)

        lbl_adresse = Label(main_frame, text='Adresse:', font=('times new roman', 12, 'bold'))
        lbl_adresse.grid(row=1, column=0, padx=10, pady=10)
        entry_adresse = ttk.Entry(main_frame, textvariable=self.var_adresse, font=('times new roman', 12))
        entry_adresse.grid(row=1, column=1, padx=10, pady=10)

        lbl_telephone = Label(main_frame, text='Téléphone:', font=('times new roman', 12, 'bold'))
        lbl_telephone.grid(row=2, column=0, padx=10, pady=10)
        entry_telephone = ttk.Entry(main_frame, textvariable=self.var_telephone, font=('times new roman', 12))
        entry_telephone.grid(row=2, column=1, padx=10, pady=10)

        lbl_email = Label(main_frame, text='Email:', font=('times new roman', 12, 'bold'))
        lbl_email.grid(row=3, column=0, padx=10, pady=10)
        entry_email = ttk.Entry(main_frame, textvariable=self.var_email, font=('times new roman', 12))
        entry_email.grid(row=3, column=1, padx=10, pady=10)

        # Boutons
        btn_ajouter = Button(main_frame, text='Ajouter', command=self.ajouter_fournisseur, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_ajouter.grid(row=4, column=0, padx=10, pady=10)

        btn_modifier = Button(main_frame, text='Modifier', command=self.modifier_fournisseur, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_modifier.grid(row=4, column=1, padx=10, pady=10)

        btn_supprimer = Button(main_frame, text='Supprimer', command=self.supprimer_fournisseur, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_supprimer.grid(row=4, column=2, padx=10, pady=10)

        btn_reinitialiser = Button(main_frame, text='Réinitialiser', command=self.reinitialiser, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_reinitialiser.grid(row=4, column=3, padx=10, pady=10)

        # Tableau
        table_frame = Frame(main_frame, bd=4, relief=RIDGE)
        table_frame.place(x=10, y=300, width=1270, height=180)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.table_fournisseur = ttk.Treeview(table_frame, columns=('fournisseur_id', 'nom', 'adresse', 'telephone', 'email'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.table_fournisseur.xview)
        scroll_y.config(command=self.table_fournisseur.yview)

        self.table_fournisseur.heading('fournisseur_id', text='ID')
        self.table_fournisseur.heading('nom', text='Nom')
        self.table_fournisseur.heading('adresse', text='Adresse')
        self.table_fournisseur.heading('telephone', text='Téléphone')
        self.table_fournisseur.heading('email', text='Email')

        self.table_fournisseur['show'] = 'headings'

        self.table_fournisseur.column('fournisseur_id', width=50)
        self.table_fournisseur.column('nom', width=100)
        self.table_fournisseur.column('adresse', width=150)
        self.table_fournisseur.column('telephone', width=100)
        self.table_fournisseur.column('email', width=150)

        self.table_fournisseur.pack(fill=BOTH, expand=1)
        self.table_fournisseur.bind("<ButtonRelease-1>", self.get_cursor)

        self.afficher_fournisseurs()

    def ajouter_fournisseur(self):
        if self.var_nom.get() == '' or self.var_adresse.get() == '':
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
                    'INSERT INTO fournisseur (nom, adresse, telephone, email) VALUES (%s, %s, %s, %s)',
                    (
                        self.var_nom.get(),
                        self.var_adresse.get(),
                        self.var_telephone.get(),
                        self.var_email.get()
                    )
                )
                conn.commit()
                self.afficher_fournisseurs()
                conn.close()
                messagebox.showinfo('Succès', 'Fournisseur ajouté avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_fournisseurs(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='******',
                database='GestionReservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM fournisseur')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.table_fournisseur.delete(*self.table_fournisseur.get_children())
                for i in rows:
                    self.table_fournisseur.insert("", END, values=i)
                conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.table_fournisseur.focus()
        content = self.table_fournisseur.item(cursor_row)
        row = content["values"]

        self.var_fournisseur_id.set(row[0])
        self.var_nom.set(row[1])
        self.var_adresse.set(row[2])
        self.var_telephone.set(row[3])
        self.var_email.set(row[4])

    def modifier_fournisseur(self):
        if self.var_fournisseur_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner un fournisseur', parent=self.root)
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
                    'UPDATE fournisseur SET nom=%s, adresse=%s, telephone=%s, email=%s WHERE fournisseur_id=%s',
                    (
                        self.var_nom.get(),
                        self.var_adresse.get(),
                        self.var_telephone.get(),
                        self.var_email.get(),
                        self.var_fournisseur_id.get()
                    )
                )
                conn.commit()
                self.afficher_fournisseurs()
                conn.close()
                messagebox.showinfo('Succès', 'Fournisseur modifié avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def supprimer_fournisseur(self):
        if self.var_fournisseur_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner un fournisseur', parent=self.root)
        else:
            try:
                confirmation = messagebox.askyesno('Confirmation', 'Voulez-vous vraiment supprimer ce fournisseur ?', parent=self.root)
                if confirmation:
                    conn = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        password='******',
                        database='GestionReservation'
                    )
                    con_cursor = conn.cursor()
                    con_cursor.execute('DELETE FROM fournisseur WHERE fournisseur_id=%s', (self.var_fournisseur_id.get(),))
                    conn.commit()
                    self.afficher_fournisseurs()
                    conn.close()
                    messagebox.showinfo('Succès', 'Fournisseur supprimé avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def reinitialiser(self):
        self.var_fournisseur_id.set('')
        self.var_nom.set('')
        self.var_adresse.set('')
        self.var_telephone.set('')
        self.var_email.set('')

if __name__ == "__main__":
    root = Tk()
    obj = FenetreFournisseur(root)
    root.mainloop()
