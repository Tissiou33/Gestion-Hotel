from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

class FenetreChambre:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestion des Chambres')
        self.root.geometry('1295x550+230+220')

        # Variables
        self.var_chambre_id = StringVar()
        self.var_numero = StringVar()
        self.var_type_chambre_id = StringVar()  #champ pour le type de chambre (entier)
        self.var_etage = StringVar()  # champ pour l'étage
        self.var_statut = StringVar()  # champ pour le statut

        # Titre
        titre = Label(self.root, text='GESTION DES CHAMBRES', font=('times new roman', 18, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1295, height=50)

        # Cadre pour la saisie (à gauche)
        saisie_frame = Frame(self.root, bd=4, relief=RIDGE)
        saisie_frame.place(x=0, y=50, width=400, height=500)

        # Cadre pour l'affichage (à droite)
        affichage_frame = Frame(self.root, bd=4, relief=RIDGE)
        affichage_frame.place(x=400, y=50, width=895, height=500)

        # ==================== Partie Saisie ====================
        # Labels et Entrées
        lbl_numero = Label(saisie_frame, text='Numéro:', font=('times new roman', 12, 'bold'))
        lbl_numero.grid(row=0, column=0, padx=10, pady=10)
        entry_numero = ttk.Entry(saisie_frame, textvariable=self.var_numero, font=('times new roman', 12))
        entry_numero.grid(row=0, column=1, padx=10, pady=10)

        lbl_type_chambre = Label(saisie_frame, text='Type de chambre:', font=('times new roman', 12, 'bold'))
        lbl_type_chambre.grid(row=1, column=0, padx=10, pady=10)
        self.combo_type_chambre = ttk.Combobox(saisie_frame, textvariable=self.var_type_chambre_id, font=('times new roman', 12), state='readonly')
        # Remplir le Combobox avec les IDs de type_chambre (entiers)
        self.combo_type_chambre['values'] = self.get_type_chambre_ids()  # Récupére les IDs de la base de données
        self.combo_type_chambre.grid(row=1, column=1, padx=10, pady=10)
        self.combo_type_chambre.current(0)

        lbl_etage = Label(saisie_frame, text='Étage (1-7):', font=('times new roman', 12, 'bold'))
        lbl_etage.grid(row=2, column=0, padx=10, pady=10)
        entry_etage = ttk.Entry(saisie_frame, textvariable=self.var_etage, font=('times new roman', 12))
        entry_etage.grid(row=2, column=1, padx=10, pady=10)

        lbl_statut = Label(saisie_frame, text='Statut:', font=('times new roman', 12, 'bold'))
        lbl_statut.grid(row=3, column=0, padx=10, pady=10)
        self.combo_statut = ttk.Combobox(saisie_frame, textvariable=self.var_statut, font=('times new roman', 12), state='readonly')
        self.combo_statut['values'] = ('vaccant', 'occupée', 'maintenance')  # Valeurs possibles
        self.combo_statut.grid(row=3, column=1, padx=10, pady=10)
        self.combo_statut.current(0)

        # Boutons
        btn_ajouter = Button(saisie_frame, text='Ajouter', command=self.ajouter_chambre, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_ajouter.grid(row=4, column=0, padx=10, pady=10)

        btn_modifier = Button(saisie_frame, text='Modifier', command=self.modifier_chambre, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_modifier.grid(row=4, column=1, padx=10, pady=10)

        btn_supprimer = Button(saisie_frame, text='Supprimer', command=self.supprimer_chambre, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_supprimer.grid(row=5, column=0, padx=10, pady=10)

        btn_reinitialiser = Button(saisie_frame, text='Réinitialiser', command=self.reinitialiser, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_reinitialiser.grid(row=5, column=1, padx=10, pady=10)

        # ==================== Partie Affichage ====================
        # Tableau pour afficher les chambres
        scroll_x = ttk.Scrollbar(affichage_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(affichage_frame, orient=VERTICAL)

        self.table_chambre = ttk.Treeview(affichage_frame, columns=(
            'chambre_id', 'numero', 'type_chambre', 'capacite', 'prix', 'etage', 'statut'
        ), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.table_chambre.xview)
        scroll_y.config(command=self.table_chambre.yview)

        # En-têtes du tableau
        self.table_chambre.heading('chambre_id', text='ID')
        self.table_chambre.heading('numero', text='Numéro')
        self.table_chambre.heading('type_chambre', text='Type de chambre')
        self.table_chambre.heading('capacite', text='Capacité')
        self.table_chambre.heading('prix', text='Prix')
        self.table_chambre.heading('etage', text='Étage')
        self.table_chambre.heading('statut', text='Statut')

        self.table_chambre['show'] = 'headings'

        # Largeur des colonnes
        self.table_chambre.column('chambre_id', width=50)
        self.table_chambre.column('numero', width=100)
        self.table_chambre.column('type_chambre', width=150)
        self.table_chambre.column('capacite', width=100)
        self.table_chambre.column('prix', width=100)
        self.table_chambre.column('etage', width=100)
        self.table_chambre.column('statut', width=100)

        self.table_chambre.pack(fill=BOTH, expand=1)
        self.table_chambre.bind("<ButtonRelease-1>", self.get_cursor)

        self.afficher_chambres()

    def get_type_chambre_ids(self):
        """Récupère les IDs de type_chambre depuis la base de données."""
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='******',
                database='GestionReservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT type_chambre_id FROM type_chambre')
            rows = con_cursor.fetchall()
            conn.close()
            # Retourne une liste d'IDs (entiers)
            return [row[0] for row in rows]
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)
            return []

    def ajouter_chambre(self):
        if self.var_numero.get() == '' or self.var_type_chambre_id.get() == '' or self.var_etage.get() == '' or self.var_statut.get() == '':
            messagebox.showerror('Erreur', 'Tous les champs doivent être remplis', parent=self.root)
        else:
            try:
                etage = int(self.var_etage.get())
                if etage < 1 or etage > 7:
                    messagebox.showerror('Erreur', 'L\'étage doit être compris entre 1 et 7', parent=self.root)
                    return

                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='******',
                    database='GestionReservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute(
                    'INSERT INTO chambre (numero, type_chambre_id, etage, statut) VALUES (%s, %s, %s, %s)',
                    (
                        self.var_numero.get(),
                        int(self.var_type_chambre_id.get()),  # Convertir en entier
                        etage,  # Étage validé
                        self.var_statut.get()
                    )
                )
                conn.commit()
                self.afficher_chambres()
                conn.close()
                messagebox.showinfo('Succès', 'Chambre ajoutée avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_chambres(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='******',
                database='GestionReservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('''
                SELECT c.chambre_id, c.numero, t.nom, t.capacite, t.prix, c.etage, c.statut
                FROM chambre c
                JOIN type_chambre t ON c.type_chambre_id = t.type_chambre_id
            ''')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.table_chambre.delete(*self.table_chambre.get_children())
                for i in rows:
                    self.table_chambre.insert("", END, values=i)
                conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.table_chambre.focus()
        content = self.table_chambre.item(cursor_row)
        row = content["values"]

        self.var_chambre_id.set(row[0])
        self.var_numero.set(row[1])
        self.var_type_chambre_id.set(row[2])  # Affiche le nom du type de chambre
        self.var_etage.set(row[5])
        self.var_statut.set(row[6])

    def modifier_chambre(self):
        if self.var_chambre_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner une chambre', parent=self.root)
        else:
            try:
                etage = int(self.var_etage.get())
                if etage < 1 or etage > 7:
                    messagebox.showerror('Erreur', 'L\'étage doit être compris entre 1 et 7', parent=self.root)
                    return

                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='******',
                    database='GestionReservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute(
                    'UPDATE chambre SET numero=%s, type_chambre_id=%s, etage=%s, statut=%s WHERE chambre_id=%s',
                    (
                        self.var_numero.get(),
                        int(self.var_type_chambre_id.get()),  # Convertir en entier
                        etage,  # Étage validé
                        self.var_statut.get(),
                        self.var_chambre_id.get()
                    )
                )
                conn.commit()
                self.afficher_chambres()
                conn.close()
                messagebox.showinfo('Succès', 'Chambre modifiée avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def supprimer_chambre(self):
        if self.var_chambre_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner une chambre', parent=self.root)
        else:
            try:
                confirmation = messagebox.askyesno('Confirmation', 'Voulez-vous vraiment supprimer cette chambre ?', parent=self.root)
                if confirmation:
                    conn = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        password='******',
                        database='GestionReservation'
                    )
                    con_cursor = conn.cursor()
                    con_cursor.execute('DELETE FROM chambre WHERE chambre_id=%s', (self.var_chambre_id.get(),))
                    conn.commit()
                    self.afficher_chambres()
                    conn.close()
                    messagebox.showinfo('Succès', 'Chambre supprimée avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def reinitialiser(self):
        self.var_chambre_id.set('')
        self.var_numero.set('')
        self.var_type_chambre_id.set('')
        self.var_etage.set('')
        self.var_statut.set('')

if __name__ == "__main__":
    root = Tk()
    obj = FenetreChambre(root)
    root.mainloop()
