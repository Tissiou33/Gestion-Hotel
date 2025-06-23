from tkinter import *
from PIL import Image, ImageTk
from client import FenetreClient
from chambre import FenetreChambre
from reservation_chambre import FenetreReservationChambre
from reservation_salle import FenetreReservationSalle
from objets_perdus import FenetreObjetsPerdus
from admin import FenetreAdmin  # Importation de la classe Admin
import psycopg2
import os
from tkinter import messagebox
from tkinter import ttk

class SystemeGestionHotel:
    def __init__(self, root):
        self.root = root
        self.root.title('Système de Gestion Hôtelière')
        self.root.geometry('1550x800+0+0')

        # Chemin des images (à adapter )
        self.image_paths = {
            'hotel1': 'hotel1.jpg',
            'hotel2': 'hotel2.jpg',
            'hotel3': 'hotel3.jpg',
            'hotel4': 'hotel4.jpg',
            'hotel5': 'hotel5.jpg'
        }

        # Vérifie si les images existent
        for key, path in self.image_paths.items():
            if not os.path.exists(path):
                print(f"Attention : L'image '{path}' n'existe pas. Vérifie le chemin d'accès.")
                self.image_paths[key] = None  # Marque l'image comme manquante

        # Image 1 (en haut)
        if self.image_paths['hotel1']:
            img1 = Image.open(self.image_paths['hotel1'])
            img1 = img1.resize((1550, 140), Image.LANCZOS)
            self.photoimg1 = ImageTk.PhotoImage(img1)
            labelimg = Label(self.root, image=self.photoimg1, bd=4, relief=RAISED)
            labelimg.place(x=0, y=0, width=1550, height=140)
        else:
            labelimg = Label(self.root, text="Image hotel1.jpg manquante", bd=4, relief=RAISED, fg='red')
            labelimg.place(x=0, y=0, width=1550, height=140)

        # Logo (en haut à gauche)+
        if self.image_paths['hotel2']:
            img2 = Image.open(self.image_paths['hotel2'])
            img2 = img2.resize((230, 140), Image.LANCZOS)
            self.photoimg2 = ImageTk.PhotoImage(img2)
            labelimg1 = Label(self.root, image=self.photoimg2, bd=4, relief=RIDGE)
            labelimg1.place(x=0, y=0, width=230, height=140)
        else:
            labelimg1 = Label(self.root, text="Image hotel2.jpg manquante", bd=4, relief=RIDGE, fg='red')
            labelimg1.place(x=0, y=0, width=230, height=140)

        # Titre
        titre = Label(self.root, text='SYSTÈME DE GESTION HÔTELIÈRE', font=('times new roman', 40, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        titre.place(x=0, y=140, width=1550, height=50)

        # Main Frame
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=190, width=1550, height=620)

        # Menu
        label_menu = Label(self.root, text='MENU', font=('times new roman', 20, 'bold'), fg='gold', bg='black', bd=4, relief=RIDGE)
        label_menu.place(x=0, y=190, width=230)

        # Button Frame
        button_frame = Frame(self.root, bd=4, relief=RIDGE)
        button_frame.place(x=0, y=230, width=228, height=260)

        # Boutons
        btn_client = Button(button_frame, text='CLIENTS', command=self.ouvrir_fenetre_client, width=22, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_client.grid(row=0, column=0, pady=1)

        btn_chambre = Button(button_frame, text='CHAMBRES', command=self.ouvrir_fenetre_chambre, width=22, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_chambre.grid(row=1, column=0, pady=1)

        btn_reservation_chambre = Button(button_frame, text='RÉSERVATION CHAMBRE', command=self.ouvrir_fenetre_reservation_chambre, width=22, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_reservation_chambre.grid(row=2, column=0, pady=1)

        btn_reservation_salle = Button(button_frame, text='RÉSERVATION SALLE', command=self.ouvrir_fenetre_reservation_salle, width=22, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_reservation_salle.grid(row=3, column=0, pady=1)

        btn_objets_perdus = Button(button_frame, text='OBJETS PERDUS', command=self.ouvrir_fenetre_objets_perdus, width=22, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_objets_perdus.grid(row=4, column=0, pady=1)

        # Nouveau bouton pour afficher les plats
        btn_plats = Button(button_frame, text='PLATS', command=self.afficher_plats, width=22, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_plats.grid(row=5, column=0, pady=1)
        
        # Nouveau bouton pour afficher les plats
        btn_plats = Button(button_frame, text='BOISSONS', command=self.afficher_boissons, width=22, font=('times new roman', 14, 'bold'), fg='gold', bg='black', bd=0, cursor='hand1')
        btn_plats.grid(row=6, column=0, pady=1)
        
        # Image 3 (à droite)
        if self.image_paths['hotel3']:
            img3 = Image.open(self.image_paths['hotel3'])
            img3 = img3.resize((1310, 590), Image.LANCZOS)
            self.photoimg3 = ImageTk.PhotoImage(img3)
            labelimg2 = Label(main_frame, image=self.photoimg3, bd=4, relief=RIDGE)
            labelimg2.place(x=225, y=0, width=1310, height=590)
        else:
            labelimg2 = Label(main_frame, text="Image hotel3.jpg manquante", bd=4, relief=RIDGE, fg='red')
            labelimg2.place(x=225, y=0, width=1310, height=590)
        
        #  Image 1 (en bas à gauche)
        if self.image_paths['hotel4']:
            img4 = Image.open(self.image_paths['hotel4'])
            img4 = img4.resize((230, 210), Image.LANCZOS)
            self.photoimg4 = ImageTk.PhotoImage(img4)
            labelimg3 = Label(main_frame, image=self.photoimg4, bd=4, relief=RIDGE)
            labelimg3.place(x=0, y=225, width=230, height=210)
        else:
            labelimg3 = Label(main_frame, text="Image hotel4.jpg manquante", bd=4, relief=RIDGE, fg='red')
            labelimg3.place(x=0, y=225, width=230, height=210)
       
        #  Image 2 (en bas à gauche)
        if self.image_paths['hotel5']:
            img5 = Image.open(self.image_paths['hotel5'])
            img5 = img5.resize((230, 190), Image.LANCZOS)
            self.photoimg5 = ImageTk.PhotoImage(img5)
            labelimg4 = Label(main_frame, image=self.photoimg5, bd=4, relief=RIDGE)
            labelimg4.place(x=0, y=400, width=230, height=190)
        else:
            labelimg4 = Label(main_frame, text="Image hotel5.jpg manquante", bd=4, relief=RIDGE, fg='red')
            labelimg4.place(x=0, y=400, width=230, height=190)

    def ouvrir_fenetre_client(self):
        self.nouvelle_fenetre = Toplevel(self.root)
        self.app = FenetreClient(self.nouvelle_fenetre)

    def ouvrir_fenetre_chambre(self):
        self.nouvelle_fenetre = Toplevel(self.root)
        self.app = FenetreChambre(self.nouvelle_fenetre)

    def ouvrir_fenetre_reservation_chambre(self):
        self.nouvelle_fenetre = Toplevel(self.root)
        self.app = FenetreReservationChambre(self.nouvelle_fenetre)

    def ouvrir_fenetre_reservation_salle(self):
        self.nouvelle_fenetre = Toplevel(self.root)
        self.app = FenetreReservationSalle(self.nouvelle_fenetre)

    def ouvrir_fenetre_objets_perdus(self):
        self.nouvelle_fenetre = Toplevel(self.root)
        self.app = FenetreObjetsPerdus(self.nouvelle_fenetre)

    def afficher_plats(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='******',
                database='GestionReservation'
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
                password='******',
                database='GestionReservation'
            )
            con_cursor = conn.cursor()
            con_cursor.execute('SELECT * FROM boisson')
            rows = con_cursor.fetchall()
            if len(rows) != 0:
                self.afficher_table(rows, ['ID', 'Nom', 'Prix'])
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
        
if __name__ == "__main__":
    root = Tk()
    obj = SystemeGestionHotel(root)
    root.mainloop()
