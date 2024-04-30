import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk

# Fenêtre principale
window = tk.Tk()
window.title('v5')
window.geometry('1000x700')
window.minsize(500,500)

# Bande rouge
s = ttk.Style()
s.configure('bande_rouge.TFrame', background='#F54E59')
s.configure('partie_droite.TFrame', background='green')

bande_rouge = ttk.Frame(window, style='bande_rouge.TFrame')
bande_rouge.place(x=0,y=0,relwidth=0.3, relheight=1)

# Logo
logo_proxiserve = Image.open('logo_proxiserve.png')
resized_logo = logo_proxiserve.resize((175, 175))
logo_final = ImageTk.PhotoImage(resized_logo)

logo = ttk.Label(
    bande_rouge,
    image=logo_final,
    background='#F54E59',
    width=15)
logo.pack(pady=(50,0))

# Mentions légales
mentions = ttk.Label(
    bande_rouge,
    text='©️ 2024 ProxiData. Tous droits réservés',
    background='#F54E59',
    font=('Inter', 10))
mentions.pack(pady=(400,0))

# Partie droite
partie_droite = ttk.Frame(window)
partie_droite.place(relx=0.3,y=0,relwidth=0.7,relheight=1)

# # Titre Proxidata
# proxidata = ttk.Label(
#     partie_droite,
#     text="ProxiData",
#     foreground='#F54E59',
#     font=("Inter", 25, 'bold'),
#     anchor='center')
# proxidata.pack(pady=50)
# Titre
image_titre = Image.open('image_titre.png')
resized_titre = image_titre.resize((243,42))
titre_final = ImageTk.PhotoImage(resized_titre)

titre = ttk.Label(
    partie_droite,
    image=titre_final,
    background='#F1F1F1')
titre.pack(pady=50)

#  Image Accueil
image_accueil = Image.open('Images/image_accueil.png')
resized_image = image_accueil.resize((500,200))
image_finale = ImageTk.PhotoImage(resized_image)

label_image = ttk.Label(
    partie_droite,
    image=image_finale)
label_image.pack(pady=(75,0))

def popupmsg():

    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - 175
        y = (window.winfo_screenheight() // 2) - 75
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    popup = tk.Toplevel(window)
    popup.title('Quitter ?')
    popup.geometry('350x150')
    popup.minsize(350,150)
    popup.maxsize(350,150)
    center_window(popup)

    popup.grab_set()

    label = ttk.Label(
        popup,
        text="Voulez-vous vraiment revenir à l'accueil ?",
        font=("Inter", 13, 'bold'))
    label.pack(pady=(30,0))

    def quitter():
        popup.grab_release()
        popup.destroy()

    quitter_button = ctk.CTkButton(
        popup,
        text='Oui',
        fg_color='#F54E59',
        hover_color='#C33841',
        width=90,
        height=45,
        font=("Inter", 14),
        corner_radius=80,
        anchor='CENTER',
        command=quitter)
    quitter_button.pack(side='left', padx=(60, 0), pady=(0, 10))

    annuler_button = ctk.CTkButton(
        popup,
        text='Non',
        fg_color='#F54E59',
        hover_color='#C33841',
        width=90,
        height=45,
        font=("Inter", 14),
        corner_radius=80,
        anchor='CENTER',
        command=quitter)
    annuler_button.pack(side='right', padx=(0, 60), pady=(0, 10))

    popup.mainloop()

# Bouton entrer
bouton_entrer = ctk.CTkButton(
    partie_droite,
    text='Entrer',
    fg_color='#F54E59',
    hover_color='#C33841',
    height=75,
    width=150,
    font=("Inter", 18),
    corner_radius=80,
    anchor='CENTER',
    command=popupmsg)
bouton_entrer.pack(pady=(175,0))

window.mainloop()