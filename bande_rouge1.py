from tkinter import ttk
from PIL import Image, ImageTk


class BandeRouge1:
    def __init__(self, master):
        self.master = master

        # Styles
        s = ttk.Style()
        s.configure('bande_rouge.TFrame', background='#F54E59')

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

        # Mentions légales
        mentions = ttk.Label(
            self.bande_rouge,
            text='©️ 2024 ProxiData\n Tous droits réservés',
            background='#F54E59',
            font=('Inter', 10))
        mentions.pack(side='bottom', pady=(0, 25), anchor='s')

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
                    self.logo.pack(pady=(50, 0))