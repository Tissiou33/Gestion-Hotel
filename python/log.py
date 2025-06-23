from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from datetime import datetime

class FenetreLog:
    def __init__(self, root):
        self.root = root
        self.root.title('Historique des opérations')
        self.root.geometry('1295x550+230+220')

        # Variables
        self.var_log_id = StringVar()
        self.var_table_name = StringVar()
        self.var_operation = StringVar()
        self.var_record_id = StringVar()
        self.var_operation_time = StringVar()
        self.var_date_recherche = StringVar()  # Variable pour la date de recherche

        # Titre
        titre = Label(self.root, text='HISTORIQUE DES OPERATION HOTELIERE', font=('times new roman', 18, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1295, height=50)

        # Champ de saisie pour la date
        label_date = Label(self.root, text='Rechercher par date (AAAA-MM-JJ):', font=('times new roman', 12))
        label_date.place(x=10, y=60)

        self.entry_date = Entry(self.root, textvariable=self.var_date_recherche, font=('times new roman', 12))
        self.entry_date.place(x=250, y=60, width=150)

        btn_rechercher = Button(self.root, text='Rechercher', command=self.rechercher_par_date, font=('times new roman', 12), bg='blue', fg='white')
        btn_rechercher.place(x=420, y=60, width=100)

        # Main Frame
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=100, width=1295, height=450)

        # Tableau
        table_frame = Frame(main_frame, bd=4, relief=RIDGE)
        table_frame.place(x=0, y=0, width=1295, height=450)  # Ajusté pour occuper tout l'espace

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.table_log = ttk.Treeview(table_frame, columns=('log_id', 'table_name', 'operation', 'record_id', 'operation_time'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.table_log.xview)
        scroll_y.config(command=self.table_log.yview)

        self.table_log.heading('log_id', text='ID')
        self.table_log.heading('table_name', text='Table')
        self.table_log.heading('operation', text='Opération')
        self.table_log.heading('record_id', text='ID Enregistrement')
        self.table_log.heading('operation_time', text='Date')

        self.table_log['show'] = 'headings'

        self.table_log.column('log_id', width=50)
        self.table_log.column('table_name', width=100)
        self.table_log.column('operation', width=100)
        self.table_log.column('record_id', width=100)
        self.table_log.column('operation_time', width=100)

        self.table_log.pack(fill=BOTH, expand=1)
        self.table_log.bind("<ButtonRelease-1>", self.get_cursor)

        self.afficher_logs()

    def afficher_logs(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='******',
                database='GestionReservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM log')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.table_log.delete(*self.table_log.get_children())
                for i in rows:
                    self.table_log.insert("", END, values=i)
                conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def rechercher_par_date(self):
        date_recherche = self.var_date_recherche.get()
        if not date_recherche:
            messagebox.showwarning('Avertissement', 'Veuillez entrer une date.', parent=self.root)
            return

        try:
            # Convertir la date en format SQL (AAAA-MM-JJ)
            datetime.strptime(date_recherche, '%Y-%m-%d')  # Valider le format de la date
        except ValueError:
            messagebox.showwarning('Avertissement', 'Format de date invalide. Utilisez AAAA-MM-JJ.', parent=self.root)
            return

        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='******',
                database='GestionReservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute("SELECT * FROM log WHERE operation_time::date = %s", (date_recherche,))
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.table_log.delete(*self.table_log.get_children())
                for i in rows:
                    self.table_log.insert("", END, values=i)
            else:
                messagebox.showinfo('Information', 'Aucun log trouvé pour cette date.', parent=self.root)
            conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.table_log.focus()
        content = self.table_log.item(cursor_row)
        row = content["values"]

        self.var_log_id.set(row[0])
        self.var_table_name.set(row[1])
        self.var_operation.set(row[2])
        self.var_record_id.set(row[3])
        self.var_operation_time.set(row[4])

if __name__ == "__main__":
    root = Tk()
    obj = FenetreLog(root)
    root.mainloop()
