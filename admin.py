from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import psycopg2

class FenetreAdmin:
    def __init__(self, root):
        self.root = root
        self.root.title('Système de Gestion Hôtelière - Admin')
        self.root.geometry('1550x800+0+0')

        # Titre
        titre = Label(self.root, text='PANEL ADMINISTRATEUR', font=('times new roman', 40, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1550, height=50)

        # Main Frame
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=50, width=1550, height=750)
        

        # Boutons
        btn_clients = Button(main_frame, text='Clients', command=self.afficher_clients, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_clients.place(x=50, y=50, width=200, height=50)

        btn_chambres = Button(main_frame, text='Chambres', command=self.afficher_chambres, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_chambres.place(x=50, y=150, width=200, height=50)

        btn_reservations = Button(main_frame, text='Réservations', command=self.afficher_reservations, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_reservations.place(x=50, y=250, width=200, height=50)

        btn_paiements = Button(main_frame, text='Paiements', command=self.afficher_paiements, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_paiements.place(x=50, y=350, width=200, height=50)

        btn_historique_clients = Button(main_frame, text='Historique Clients', command=self.afficher_historique_clients, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_historique_clients.place(x=50, y=450, width=200, height=50)

        btn_presence_employes = Button(main_frame, text='Présence Employés', command=self.afficher_presence_employes, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_presence_employes.place(x=50, y=550, width=200, height=50)

        btn_montants_jour = Button(main_frame, text='Montants Versés', command=self.afficher_montants_jour, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_montants_jour.place(x=50, y=650, width=200, height=50)

        # Nouveaux boutons pour les plats et les boissons
        btn_plats = Button(main_frame, text='Plats', command=self.afficher_plats, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_plats.place(x=300, y=50, width=200, height=50)

        btn_boissons = Button(main_frame, text='Boissons', command=self.afficher_boissons, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_boissons.place(x=300, y=150, width=200, height=50)

        # Boutons pour ajouter des plats et des boissons
        btn_ajouter_plat = Button(main_frame, text='Ajouter Plat', command=self.ajouter_plat, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_ajouter_plat.place(x=300, y=250, width=200, height=50)

        btn_ajouter_boisson = Button(main_frame, text='Ajouter Boisson', command=self.ajouter_boisson, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_ajouter_boisson.place(x=300, y=350, width=200, height=50)

    def afficher_plats(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM plat')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.afficher_table(rows, ['ID', 'Nom', 'Type', 'Origine', 'Prix'])
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_boissons(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM boisson')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.afficher_table(rows, ['ID', 'Nom', 'Prix'])
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def ajouter_plat(self):
        nom = simpledialog.askstring("Ajouter un plat", "Nom du plat:", parent=self.root)
        if nom:
            type_plat = simpledialog.askstring("Ajouter un plat", "Type du plat (P, R, D, F):", parent=self.root)
            origine = simpledialog.askstring("Ajouter un plat", "Origine (Afrique, Europe, Asie, Viande):", parent=self.root)
            prix = simpledialog.askfloat("Ajouter un plat", "Prix du plat:", parent=self.root)
            if type_plat and origine and prix:
                try:
                    conn = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        password='DAMALI@\@2025',
                        database='Gestion_Reservation'
                    )
                    con_cursor = conn.cursor()
                    con_cursor.execute(
                        'INSERT INTO plat (nom, type, origine, plat_prix) VALUES (%s, %s, %s, %s)',
                        (nom, type_plat, origine, prix)
                    )
                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Succès', 'Plat ajouté avec succès', parent=self.root)
                    self.afficher_plats()
                except Exception as es:
                    messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def ajouter_boisson(self):
        nom = simpledialog.askstring("Ajouter une boisson", "Nom de la boisson:", parent=self.root)
        if nom:
            prix = simpledialog.askfloat("Ajouter une boisson", "Prix de la boisson:", parent=self.root)
            if prix:
                try:
                    conn = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        password='DAMALI@\@2025',
                        database='Gestion_Reservation'
                    )
                    con_cursor = conn.cursor()
                    con_cursor.execute(
                        'INSERT INTO boisson (nom, prix) VALUES (%s, %s)',
                        (nom, prix)
                    )
                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Succès', 'Boisson ajoutée avec succès', parent=self.root)
                    self.afficher_boissons()
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
                self.afficher_table(rows, ['ID', 'Nom', 'Prénom', 'Email', 'Numéro', 'Téléphone', 'Adresse', 'Type de papier', 'Numéro de papier', 'Date de début'])
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_chambres(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM chambre')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.afficher_table(rows, ['ID', 'Numéro', 'Type', 'État', 'Prix', 'Capacité', 'Classe'])
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_reservations(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM reservation_chambre')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.afficher_table(rows, ['ID', 'ID Client', 'ID Chambre', 'Date de début', 'Nombre de jours', 'Date de départ', 'Prix'])
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_paiements(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM payement')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.afficher_table(rows, ['ID', 'Table Concernée', 'ID Chambre', 'ID Client', 'Type de Paiement', 'Prix Total'])
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_historique_clients(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM clients_historique')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.afficher_table(rows, ['ID Client', 'Nom', 'Prénom', 'Email', 'Numéro', 'Téléphone', 'Adresse', 'Type de Papier', 'Date de Début'])
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_presence_employes(self):
        try:
            date = simpledialog.askstring("Date", "Entrez la date (AAAA-MM-JJ):", parent=self.root)
            if date:
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='DAMALI@\@2025',
                    database='Gestion_Reservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute('SELECT * FROM presence WHERE date_entree = %s', (date,))
                rows = con_cursor.fetchall()
                if len(rows) != 0:
                    self.afficher_table(rows, ['ID', 'ID Employé', 'Date Entrée', 'Date Sortie'])
                else:
                    messagebox.showinfo('Information', 'Aucun employé présent à cette date.', parent=self.root)
                conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_montants_jour(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT date_creation, SUM(prix_total) FROM payement GROUP BY date_creation')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.afficher_table(rows, ['Date', 'Montant Total'])
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_table(self, rows, colonnes):
        fenetre_table = Toplevel(self.root)
        fenetre_table.title('Tableau des données')
        fenetre_table.geometry('800x400')

        scroll_x = ttk.Scrollbar(fenetre_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(fenetre_table, orient=VERTICAL)

        table = ttk.Treeview(fenetre_table, columns=colonnes, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=table.xview)
        scroll_y.config(command=table.yview)

        for col in colonnes:
            table.heading(col, text=col)
            table.column(col, width=100)

        table['show'] = 'headings'

        for row in rows:
            table.insert("", END, values=row)

        table.pack(fill=BOTH, expand=1)

    # Les autres méthodes restent inchangées...

if __name__ == "__main__":
    root = Tk()
    obj = FenetreAdmin(root)
    root.mainloop()