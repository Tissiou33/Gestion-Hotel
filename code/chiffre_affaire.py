from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

class FenetreChiffreAffaire:
    def __init__(self, root):
        self.root = root
        self.root.title('Chiffre d\'affaire')
        self.root.geometry('1295x550+230+220')

        # Variables
        self.var_chiffre_affaire = StringVar()

        # Titre
        titre = Label(self.root, text='CHIFFRE D\'AFFAIRE', font=('times new roman', 18, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=0, width=1295, height=50)

        # Main Frame
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=50, width=1295, height=500)

        # Labels et Entrées
        lbl_chiffre_affaire = Label(main_frame, text='Chiffre d\'affaire:', font=('times new roman', 12, 'bold'))
        lbl_chiffre_affaire.grid(row=0, column=0, padx=10, pady=10)
        entry_chiffre_affaire = ttk.Entry(main_frame, textvariable=self.var_chiffre_affaire, font=('times new roman', 12), state='readonly')
        entry_chiffre_affaire.grid(row=0, column=1, padx=10, pady=10)

        # Boutons
        btn_calculer = Button(main_frame, text='Calculer', command=self.calculer_chiffre_affaire, font=('times new roman', 12, 'bold'), bg='black', fg='gold')
        btn_calculer.grid(row=1, column=0, padx=10, pady=10)

    def calculer_chiffre_affaire(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='DAMALI@\@2025',
                database='Gestion_Reservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT SUM(prix) FROM reservation_chambre')
            chiffre_affaire = con_cursor.fetchone()[0]
            self.var_chiffre_affaire.set(chiffre_affaire)
            conn.close()
        except Exception as es:
            messagebox.showwarning('Avertissement', f'Erreur: {str(es)}', parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = FenetreChiffreAffaire(root)
    root.mainloop()
