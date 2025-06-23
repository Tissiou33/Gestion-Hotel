from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from fpdf import FPDF  # Bibliothèque pour générer des PDFs

class FenetreReservationChambre:
    def __init__(self, root):
        self.root = root
        self.root.title('Réservation de Chambre')
        self.root.geometry('1295x550+230+220')

        # Variables
        self.var_reservation_id = StringVar()
        self.var_client_id = StringVar()
        self.var_chambre_id = StringVar()
        self.var_date_debut = StringVar()
        self.var_nb_jours = StringVar()
        self.var_type_paiement = StringVar()
        self.var_taxe = StringVar()
        self.var_reduction = StringVar()
        self.var_type_restauration = StringVar()  # Nouveau champ pour le type de restauration
        self.var_quantite = StringVar()  # Nouveau champ pour la quantité

        # Titre
        titre = Label(self.root, text='RÉSERVATION DE CHAMBRE', font=('times new roman', 18, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1295, height=50)

        # Cadre pour la saisie (à gauche)
        saisie_frame = Frame(self.root, bd=4, relief=RIDGE)
        saisie_frame.place(x=0, y=50, width=400, height=500)

        # Cadre pour l'affichage (à droite)
        affichage_frame = Frame(self.root, bd=4, relief=RIDGE)
        affichage_frame.place(x=400, y=50, width=895, height=500)

        # ==================== Partie Saisie ====================
        # Labels et Entrées
        lbl_client_id = Label(saisie_frame, text='ID Client:', font=('times new roman', 12, 'bold'))
        lbl_client_id.grid(row=0, column=0, padx=8, pady=8)
        entry_client_id = ttk.Entry(saisie_frame, textvariable=self.var_client_id, font=('times new roman', 12))
        entry_client_id.grid(row=0, column=1, padx=8, pady=8)

        lbl_chambre_id = Label(saisie_frame, text='ID Chambre:', font=('times new roman', 12, 'bold'))
        lbl_chambre_id.grid(row=1, column=0, padx=8, pady=8)
        entry_chambre_id = ttk.Entry(saisie_frame, textvariable=self.var_chambre_id, font=('times new roman', 12))
        entry_chambre_id.grid(row=1, column=1, padx=8, pady=8)

        lbl_date_debut = Label(saisie_frame, text='Date de début:', font=('times new roman', 12, 'bold'))
        lbl_date_debut.grid(row=2, column=0, padx=8, pady=8)
        entry_date_debut = ttk.Entry(saisie_frame, textvariable=self.var_date_debut, font=('times new roman', 12))
        entry_date_debut.grid(row=2, column=1, padx=8, pady=8)

        lbl_nb_jours = Label(saisie_frame, text='Nombre de jours:', font=('times new roman', 12, 'bold'))
        lbl_nb_jours.grid(row=3, column=0, padx=8, pady=8)
        entry_nb_jours = ttk.Entry(saisie_frame, textvariable=self.var_nb_jours, font=('times new roman', 12))
        entry_nb_jours.grid(row=3, column=1, padx=8, pady=8)

        # Nouveaux champs : Type de restauration et Quantité
        lbl_type_restauration = Label(saisie_frame, text='Type de restauration:', font=('times new roman', 12, 'bold'))
        lbl_type_restauration.grid(row=4, column=0, padx=10, pady=10)
        self.combo_type_restauration = ttk.Combobox(saisie_frame, textvariable=self.var_type_restauration, font=('times new roman', 12), state='readonly')
        self.combo_type_restauration['values'] = ('1-HS', '2-PD', '3-DP', '4-PC', '5-TT')
        self.combo_type_restauration.grid(row=4, column=1, padx=10, pady=10)
        self.combo_type_restauration.current(0)

        lbl_quantite = Label(saisie_frame, text='Quantité:', font=('times new roman', 12, 'bold'))
        lbl_quantite.grid(row=5, column=0, padx=10, pady=10)
        entry_quantite = ttk.Entry(saisie_frame, textvariable=self.var_quantite, font=('times new roman', 12))
        entry_quantite.grid(row=5, column=1, padx=10, pady=10)

        # Type de paiement, Taxe, Réduction
        lbl_type_paiement = Label(saisie_frame, text='Type de paiement:', font=('times new roman', 12, 'bold'))
        lbl_type_paiement.grid(row=6, column=0, padx=10, pady=10)
        self.combo_type_paiement = ttk.Combobox(saisie_frame, textvariable=self.var_type_paiement, font=('times new roman', 12), state='readonly')
        self.combo_type_paiement['values'] = ('Virement', 'Espèce', 'Crypto')
        self.combo_type_paiement.grid(row=6, column=1, padx=10, pady=10)
        self.combo_type_paiement.current(0)

        lbl_taxe = Label(saisie_frame, text='Taxe:', font=('times new roman', 12, 'bold'))
        lbl_taxe.grid(row=7, column=0, padx=8, pady=8)
        entry_taxe = ttk.Entry(saisie_frame, textvariable=self.var_taxe, font=('times new roman', 12))
        entry_taxe.grid(row=7, column=1, padx=8, pady=8)

        lbl_reduction = Label(saisie_frame, text='Réduction:', font=('times new roman', 12, 'bold'))
        lbl_reduction.grid(row=8, column=0, padx=8, pady=8)
        entry_reduction = ttk.Entry(saisie_frame, textvariable=self.var_reduction, font=('times new roman', 12))
        entry_reduction.grid(row=8, column=1, padx=8, pady=8)

        # Boutons
        btn_ajouter = Button(saisie_frame, text='Ajouter', command=self.ajouter_reservation, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_ajouter.grid(row=9, column=0, padx=10, pady=10)

        btn_modifier = Button(saisie_frame, text='Modifier', command=self.modifier_reservation, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_modifier.grid(row=9, column=1, padx=10, pady=10)

        btn_supprimer = Button(saisie_frame, text='Supprimer', command=self.supprimer_reservation, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_supprimer.grid(row=10, column=1, padx=10, pady=10)

        btn_reinitialiser = Button(saisie_frame, text='Réinitialiser', command=self.reinitialiser, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_reinitialiser.grid(row=10, column=0, padx=10, pady=10)
        
         # Add Generate Receipt button
        btn_generer = Button(saisie_frame, text='Reçu', command=self.generer_reçu, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_generer.grid(row=10, column=2, columnspan=2, padx=10, pady=10)


        # ==================== Partie Affichage ====================
        # Tableau pour afficher les réservations
        scroll_x = ttk.Scrollbar(affichage_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(affichage_frame, orient=VERTICAL)

        self.table_reservation = ttk.Treeview(affichage_frame, columns=(
            'reservation_id', 'client_id', 'nom_client', 'telephone_client', 'chambre_id', 'type_chambre', 'date_debut', 
            'nb_jours', 'type_restauration', 'quantite', 'type_paiement', 'taxe', 'reduction', 'prix_finale'
        ), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.table_reservation.xview)
        scroll_y.config(command=self.table_reservation.yview)

        # En-têtes du tableau
        self.table_reservation.heading('reservation_id', text='ID')
        self.table_reservation.heading('client_id', text='ID Client')
        self.table_reservation.heading('nom_client', text='Nom Client')
        self.table_reservation.heading('telephone_client', text='Téléphone Client')
        self.table_reservation.heading('chambre_id', text='ID Chambre')
        self.table_reservation.heading('type_chambre', text='Type Chambre')
        self.table_reservation.heading('date_debut', text='Date de début')
        self.table_reservation.heading('nb_jours', text='Nombre de jours')
        self.table_reservation.heading('type_restauration', text='Type Restauration')
        self.table_reservation.heading('quantite', text='Quantité')
        self.table_reservation.heading('type_paiement', text='Type de Paiement')
        self.table_reservation.heading('taxe', text='Taxe')
        self.table_reservation.heading('reduction', text='Réduction')
        self.table_reservation.heading('prix_finale', text='Prix Final')

        self.table_reservation['show'] = 'headings'

        # Largeur des colonnes
        self.table_reservation.column('reservation_id', width=50)
        self.table_reservation.column('client_id', width=100)
        self.table_reservation.column('nom_client', width=100)
        self.table_reservation.column('telephone_client', width=100)
        self.table_reservation.column('chambre_id', width=100)
        self.table_reservation.column('type_chambre', width=100)
        self.table_reservation.column('date_debut', width=100)
        self.table_reservation.column('nb_jours', width=100)
        self.table_reservation.column('type_restauration', width=100)
        self.table_reservation.column('quantite', width=100)
        self.table_reservation.column('type_paiement', width=100)
        self.table_reservation.column('taxe', width=100)
        self.table_reservation.column('reduction', width=100)
        self.table_reservation.column('prix_finale', width=100)

        self.table_reservation.pack(fill=BOTH, expand=1)
        self.table_reservation.bind("<ButtonRelease-1>", self.get_cursor)

        self.afficher_reservations()

    def ajouter_reservation(self):
        if self.var_client_id.get() == '' or self.var_chambre_id.get() == '' or self.var_date_debut.get() == '' or self.var_nb_jours.get() == '' or self.var_type_paiement.get() == '' or self.var_taxe.get() == '' or self.var_reduction.get() == '' or self.var_type_restauration.get() == '' or self.var_quantite.get() == '':
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

                # Insérer la réservation
                con_cursor.execute(
                    'INSERT INTO reservation_chambre (client_id, chambre_id, date_debut, nb_jour, type_paiement, taxe, reduction, type_restauration_id, quantite) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (
                        self.var_client_id.get(),
                        self.var_chambre_id.get(),
                        self.var_date_debut.get(),
                        self.var_nb_jours.get(),
                        self.var_type_paiement.get(),
                        self.var_taxe.get(),
                        self.var_reduction.get(),
                        self.var_type_restauration.get().split('-')[0],  # Récupérer l'ID du type de restauration
                        self.var_quantite.get()
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
                SELECT r.reservation_id, r.client_id, c.nom, c.telephone, r.chambre_id, t.nom, r.date_debut, 
                r.nb_jour, tr.type, r.quantite, r.type_paiement, r.taxe, r.reduction, r.prix_finale
                FROM reservation_chambre r
                JOIN client c ON r.client_id = c.client_id
                JOIN chambre ch ON r.chambre_id = ch.chambre_id
                JOIN type_chambre t ON ch.type_chambre_id = t.type_chambre_id
                JOIN type_restauration tr ON r.type_restauration_id = tr.type_restauration_id
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

    def get_cursor(self, event=""):
        cursor_row = self.table_reservation.focus()
        content = self.table_reservation.item(cursor_row)
        row = content["values"]

        self.var_reservation_id.set(row[0])
        self.var_client_id.set(row[1])
        self.var_chambre_id.set(row[4])
        self.var_date_debut.set(row[6])
        self.var_nb_jours.set(row[7])
        self.var_type_restauration.set(row[8])
        self.var_quantite.set(row[9])
        self.var_type_paiement.set(row[10])
        self.var_taxe.set(row[11])
        self.var_reduction.set(row[12])
        
    def generer_reçu(self):
        if self.var_reservation_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner une réservation', parent=self.root)
        else:
            try:
                # Connexion à la base de données
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='',
                    database='GestionReservation'
                )
                con_cursor = conn.cursor()
                con_cursor.execute('''
                    SELECT 
                        c.nom, c.prenom, c.telephone, 
                        ch.numero, ch.etage, tc.nom,
                        tr.type, r.quantite,
                        r.date_debut, r.nb_jour, 
                        r.type_paiement, r.prix_finale 
                    FROM reservation_chambre r
                    JOIN client c ON r.client_id = c.client_id
                    JOIN chambre ch ON r.chambre_id = ch.chambre_id
                    JOIN type_chambre tc ON ch.type_chambre_id = tc.type_chambre_id
                    JOIN type_restauration tr ON r.type_restauration_id = tr.type_restauration_id
                    WHERE r.reservation_id = %s
                ''', (self.var_reservation_id.get(),))
                
                row = con_cursor.fetchone()
                conn.close()

                if row:
                    # Création du PDF
                    pdf = FPDF()
                    pdf.add_page()

                    # Utiliser la police standard Helvetica
                    pdf.set_font('Helvetica', '', 12)

                    # En-tête professionnel
                    pdf.set_font('Helvetica', 'B', 24)
                    pdf.set_text_color(31, 73, 125)  # Bleu professionnel
                    pdf.cell(0, 15, 'Hotel GROUPRE 1', 0, 1, 'C')
                    pdf.set_font('Helvetica', 'B', 18)
                    pdf.cell(0, 10, 'Reçu de Réservation', 0, 1, 'C')
                    pdf.ln(10)

                    # Informations client
                    pdf.set_font('Helvetica', 'B', 12)
                    pdf.cell(0, 10, 'Informations Client', 0, 1)
                    pdf.set_font('Helvetica', '', 12)
                    pdf.cell(50, 8, 'Nom:', 0, 0)
                    pdf.cell(0, 8, f'{row[0]} {row[1]}', 0, 1)
                    pdf.cell(50, 8, 'Téléphone:', 0, 0)
                    pdf.cell(0, 8, row[2], 0, 1)
                    pdf.ln(10)

                    # Détails de la chambre
                    pdf.set_font('Helvetica', 'B', 12)
                    pdf.cell(0, 10, 'Détails de la Chambre', 0, 1)
                    pdf.set_font('Helvetica', '', 12)
                    pdf.cell(50, 8, 'Numéro:', 0, 0)
                    pdf.cell(0, 8, str(row[3]), 0, 1)
                    pdf.cell(50, 8, 'Étage:', 0, 0)
                    pdf.cell(0, 8, str(row[4]), 0, 1)
                    pdf.cell(50, 8, 'Type:', 0, 0)
                    pdf.cell(0, 8, row[5], 0, 1)
                    pdf.cell(50, 8, 'Restauration:', 0, 0)
                    pdf.cell(0, 8, row[6], 0, 1)
                    pdf.cell(50, 8, 'Quantité:', 0, 0)
                    pdf.cell(0, 8, str(row[7]), 0, 1)
                    pdf.ln(10)

                    # Période de réservation
                    pdf.set_font('Helvetica', 'B', 12)
                    pdf.cell(50, 10, 'Période:', 0, 0)
                    pdf.set_font('Helvetica', '', 12)
                    pdf.cell(0, 10, f'Du {row[8]} pour {row[9]} jours', 0, 1)
                    pdf.ln(10)

                    # Total à régler
                    pdf.set_font('Helvetica', 'B', 14)
                    pdf.cell(0, 10, f'Total à régler: {row[11]} FCFA', 1, 1, 'C')  # Utiliser "EUR" au lieu de "€"
                    pdf.ln(15)

                    # Mentions légales
                    pdf.set_font('Helvetica', 'I', 10)
                    pdf.set_text_color(100)
                    pdf.cell(0, 5, 'Merci pour votre confiance !', 0, 1, 'C')
                    pdf.cell(0, 5, 'En cas de problème, contactez le service client au 93 58 30 58', 0, 1, 'C')

                    # Sauvegarde du PDF
                    nom_fichier = f"Reçu_{row[0]}_{row[1]}_{self.var_reservation_id.get()}.pdf"
                    pdf.output(nom_fichier)
                    messagebox.showinfo('Succès', f'Reçu généré : {nom_fichier}', parent=self.root)
                else:
                    messagebox.showerror('Erreur', 'Aucune donnée trouvée', parent=self.root)
            except Exception as es:
                messagebox.showerror('Erreur', f'Erreur lors de la génération du PDF: {str(es)}', parent=self.root)
    
    def modifier_reservation(self):
        if self.var_reservation_id.get() == '':
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
                    'UPDATE reservation_chambre SET client_id=%s, chambre_id=%s, date_debut=%s, nb_jour=%s, type_paiement=%s, taxe=%s, reduction=%s, type_restauration_id=%s, quantite=%s WHERE reservation_id=%s',
                    (
                        self.var_client_id.get(),
                        self.var_chambre_id.get(),
                        self.var_date_debut.get(),
                        self.var_nb_jours.get(),
                        self.var_type_paiement.get(),
                        self.var_taxe.get(),
                        self.var_reduction.get(),
                        self.var_type_restauration.get().split('-')[0],  # Récupérer l'ID du type de restauration
                        self.var_quantite.get(),
                        self.var_reservation_id.get()
                    )
                )
                conn.commit()
                self.afficher_reservations()
                conn.close()
                messagebox.showinfo('Succès', 'Réservation modifiée avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def supprimer_reservation(self):
        if self.var_reservation_id.get() == '':
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
                    con_cursor.execute('DELETE FROM reservation_chambre WHERE reservation_id=%s', (self.var_reservation_id.get(),))
                    conn.commit()
                    self.afficher_reservations()
                    conn.close()
                    messagebox.showinfo('Succès', 'Réservation supprimée avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)
    
    def reinitialiser(self):
        self.var_reservation_id.set('')
        self.var_client_id.set('')
        self.var_chambre_id.set('')
        self.var_date_debut.set('')
        self.var_nb_jours.set('')
        self.var_type_paiement.set('')
        self.var_taxe.set('')
        self.var_reduction.set('')
        self.var_type_restauration.set('')
        self.var_quantite.set('')

if __name__ == "__main__":
    root = Tk()
    obj = FenetreReservationChambre(root)
    root.mainloop()
