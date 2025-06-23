from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from fpdf import FPDF  # Bibliothèque pour générer des PDFs

class FenetreReservationSalle:
    def __init__(self, root):
        self.root = root
        self.root.title('Réservation de Salle')
        self.root.geometry('1295x550+230+220')

        # Variables
        self.var_identifiant = StringVar()
        self.var_salle_id = StringVar()
        self.var_client_id = StringVar()
        self.var_nb_heure = StringVar()
        self.var_taxe = StringVar()
        self.var_type_paiement = StringVar()
        self.var_date = StringVar()  # Nouvelle variable pour la date

        # Titre
        titre = Label(self.root, text='RÉSERVATION DE SALLE', font=('times new roman', 18, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1295, height=50)

        # Cadre pour la saisie (à gauche)
        saisie_frame = Frame(self.root, bd=4, relief=RIDGE)
        saisie_frame.place(x=0, y=50, width=400, height=500)

        # Cadre pour l'affichage (à droite)
        affichage_frame = Frame(self.root, bd=4, relief=RIDGE)
        affichage_frame.place(x=400, y=50, width=895, height=500)

        # ==================== Partie Saisie ====================
        # Labels et Entrées
        lbl_salle_id = Label(saisie_frame, text='ID Salle:', font=('times new roman', 12, 'bold'))
        lbl_salle_id.grid(row=0, column=0, padx=10, pady=10)
        entry_salle_id = ttk.Entry(saisie_frame, textvariable=self.var_salle_id, font=('times new roman', 12))
        entry_salle_id.grid(row=0, column=1, padx=10, pady=10)

        lbl_client_id = Label(saisie_frame, text='ID Client:', font=('times new roman', 12, 'bold'))
        lbl_client_id.grid(row=1, column=0, padx=10, pady=10)
        entry_client_id = ttk.Entry(saisie_frame, textvariable=self.var_client_id, font=('times new roman', 12))
        entry_client_id.grid(row=1, column=1, padx=10, pady=10)

        lbl_nb_heure = Label(saisie_frame, text='Nombre d\'heures:', font=('times new roman', 12, 'bold'))
        lbl_nb_heure.grid(row=2, column=0, padx=10, pady=10)
        entry_nb_heure = ttk.Entry(saisie_frame, textvariable=self.var_nb_heure, font=('times new roman', 12))
        entry_nb_heure.grid(row=2, column=1, padx=10, pady=10)

        lbl_taxe = Label(saisie_frame, text='Taxe:', font=('times new roman', 12, 'bold'))
        lbl_taxe.grid(row=3, column=0, padx=10, pady=10)
        entry_taxe = ttk.Entry(saisie_frame, textvariable=self.var_taxe, font=('times new roman', 12))
        entry_taxe.grid(row=3, column=1, padx=10, pady=10)

        # Nouveau champ pour la date
        lbl_date = Label(saisie_frame, text='Date (AAAA-MM-JJ):', font=('times new roman', 12, 'bold'))
        lbl_date.grid(row=4, column=0, padx=10, pady=10)
        entry_date = ttk.Entry(saisie_frame, textvariable=self.var_date, font=('times new roman', 12))
        entry_date.grid(row=4, column=1, padx=10, pady=10)

        # Label pour le type de paiement
        lbl_type_paiement = Label(saisie_frame, text='Type de paiement:', font=('times new roman', 12, 'bold'))
        lbl_type_paiement.grid(row=5, column=0, padx=10, pady=10)
        
        # Menu déroulant pour le type de paiement
        self.var_type_paiement = StringVar()
        combo_type_paiement = ttk.Combobox(saisie_frame, textvariable=self.var_type_paiement, font=('times new roman', 12), state='readonly')
        combo_type_paiement['values'] = ('Virement', 'Espèce', 'Crypto')  # Options disponibles
        combo_type_paiement.grid(row=5, column=1, padx=10, pady=10)
        combo_type_paiement.current(0)  # Définir la première option comme sélectionnée par défaut

        # Boutons
        btn_ajouter = Button(saisie_frame, text='Ajouter', command=self.ajouter_reservation, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_ajouter.grid(row=6, column=0, padx=10, pady=10)

        btn_modifier = Button(saisie_frame, text='Modifier', command=self.modifier_reservation, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_modifier.grid(row=6, column=1, padx=10, pady=10)

        btn_supprimer = Button(saisie_frame, text='Supprimer', command=self.supprimer_reservation, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_supprimer.grid(row=8, column=0, padx=10, pady=10)

        btn_reinitialiser = Button(saisie_frame, text='Réinitialiser', command=self.reinitialiser, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_reinitialiser.grid(row=8, column=1, padx=10, pady=10)

        # Bouton pour imprimer le reçu en PDF
        btn_imprimer = Button(saisie_frame, text='Imprimer Reçu', command=self.imprimer_recu, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_imprimer.grid(row=7, column=0, padx=10, pady=10)

        # Bouton pour rechercher par date
        btn_rechercher_date = Button(saisie_frame, text='Rechercher par Date', command=self.rechercher_par_date, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_rechercher_date.grid(row=7, column=1, padx=10, pady=10)

        # ==================== Partie Affichage ====================
        # Tableau pour afficher les réservations
        scroll_x = ttk.Scrollbar(affichage_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(affichage_frame, orient=VERTICAL)

        self.table_reservation = ttk.Treeview(affichage_frame, columns=('identifiant', 'salle_id', 'nom_salle', 'client_id', 'nom_client', 'prenom_client', 'telephone_client', 'nb_heure', 'taxe', 'prix_total', 'type_paiement', 'date'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.table_reservation.xview)
        scroll_y.config(command=self.table_reservation.yview)

        self.table_reservation.heading('identifiant', text='ID')
        self.table_reservation.heading('salle_id', text='ID Salle')
        self.table_reservation.heading('nom_salle', text='Nom Salle')
        self.table_reservation.heading('client_id', text='ID Client')
        self.table_reservation.heading('nom_client', text='Nom Client')
        self.table_reservation.heading('prenom_client', text='Prénom Client')
        self.table_reservation.heading('telephone_client', text='Téléphone Client')
        self.table_reservation.heading('nb_heure', text='Nombre d\'heures')
        self.table_reservation.heading('taxe', text='Taxe')
        self.table_reservation.heading('prix_total', text='Prix Total')
        self.table_reservation.heading('type_paiement', text='Type de Paiement')
        self.table_reservation.heading('date', text='Date')

        self.table_reservation['show'] = 'headings'

        self.table_reservation.column('identifiant', width=50)
        self.table_reservation.column('salle_id', width=100)
        self.table_reservation.column('nom_salle', width=100)
        self.table_reservation.column('client_id', width=100)
        self.table_reservation.column('nom_client', width=100)
        self.table_reservation.column('prenom_client', width=100)
        self.table_reservation.column('telephone_client', width=100)
        self.table_reservation.column('nb_heure', width=100)
        self.table_reservation.column('taxe', width=100)
        self.table_reservation.column('prix_total', width=100)
        self.table_reservation.column('type_paiement', width=100)
        self.table_reservation.column('date', width=100)

        self.table_reservation.pack(fill=BOTH, expand=1)
        self.table_reservation.bind("<ButtonRelease-1>", self.get_cursor)

        self.afficher_reservations()

    def ajouter_reservation(self):
        if self.var_salle_id.get() == '' or self.var_client_id.get() == '' or self.var_nb_heure.get() == '' or self.var_taxe.get() == '' or self.var_type_paiement.get() == '' or self.var_date.get() == '':
            messagebox.showerror('Erreur', 'Tous les champs doivent être remplis', parent=self.root)
        else:
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='',
                    database='GestionReservation'
                )
                con_cursor = conn.cursor()

                # Insérer la réservation (le trigger calculera le prix_total)
                con_cursor.execute(
                    'INSERT INTO reservation_salle (salle_id, client_id, nb_heure, taxe, type_paiement, date_creation) VALUES (%s, %s, %s, %s, %s, %s)',
                    (
                        self.var_salle_id.get(),
                        self.var_client_id.get(),
                        self.var_nb_heure.get(),
                        self.var_taxe.get(),
                        self.var_type_paiement.get(),
                        self.var_date.get()
                    )
                )
                conn.commit()
                self.afficher_reservations()
                conn.close()
                messagebox.showinfo('Succès', 'Réservation ajoutée avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_reservations(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='',
                database='GestionReservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('''
                SELECT r.identifiant, r.salle_id, s.nom, r.client_id, c.nom, c.prenom, c.telephone, r.nb_heure, r.taxe, r.prix_total, r.type_paiement, r.date_creation
                FROM reservation_salle r
                JOIN salle s ON r.salle_id = s.salle_id
                JOIN client c ON r.client_id = c.client_id
            ''')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.table_reservation.delete(*self.table_reservation.get_children())
                for i in rows:
                    self.table_reservation.insert("", END, values=i)
                conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def rechercher_par_date(self):
        date_recherche = self.var_date.get()
        if date_recherche == '':
            messagebox.showerror('Erreur', 'Veuillez entrer une date pour la recherche', parent=self.root)
        else:
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='',
                    database='GestionReservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute('''
                    SELECT r.identifiant, r.salle_id, s.nom, r.client_id, c.nom, c.prenom, c.telephone, r.nb_heure, r.taxe, r.prix_total, r.type_paiement, r.date_creation
                    FROM reservation_salle r
                    JOIN salle s ON r.salle_id = s.salle_id
                    JOIN client c ON r.client_id = c.client_id
                    WHERE r.date = %s
                ''', (date_recherche,))
                rows = con_cursor.fetchall()
                if len(rows) != 0:
                    self.table_reservation.delete(*self.table_reservation.get_children())
                    for i in rows:
                        self.table_reservation.insert("", END, values=i)
                else:
                    messagebox.showinfo('Information', 'Aucune réservation trouvée pour cette date', parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def imprimer_recu(self):
        cursor_row = self.table_reservation.focus()
        content = self.table_reservation.item(cursor_row)
        row = content["values"]

        if not row:
            messagebox.showerror('Erreur', 'Veuillez sélectionner une réservation pour imprimer le reçu', parent=self.root)
            return

        try:
            # Création du PDF
            pdf = FPDF()
            pdf.add_page()

            # Utiliser la police standard Helvetica
            pdf.set_font('Helvetica', '', 12)

            # En-tête professionnel
            pdf.set_font('Helvetica', 'B', 24)
            pdf.set_text_color(31, 73, 125)  # Bleu professionnel
            pdf.cell(0, 15, 'Hôtel Marhaba', 0, 1, 'C')
            pdf.set_font('Helvetica', 'B', 18)
            pdf.cell(0, 10, 'Reçu de Réservation de Salle', 0, 1, 'C')
            pdf.ln(10)

            # Informations client
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 10, 'Informations Client', 0, 1)
            pdf.set_font('Helvetica', '', 12)
            pdf.cell(50, 8, 'Nom:', 0, 0)
            pdf.cell(0, 8, f'{str(row[4])} {str(row[5])}', 0, 1)  # Convertir en chaîne de caractères
            pdf.cell(50, 8, 'Téléphone:', 0, 0)
            pdf.cell(0, 8, str(row[6]), 0, 1)  # Convertir en chaîne de caractères
            pdf.ln(10)

            # Détails de la salle
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 10, 'Détails de la Salle', 0, 1)
            pdf.set_font('Helvetica', '', 12)
            pdf.cell(50, 8, 'ID Salle:', 0, 0)
            pdf.cell(0, 8, str(row[1]), 0, 1)  # Convertir en chaîne de caractères
            pdf.cell(50, 8, 'Nom Salle:', 0, 0)
            pdf.cell(0, 8, str(row[2]), 0, 1)  # Convertir en chaîne de caractères
            pdf.cell(50, 8, 'Nombre d\'heures:', 0, 0)
            pdf.cell(0, 8, str(row[7]), 0, 1)  # Convertir en chaîne de caractères
            pdf.cell(50, 8, 'Taxe:', 0, 0)
            pdf.cell(0, 8, str(row[8]), 0, 1)  # Convertir en chaîne de caractères
            pdf.cell(50, 8, 'Prix Total:', 0, 0)
            pdf.cell(0, 8, f'{str(row[9])} FCFA', 0, 1)  # Convertir en chaîne de caractères
            pdf.ln(10)

            # Période de réservation
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(50, 10, 'Date:', 0, 0)
            pdf.set_font('Helvetica', '', 12)
            pdf.cell(0, 10, str(row[11]), 0, 1)  # Convertir en chaîne de caractères
            pdf.ln(10)

            # Type de paiement
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(50, 10, 'Type de Paiement:', 0, 0)
            pdf.set_font('Helvetica', '', 12)
            pdf.cell(0, 10, str(row[10]), 0, 1)  # Convertir en chaîne de caractères
            pdf.ln(15)

            # Mentions légales
            pdf.set_font('Helvetica', 'I', 10)
            pdf.set_text_color(100)
            pdf.cell(0, 5, 'Merci pour votre confiance !', 0, 1, 'C')
            pdf.cell(0, 5, 'En cas de problème, contactez le service client au 93 58 30 58', 0, 1, 'C')

            # Sauvegarde du PDF
            nom_fichier = f"Reçu_Salle_{str(row[0])}.pdf"  # Convertir en chaîne de caractères
            pdf.output(nom_fichier)
            messagebox.showinfo('Succès', f'Reçu généré : {nom_fichier}', parent=self.root)
        except Exception as es:
            messagebox.showerror('Erreur', f'Erreur lors de la génération du PDF: {str(es)}', parent=self.root)
            
            
    def get_cursor(self, event=""):
        cursor_row = self.table_reservation.focus()
        content = self.table_reservation.item(cursor_row)
        row = content["values"]

        self.var_identifiant.set(row[0])
        self.var_salle_id.set(row[1])
        self.var_client_id.set(row[3])
        self.var_nb_heure.set(row[7])
        self.var_taxe.set(row[8])
        self.var_type_paiement.set(row[10])
        self.var_date.set(row[11])

    def modifier_reservation(self):
        if self.var_identifiant.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner une réservation', parent=self.root)
        else:
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='',
                    database='GestionReservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute(
                    'UPDATE reservation_salle SET salle_id=%s, client_id=%s, nb_heure=%s, taxe=%s, type_paiement=%s, date=%s WHERE identifiant=%s',
                    (
                        self.var_salle_id.get(),
                        self.var_client_id.get(),
                        self.var_nb_heure.get(),
                        self.var_taxe.get(),
                        self.var_type_paiement.get(),
                        self.var_date.get(),
                        self.var_identifiant.get()
                    )
                )
                conn.commit()
                self.afficher_reservations()
                conn.close()
                messagebox.showinfo('Succès', 'Réservation modifiée avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def supprimer_reservation(self):
        if self.var_identifiant.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner une réservation', parent=self.root)
        else:
            try:
                confirmation = messagebox.askyesno('Confirmation', 'Voulez-vous vraiment supprimer cette réservation ?', parent=self.root)
                if confirmation:
                    conn = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        password='',
                        database='GestionReservation'
                    )
                    con_cursor = conn.cursor()
                    con_cursor.execute('DELETE FROM reservation_salle WHERE identifiant=%s', (self.var_identifiant.get(),))
                    conn.commit()
                    self.afficher_reservations()
                    conn.close()
                    messagebox.showinfo('Succès', 'Réservation supprimée avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def reinitialiser(self):
        self.var_identifiant.set('')
        self.var_salle_id.set('')
        self.var_client_id.set('')
        self.var_nb_heure.set('')
        self.var_taxe.set('')
        self.var_type_paiement.set('')
        self.var_date.set('')

if __name__ == "__main__":
    root = Tk()
    obj = FenetreReservationSalle(root)
    root.mainloop()
