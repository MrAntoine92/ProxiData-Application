from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import filedialog
import os
from recap_page import RecapPage
from bande_rouge2 import BandeRouge2
import tkinter.messagebox as messagebox
from file_manager import FileManager


# slt
class ParcourirPage:
    def __init__(self, master):
        self.master = master
        global filename
        s = ttk.Style()
        s.configure('partie_droite.TFrame', background='green')

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

        # Trait
        self.trait = ttk.Separator(self.partie_droite, orient='horizontal')
        self.trait.pack(fill='x', padx=(50))

        image_accueil = Image.open('Images/vide.png')
        resized_image = image_accueil.resize((50, 30))
        self.image_finale = ImageTk.PhotoImage(resized_image)

        self.label_image = ttk.Label(
            self.partie_droite,
            image=self.image_finale if self.image_finale else None)
        self.label_image.pack(pady=(10, 0))

        #  Frame parcourir
        self.frame_parcourir = ttk.Frame(self.partie_droite)
        self.frame_parcourir.pack(pady=(10, 0))

        # Bouton chemin PAS CLIQUABLE
        self.bouton_chemin = ctk.CTkButton(
            self.frame_parcourir,
            text='Importez le fichier',
            fg_color='#E7E7E7',
            # text_color='black',
            height=20,
            width=300,
            font=("Inter", 16),
            corner_radius=15,
            state='disabled',
            border_width=2)
        self.bouton_chemin.pack(side='left')

        # Bouton parcourir
        self.bouton_parcourir = ctk.CTkButton(
            self.frame_parcourir,
            text='Parcourir',
            fg_color='#F54E59',
            hover_color='#CC2F39',
            height=50,
            width=100,
            font=("Inter", 18),
            corner_radius=80,
            command=self.browseFiles)
        self.bouton_parcourir.pack(side='right', padx=50)

        # Bouton entrer
        self.bouton_valider = ctk.CTkButton(
            self.partie_droite,
            text='Valider',
            fg_color='#F54E59',
            hover_color='#CC2F39',
            height=70,
            width=150,
            font=("Inter", 18),
            corner_radius=80,
            command=self.validate,
        )
        self.bouton_valider.pack(pady=(50, 0))

        self.master.bind("<Configure>", self.on_configure, add="+")

    def on_configure(self, event):
        self.resize_image()

    def resize_image(self, event=None):
        new_img_width = self.partie_droite.winfo_width()
        if new_img_width > 0:
            img = Image.open('Images/vide.png')
            new_img_size = int(new_img_width * 0.5)
            new_img_size_h = int(new_img_size * 0.3)
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

    def browseFiles(self):
        self.filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select an Excel File",
            filetypes=(("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if self.filename:
            file_name = os.path.basename(self.filename)
            self.bouton_chemin.configure(
                text=file_name,
                text_color_disabled='black'
            )
        else:
            print("No file selected.")

    def show_recap_page(self):
        # Hide elements of the first page
        BandeRouge2(self.master)
        RecapPage(self.master)


    def validate(self):
        from import_data import test_colonne, import_fiche, import_ref, select_agences
        if not hasattr(self, 'filename') or not self.filename:
            self.bouton_valider.configure(state='disabled') 
            self.master.after(1000, self.enable_button)
        
        else :
            df = import_fiche(self.filename)
            glob_df = import_ref("Fiches/Benchmark Classement Agences REEL 2022 et REEL 2023.xlsx")
            final_df = select_agences(df, glob_df)
            if test_colonne(final_df) == True:
                FileManager.set_filename(self.filename)
                self.show_recap_page()
            else:
                message = test_colonne(self.filename)
                print(message)
                self.reset_page_and_show_error(message)


    def enable_button(self):
        # Enable the button
        self.bouton_valider.configure(state='normal')

    def reset_page_and_show_error(self, error_message):
        # Reset the current page
        self.reset_page()

        # Show the error message
        messagebox.showerror("Error", error_message)

    def reset_page(self):
        self.filename = None
        self.bouton_chemin.configure(text='Importez le fichier')
