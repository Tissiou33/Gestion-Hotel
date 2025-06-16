from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

class FenetreClient:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestion des Clients')
        self.root.geometry('1295x550+230+220')

        # Variables
        self.var_client_id = StringVar()
        self.var_nom = StringVar()
        self.var_prenom = StringVar()
        self.var_email = StringVar()
        self.var_sexe = StringVar()
        self.var_telephone = StringVar()
        self.var_adresse = StringVar()
        self.var_type_papier = StringVar()
        self.var_numero_papier = StringVar()
        self.var_date_debut = StringVar()

        # Titre
        titre = Label(self.root, text='GESTION DES CLIENTS', font=('times new roman', 18, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1295, height=50)

        # Cadre pour la saisie (à gauche)
        saisie_frame = Frame(self.root, bd=4, relief=RIDGE)
        saisie_frame.place(x=0, y=50, width=400, height=500)

        # Cadre pour l'affichage (à droite)
        affichage_frame = Frame(self.root, bd=4, relief=RIDGE)
        affichage_frame.place(x=400, y=50, width=895, height=500)

        # ==================== Partie Saisie ====================
        # Labels et Entrées
        lbl_nom = Label(saisie_frame, text='Nom:', font=('times new roman', 12, 'bold'))
        lbl_nom.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        entry_nom = ttk.Entry(saisie_frame, textvariable=self.var_nom, font=('times new roman', 12))
        entry_nom.grid(row=0, column=1, padx=10, pady=10)

        lbl_prenom = Label(saisie_frame, text='Prénom:', font=('times new roman', 12, 'bold'))
        lbl_prenom.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        entry_prenom = ttk.Entry(saisie_frame, textvariable=self.var_prenom, font=('times new roman', 12))
        entry_prenom.grid(row=1, column=1, padx=10, pady=10)

        lbl_email = Label(saisie_frame, text='Email:', font=('times new roman', 12, 'bold'))
        lbl_email.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        entry_email = ttk.Entry(saisie_frame, textvariable=self.var_email, font=('times new roman', 12))
        entry_email.grid(row=2, column=1, padx=10, pady=10)

        lbl_sexe = Label(saisie_frame, text='Sexe:', font=('times new roman', 12, 'bold'))
        lbl_sexe.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        combo_sexe = ttk.Combobox(saisie_frame, textvariable=self.var_sexe, font=('times new roman', 12), state='readonly')
        combo_sexe['values'] = ('M', 'F')
        combo_sexe.current(0)
        combo_sexe.grid(row=3, column=1, padx=10, pady=10)

        lbl_telephone = Label(saisie_frame, text='Téléphone:', font=('times new roman', 12, 'bold'))
        lbl_telephone.grid(row=4, column=0, padx=10, pady=10, sticky=W)
        entry_telephone = ttk.Entry(saisie_frame, textvariable=self.var_telephone, font=('times new roman', 12))
        entry_telephone.grid(row=4, column=1, padx=10, pady=10)

        lbl_adresse = Label(saisie_frame, text='Adresse:', font=('times new roman', 12, 'bold'))
        lbl_adresse.grid(row=5, column=0, padx=10, pady=10, sticky=W)
        entry_adresse = ttk.Entry(saisie_frame, textvariable=self.var_adresse, font=('times new roman', 12))
        entry_adresse.grid(row=5, column=1, padx=10, pady=10)

        lbl_type_papier = Label(saisie_frame, text='Type de papier:', font=('times new roman', 12, 'bold'))
        lbl_type_papier.grid(row=6, column=0, padx=10, pady=10, sticky=W)
        combo_type_papier = ttk.Combobox(saisie_frame, textvariable=self.var_type_papier, font=('times new roman', 12), state='readonly')
        combo_type_papier['values'] = ('CNI', 'Passeport', 'Permis')
        combo_type_papier.current(0)
        combo_type_papier.grid(row=6, column=1, padx=10, pady=10)

        lbl_numero_papier = Label(saisie_frame, text='Numéro de papier:', font=('times new roman', 12, 'bold'))
        lbl_numero_papier.grid(row=7, column=0, padx=10, pady=10, sticky=W)
        entry_numero_papier = ttk.Entry(saisie_frame, textvariable=self.var_numero_papier, font=('times new roman', 12))
        entry_numero_papier.grid(row=7, column=1, padx=10, pady=10)

        lbl_date_debut = Label(saisie_frame, text='Date de début:', font=('times new roman', 12, 'bold'))
        lbl_date_debut.grid(row=8, column=0, padx=10, pady=10, sticky=W)
        entry_date_debut = ttk.Entry(saisie_frame, textvariable=self.var_date_debut, font=('times new roman', 12))
        entry_date_debut.grid(row=8, column=1, padx=10, pady=10)

        # Boutons
        btn_ajouter = Button(saisie_frame, text='Ajouter', command=self.ajouter_client, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_ajouter.grid(row=9, column=0, padx=10, pady=10)

        btn_modifier = Button(saisie_frame, text='Modifier', command=self.modifier_client, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_modifier.grid(row=9, column=1, padx=10, pady=10)

        btn_supprimer = Button(saisie_frame, text='Supprimer', command=self.supprimer_client, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_supprimer.grid(row=10, column=0, padx=10, pady=10)

        btn_reinitialiser = Button(saisie_frame, text='Réinitialiser', command=self.reinitialiser, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_reinitialiser.grid(row=10, column=1, padx=10, pady=10)

        # ==================== Partie Affichage ====================
        # Tableau pour afficher les clients
        scroll_x = ttk.Scrollbar(affichage_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(affichage_frame, orient=VERTICAL)

        self.table_client = ttk.Treeview(affichage_frame, columns=('client_id', 'nom', 'prenom', 'email', 'sexe', 'telephone', 'adresse', 'type_papier', 'numero_papier', 'date_debut'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.table_client.xview)
        scroll_y.config(command=self.table_client.yview)

        self.table_client.heading('client_id', text='ID')
        self.table_client.heading('nom', text='Nom')
        self.table_client.heading('prenom', text='Prénom')
        self.table_client.heading('email', text='Email')
        self.table_client.heading('sexe', text='Sexe')
        self.table_client.heading('telephone', text='Téléphone')
        self.table_client.heading('adresse', text='Adresse')
        self.table_client.heading('type_papier', text='Type de papier')
        self.table_client.heading('numero_papier', text='Numéro de papier')
        self.table_client.heading('date_debut', text='Date de début')

        self.table_client['show'] = 'headings'

        self.table_client.column('client_id', width=50)
        self.table_client.column('nom', width=100)
        self.table_client.column('prenom', width=100)
        self.table_client.column('email', width=150)
        self.table_client.column('sexe', width=50)
        self.table_client.column('telephone', width=100)
        self.table_client.column('adresse', width=150)
        self.table_client.column('type_papier', width=100)
        self.table_client.column('numero_papier', width=100)
        self.table_client.column('date_debut', width=100)

        self.table_client.pack(fill=BOTH, expand=1)
        self.table_client.bind("<ButtonRelease-1>", self.get_cursor)

        self.afficher_clients()

    def ajouter_client(self):
        if self.var_nom.get() == '' or self.var_prenom.get() == '':
            messagebox.showerror('Erreur', 'Tous les champs doivent être remplis', parent=self.root)
        else:
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='DAMALI@\@2025',
                    database='Gestion_Reservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute(
                    'INSERT INTO client (nom, prenom, email, sexe, telephone, adresse, type_papier, numero_papier, date_debut) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (
                        self.var_nom.get(),
                        self.var_prenom.get(),
                        self.var_email.get(),
                        self.var_sexe.get(),
                        self.var_telephone.get(),
                        self.var_adresse.get(),
                        self.var_type_papier.get(),
                        self.var_numero_papier.get(),
                        self.var_date_debut.get()
                    )
                )
                conn.commit()
                self.afficher_clients()
                conn.close()
                messagebox.showinfo('Succès', 'Client ajouté avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_clients(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM client')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.table_client.delete(*self.table_client.get_children())
                for i in rows:
                    self.table_client.insert("", END, values=i)
                conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.table_client.focus()
        content = self.table_client.item(cursor_row)
        row = content["values"]

        self.var_client_id.set(row[0])
        self.var_nom.set(row[1])
        self.var_prenom.set(row[2])
        self.var_email.set(row[3])
        self.var_sexe.set(row[4])
        self.var_telephone.set(row[5])
        self.var_adresse.set(row[6])
        self.var_type_papier.set(row[7])
        self.var_numero_papier.set(row[8])
        self.var_date_debut.set(row[9])

    def modifier_client(self):
        if self.var_client_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner un client', parent=self.root)
        else:
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='DAMALI@\@2025',
                    database='Gestion_Reservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute(
                    'UPDATE client SET nom=%s, prenom=%s, email=%s, sexe=%s, telephone=%s, adresse=%s, type_papier=%s, numero_papier=%s, date_debut=%s WHERE client_id=%s',
                    (
                        self.var_nom.get(),
                        self.var_prenom.get(),
                        self.var_email.get(),
                        self.var_sexe.get(),
                        self.var_telephone.get(),
                        self.var_adresse.get(),
                        self.var_type_papier.get(),
                        self.var_numero_papier.get(),
                        self.var_date_debut.get(),
                        self.var_client_id.get()
                    )
                )
                conn.commit()
                self.afficher_clients()
                conn.close()
                messagebox.showinfo('Succès', 'Client modifié avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def supprimer_client(self):
        if self.var_client_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner un client', parent=self.root)
        else:
            try:
                confirmation = messagebox.askyesno('Confirmation', 'Voulez-vous vraiment supprimer ce client ?', parent=self.root)
                if confirmation:
                    conn = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        password='DAMALI@\@2025',
                        database='Gestion_Reservation'
                    )
                    con_cursor = conn.cursor()
                    con_cursor.execute('DELETE FROM client WHERE client_id=%s', (self.var_client_id.get(),))
                    conn.commit()
                    self.afficher_clients()
                    conn.close()
                    messagebox.showinfo('Succès', 'Client supprimé avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def reinitialiser(self):
        self.var_client_id.set('')
        self.var_nom.set('')
        self.var_prenom.set('')
        self.var_email.set('')
        self.var_sexe.set('')
        self.var_telephone.set('')
        self.var_adresse.set('')
        self.var_type_papier.set('')
        self.var_numero_papier.set('')
        self.var_date_debut.set('')

if __name__ == "__main__":
    root = Tk()
    obj = FenetreClient(root)
    root.mainloop()