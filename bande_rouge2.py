import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
from bande_rouge1 import BandeRouge1
from analyse_page import AnalysePage
from comparaison_page import ComparaisonPage
from courbes_page import CourbesPage
from recap_page import RecapPage
import shutil
from tkinter import filedialog


class BandeRouge2:
    def __init__(self, master):
        self.master = master

        # Styles
        s = ttk.Style()
        s.configure('bande_rouge.TFrame', background='#F54E59')
        s.configure('trait.TSeparator', background='black')

        # Bande rouge
        self.bande_rouge = ttk.Frame(master, style='bande_rouge.TFrame')
        self.bande_rouge.place(x=0, y=0, relwidth=0.15, relheight=1)

        # Logo
        logo_proxiserve = Image.open('Images/logo_proxiserve.png')
        resized_logo = logo_proxiserve.resize((175, 175))
        self.logo_final = ImageTk.PhotoImage(resized_logo)

        self.logo = ttk.Label(
            self.bande_rouge,
            image=self.logo_final if self.logo_final else None,
            background='#F54E59',
            width=15)
        self.logo.pack(pady=(50, 0))

        # Trait 1
        self.trait_1 = ttk.Separator(
            self.bande_rouge,
            style='trait.TSeparator',
            orient='horizontal')
        self.trait_1.pack(fill='x', padx=(35))

        # Bouton accueil
        self.bouton_accueil = ctk.CTkImage(
            light_image=Image.open('Images/bouton_accueil.png'),
            dark_image=Image.open('Images/bouton_accueil.png'),
            size=(40, 40))

        self.accueil = ctk.CTkButton(
            self.bande_rouge,
            text='',
            fg_color='#F54E59',
            bg_color='#F54E59',
            hover_color='#CC2F39',
            width=50,
            height=50,
            image=self.bouton_accueil,
            command=self.popupmsg)

        self.accueil.pack(pady=(15, 15))

        # Trait 2
        self.trait_2 = ttk.Separator(
            self.bande_rouge,
            style='trait.TSeparator',
            orient='horizontal')
        self.trait_2.pack(fill='x', padx=35)

        # Bouton recap
        self.bouton_recap = ctk.CTkImage(
            light_image=Image.open('Images/bouton_recap.png'),
            dark_image=Image.open('Images/bouton_recap.png'),
            size=(40, 40))

        self.recap = ctk.CTkButton(
            self.bande_rouge,
            text='',
            fg_color='#DE3A45',
            bg_color='#F54E59',
            hover_color='#CC2F39',
            state='disabled',
            width=50,
            height=50,
            image=self.bouton_recap,
            command=self.show_recap_page)

        self.recap.pack(pady=(15, 15))

        # Trait 3
        self.trait_3 = ttk.Separator(
            self.bande_rouge,
            style='trait.TSeparator',
            orient='horizontal')
        self.trait_3.pack(fill='x', padx=35)

        # Bouton comparaison
        self.bouton_comparaison = ctk.CTkImage(
            light_image=Image.open('Images/bouton_comparaison.png'),
            dark_image=Image.open('Images/bouton_comparaison.png'),
            size=(40, 40))

        self.comparaison = ctk.CTkButton(
            self.bande_rouge,
            text='',
            fg_color='#F54E59',
            bg_color='#F54E59',
            hover_color='#CC2F39',
            width=50,
            height=50,
            image=self.bouton_comparaison,
            command=self.show_comparaison_page)

        self.comparaison.pack(pady=(15, 15))

        # Trait 4
        self.trait_4 = ttk.Separator(
            self.bande_rouge,
            style='trait.TSeparator',
            orient='horizontal')
        self.trait_4.pack(fill='x', padx=35)

        # Bouton analyse globale
        self.bouton_analyse = ctk.CTkImage(
            light_image=Image.open('Images/bouton_analyse.png'),
            dark_image=Image.open('Images/bouton_analyse.png'),
            size=(40, 40))

        self.analyse = ctk.CTkButton(
            self.bande_rouge,
            text='',
            fg_color='#F54E59',
            bg_color='#F54E59',
            hover_color='#CC2F39',
            width=50,
            height=50,
            image=self.bouton_analyse,
            command=self.show_analyse_page)

        self.analyse.pack(pady=(15, 15))

        # Trait 5
        self.trait_5 = ttk.Separator(
            self.bande_rouge,
            style='trait.TSeparator',
            orient='horizontal')
        self.trait_5.pack(fill='x', padx=35)

        # Bouton courbes
        self.bouton_courbes = ctk.CTkImage(
            light_image=Image.open('Images/bouton_courbes.png'),
            dark_image=Image.open('Images/bouton_courbes.png'),
            size=(40, 40))

        self.courbes = ctk.CTkButton(
            self.bande_rouge,
            text='',
            fg_color='#F54E59',
            bg_color='#F54E59',
            hover_color='#CC2F39',
            width=50,
            height=50,
            image=self.bouton_courbes,
            command=self.show_courbes_page)

        self.courbes.pack(pady=(15, 15))

        # Trait 6
        self.trait_6 = ttk.Separator(
            self.bande_rouge,
            style='trait.TSeparator',
            orient='horizontal')
        self.trait_6.pack(fill='x', padx=35)

        # Mentions légales
        self.mentions = ttk.Label(
            self.bande_rouge,
            text='©️ 2024 ProxiData\n Tous droits réservés',
            background='#F54E59',
            font=('Inter', 9),
            wraplength=150)
        self.mentions.pack(pady=(0, 25), side='bottom', anchor='s')

        self.master.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        self.resize_logo()

    def resize_logo(self, event=None):
        new_band_width = self.bande_rouge.winfo_width()

        if new_band_width > 0:
            logo_proxiserve = Image.open('Images/logo_proxiserve.png')
            new_logo_size = int(new_band_width * 0.5)
            if new_logo_size > 0:
                resized_logo = logo_proxiserve.resize((new_logo_size, new_logo_size))
                self.logo_image = ImageTk.PhotoImage(resized_logo)

                if self.logo:
                    self.logo.config(image=self.logo_image)
                    self.logo.pack(pady=(10, 10))

    def popupmsg(self):

        def center_window(root):
            root.update_idletasks()
            width = root.winfo_width()
            height = root.winfo_height()
            x = (root.winfo_screenwidth() // 2) - 175
            y = (root.winfo_screenheight() // 2) - 75
            root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        popup = tk.Toplevel(self.master)
        popup.title('Quitter ?')
        popup.geometry('350x150')
        popup.minsize(350, 150)
        popup.maxsize(350, 150)
        center_window(popup)

        popup.grab_set()

        label = ttk.Label(
            popup,
            text="Voulez-vous vraiment revenir à l'accueil ?",
            font=("Inter", 13, 'bold'))
        label.pack(pady=(30, 0))

        def non():
            popup.grab_release()
            popup.destroy()

        def oui():
            popup.grab_release()
            popup.destroy()
            from parcourir_page import ParcourirPage
            BandeRouge1(self.master)
            ParcourirPage(self.master)

        quitter_button = ctk.CTkButton(
            popup,
            text='Oui',
            fg_color='#F54E59',
            hover_color='#CC2F39',
            width=90,
            height=45,
            font=("Inter", 14),
            corner_radius=80,
            anchor='CENTER',
            command=oui)
        quitter_button.pack(side='left', padx=(60, 0), pady=(0, 10))

        annuler_button = ctk.CTkButton(
            popup,
            text='Non',
            fg_color='#F54E59',
            hover_color='#CC2F39',
            width=90,
            height=45,
            font=("Inter", 14),
            corner_radius=80,
            anchor='CENTER',
            command=non)
        annuler_button.pack(side='right', padx=(0, 60), pady=(0, 10))

        popup.mainloop()

    def show_recap_page(self):
        # Hide elements of the first page
        self.recap.configure(fg_color='#DE3A45', state='disabled')
        self.comparaison.configure(fg_color='#F54E59', state='normal')
        self.analyse.configure(fg_color='#F54E59', state='normal')
        self.courbes.configure(fg_color='#F54E59', state='normal')
        RecapPage(self.master)

    def show_comparaison_page(self):
        # Hide elements of the first page
        self.recap.configure(fg_color='#F54E59', state='normal')
        self.comparaison.configure(fg_color='#DE3A45', state='disabled')
        self.analyse.configure(fg_color='#F54E59', state='normal')
        self.courbes.configure(fg_color='#F54E59', state='normal')
        ComparaisonPage(self.master)

    def show_analyse_page(self):
        # Hide elements of the first page
        self.recap.configure(fg_color='#F54E59', state='normal')
        self.comparaison.configure(fg_color='#F54E59', state='normal')
        self.analyse.configure(fg_color='#DE3A45', state='disabled')
        self.courbes.configure(fg_color='#F54E59', state='normal')
        AnalysePage(self.master)

    def show_courbes_page(self):
        # Hide elements of the first page
        self.recap.configure(fg_color='#F54E59', state='normal')
        self.comparaison.configure(fg_color='#F54E59', state='normal')
        self.analyse.configure(fg_color='#F54E59', state='normal')
        self.courbes.configure(fg_color='#DE3A45', state='disabled')
        CourbesPage(self.master)

    def download_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", ".csv"), ("Excel files", ".xlsx;.xls"), ("All files", ".*")])

        if file_path:
            # Copy contents of predictions.csv to the destination file
            shutil.copyfile("Fiches/Output/predictions.csv", file_path)
