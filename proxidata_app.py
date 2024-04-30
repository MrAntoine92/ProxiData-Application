from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
import os
from bande_rouge1 import BandeRouge1
from parcourir_page import ParcourirPage

class ProxiDataApp:
    def __init__(self, master):
        self.master = master
        self.logo = None
        master.title('ProxiData')
        master.geometry('1000x700')
        master.minsize(766, 416)

        s = ttk.Style()
        s.configure('partie_droite.TFrame', background='green')

        # Bande rouge
        BandeRouge1(self.master)

        # Partie droite
        self.partie_droite = ttk.Frame(master)
        self.partie_droite.place(relx=0.15, y=0, relwidth=0.85, relheight=1)

        # Titre
        image_titre = Image.open('Images/image_titre.png')
        resized_titre = image_titre.resize((243, 42))
        self.titre_final = ImageTk.PhotoImage(resized_titre)

        self.titre = ttk.Label(
            self.partie_droite,
            image=self.titre_final,
            background='#F1F1F1')
        self.titre.pack(pady=50)

        # Image Accueil
        image_accueil = Image.open('Images/image_accueil.png')
        resized_image = image_accueil.resize((500, 200))
        self.image_finale = ImageTk.PhotoImage(resized_image)

        self.label_image = ttk.Label(
            self.partie_droite,
            image=self.image_finale if self.image_finale else None)
        self.label_image.pack(pady=(20, 0))

        # Bouton entrer
        self.bouton_entrer = ctk.CTkButton(
            self.partie_droite,
            text='Entrer',
            fg_color='#F54E59',
            hover_color='#C33841',
            height=70,
            width=150,
            font=("Inter", 18),
            corner_radius=80,
            anchor='CENTER',
            command=self.show_parcourir_page)
        self.bouton_entrer.pack(pady=(70, 0))
        
        # Check if the file 'predictions.csv' exists
        file_path = 'Fiches/Output/predictions.csv'
        if os.path.exists("Fiches/Output/predictions.csv"):
            # Delete the file
            os.remove("Fiches/Output/predictions.csv")

        self.master.bind("<Configure>", self.on_configure2, add="+")

    def on_configure2(self, event):
        self.resize_image()

    def show_parcourir_page(self):
        # Hide elements of the first page
        ParcourirPage(self.master)

    def resize_image(self, event=None):
        new_img_width = self.partie_droite.winfo_width()
        if new_img_width > 0:
            img = Image.open('Images/image_accueil.png')
            new_img_size = int(new_img_width * 0.8)
            new_img_size_h = int(new_img_size * 0.35)
            if new_img_size > 0:
                resized_img = img.resize((new_img_size, new_img_size_h))
                self.image_finale = ImageTk.PhotoImage(resized_img)

                if self.label_image:
                    self.label_image.config(image=self.image_finale)
                else:
                    self.label_image = ttk.Label(
                        image=self.image_finale,
                        background='#F54E59')
                    self.label_image.pack(pady=(75, 0))
