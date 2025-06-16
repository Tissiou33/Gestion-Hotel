from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

class FenetreFeedback:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestion des Feedback')
        self.root.geometry('1295x550+230+220')

        # Variables
        self.var_feedback_id = StringVar()
        self.var_client_id = StringVar()
        self.var_appreciation = StringVar()
        self.var_note = StringVar()

        # Titre
        titre = Label(self.root, text='GESTION DES FEEDBACK', font=('times new roman', 18, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1295, height=50)

        # Main Frame
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=50, width=1295, height=500)

        # Labels et Entrées
        lbl_client_id = Label(main_frame, text='ID Client:', font=('times new roman', 12, 'bold'))
        lbl_client_id.grid(row=0, column=0, padx=10, pady=10)
        entry_client_id = ttk.Entry(main_frame, textvariable=self.var_client_id, font=('times new roman', 12))
        entry_client_id.grid(row=0, column=1, padx=10, pady=10)

        lbl_appreciation = Label(main_frame, text='Appréciation:', font=('times new roman', 12, 'bold'))
        lbl_appreciation.grid(row=1, column=0, padx=10, pady=10)
        entry_appreciation = ttk.Entry(main_frame, textvariable=self.var_appreciation, font=('times new roman', 12))
        entry_appreciation.grid(row=1, column=1, padx=10, pady=10)

        lbl_note = Label(main_frame, text='Note:', font=('times new roman', 12, 'bold'))
        lbl_note.grid(row=2, column=0, padx=10, pady=10)
        entry_note = ttk.Entry(main_frame, textvariable=self.var_note, font=('times new roman', 12))
        entry_note.grid(row=2, column=1, padx=10, pady=10)

        # Boutons
        btn_ajouter = Button(main_frame, text='Ajouter', command=self.ajouter_feedback, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_ajouter.grid(row=3, column=0, padx=10, pady=10)

        btn_modifier = Button(main_frame, text='Modifier', command=self.modifier_feedback, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_modifier.grid(row=3, column=1, padx=10, pady=10)

        btn_supprimer = Button(main_frame, text='Supprimer', command=self.supprimer_feedback, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_supprimer.grid(row=3, column=2, padx=10, pady=10)

        btn_reinitialiser = Button(main_frame, text='Réinitialiser', command=self.reinitialiser, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_reinitialiser.grid(row=3, column=3, padx=10, pady=10)

        # Tableau
        table_frame = Frame(main_frame, bd=0, relief=RIDGE)
        table_frame.place(x=10, y=300, width=1270, height=180)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.table_feedback = ttk.Treeview(table_frame, columns=('feedback_id', 'client_id', 'appreciation', 'note','Date'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.table_feedback.xview)
        scroll_y.config(command=self.table_feedback.yview)

        self.table_feedback.heading('feedback_id', text='ID')
        self.table_feedback.heading('client_id', text='ID Client')
        self.table_feedback.heading('appreciation', text='Appréciation')
        self.table_feedback.heading('note', text='Note')
        self.table_feedback.heading('Date', text='Date')

        self.table_feedback['show'] = 'headings'

        self.table_feedback.column('feedback_id', width=50)
        self.table_feedback.column('client_id', width=50)
        self.table_feedback.column('appreciation', width=200)
        self.table_feedback.column('note', width=100)
        self.table_feedback.column('Date',width=100)

        self.table_feedback.pack(fill=BOTH, expand=1)
        self.table_feedback.bind("<ButtonRelease-1>", self.get_cursor)

        self.afficher_feedbacks()

    def ajouter_feedback(self):
        if self.var_client_id.get() == '' or self.var_appreciation.get() == '':
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
                    'INSERT INTO feedback (client_id, appreciation, note) VALUES (%s, %s, %s)',
                    (
                        self.var_client_id.get(),
                        self.var_appreciation.get(),
                        self.var_note.get()
                    )
                )
                conn.commit()
                self.afficher_feedbacks()
                conn.close()
                messagebox.showinfo('Succès', 'Feedback ajouté avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def afficher_feedbacks(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM feedback')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.table_feedback.delete(*self.table_feedback.get_children())
                for i in rows:
                    self.table_feedback.insert("", END, values=i)
                conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.table_feedback.focus()
        content = self.table_feedback.item(cursor_row)
        row = content["values"]

        self.var_feedback_id.set(row[0])
        self.var_client_id.set(row[1])
        self.var_appreciation.set(row[2])
        self.var_note.set(row[3])

    def modifier_feedback(self):
        if self.var_feedback_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner un feedback', parent=self.root)
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
                    'UPDATE feedback SET client_id=%s, appreciation=%s, note=%s WHERE feedback_id=%s',
                    (
                        self.var_client_id.get(),
                        self.var_appreciation.get(),
                        self.var_note.get(),
                        self.var_feedback_id.get()
                    )
                )
                conn.commit()
                self.afficher_feedbacks()
                conn.close()
                messagebox.showinfo('Succès', 'Feedback modifié avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def supprimer_feedback(self):
        if self.var_feedback_id.get() == '':
            messagebox.showerror('Erreur', 'Veuillez sélectionner un feedback', parent=self.root)
        else:
            try:
                confirmation = messagebox.askyesno('Confirmation', 'Voulez-vous vraiment supprimer ce feedback ?', parent=self.root)
                if confirmation:
                    conn = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        password='DAMALI@\@2025',
                        database='Gestion_Reservation'
                    )
                    con_cursor = conn.cursor()
                    con_cursor.execute('DELETE FROM feedback WHERE feedback_id=%s', (self.var_feedback_id.get(),))
                    conn.commit()
                    self.afficher_feedbacks()
                    conn.close()
                    messagebox.showinfo('Succès', 'Feedback supprimé avec succès', parent=self.root)
            except Exception as es:
                messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def reinitialiser(self):
        self.var_feedback_id.set('')
        self.var_client_id.set('')
        self.var_appreciation.set('')
        self.var_note.set('')

if __name__ == "__main__":
    root = Tk()
    obj = FenetreFeedback(root)
    root.mainloop()