from tkinter import ttk
import customtkinter as ctk
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from import_data import import_fiche, import_ref, select_agences


class RecapPage:
    def __init__(self, master):
        self.master = master

        # Styles
        s = ttk.Style()
        s.configure('partie_droite.TFrame', background='green')
        s.configure('partie_droite.TFrame', background="#F1F1F1")
        s.configure('trait.TSeparator', background='black')

        # Partie droite
        self.partie_droite = ttk.Frame(master)
        self.partie_droite.place(relx=0.15, y=0, relwidth=0.85, relheight=1)

        # Titre Proxidata
        self.agence = ttk.Label(
            self.partie_droite,
            text="Récapitulatif de l'agence",
            foreground='#8F9093',
            font=("Inter", 25, 'bold'))
        self.agence.pack(pady=50)

        # Trait
        self.trait = ttk.Separator(self.partie_droite, orient='horizontal')
        self.trait.pack(fill='x', padx=(50))

        self.frame_menu_deroulant = ttk.Frame(self.partie_droite, style='frame_menu_deroulant.TFrame')
        self.frame_menu_deroulant.pack(pady=25)

        self.bouton = ctk.CTkButton(
            self.frame_menu_deroulant,
            text='Valider',
            fg_color='#F54E59',
            hover_color='#C33841',
            height=25,
            width=100,
            font=("Inter", 16),
            corner_radius=80,
            command=self.update_graph)  # Call update_graph when the button is clicked
        self.bouton.pack(side='right')

        # Menu déroulant


        # Graphique
        df_year2 = pd.read_excel('Fiches/df_year.xlsx')

        global norm_btc, norm_btb, agencies, rename_dict

        norm_btc = pd.read_excel('Fiches/norm_btc.xlsx')
        norm_btb = pd.read_excel('Fiches/norm_btb.xlsx')

        agencies = pd.concat([norm_btb, norm_btc])

        from file_manager import FileManager
        filename = FileManager.get_filename()
        df = import_fiche(filename)
        glob_df = import_ref("Fiches/Benchmark Classement Agences REEL 2022 et REEL 2023.xlsx")
        final_df = select_agences(df, glob_df)

        tmp = pd.DataFrame()
        tmp["Taux MARGE BRUTE"] = 100 * final_df["MARGE BRUTE"]/final_df["TOTAL CA + Prod Centralisées"]
        final_df = pd.concat([final_df, tmp], axis=1)
        final_df = final_df[(final_df["Taux MARGE BRUTE"] < 100) & (final_df["Taux MARGE BRUTE"] > -100)]

        final_df["Date"] = final_df["Date"].astype(float)
        df_year = final_df[(final_df['Date'] > 100) & (final_df['Type'] =="REEL")]

        # Supprimer les doublons de date pour chaque agence
        df_year = df_year.drop_duplicates(subset=["Filtre Agence", "Date"])
        df_year["Date"] = pd.to_datetime(df_year["Date"], format='%Y')
        agence_choisie = df_year[(df_year["Date"]=="2023-01-01")]
        agence_choisie = agence_choisie[agence_choisie["AGENCE"] == agence_choisie["AGENCE"].unique()[0]]
        agence_choisie["AGENCE"] = agence_choisie["AGENCE"].astype(str)
        noms = sorted([str(noms) for noms in agencies["name_sheet"].unique()])
        #ajouter la ligne agence_choisie à la première ligne dans noms
        noms.insert(0, str(agence_choisie['name_sheet'].iloc[0]))

        self.df_year2 = df_year2

        nom_agence = noms[0]  # Le nom de l'agence que l'on va choisir (la c'est la première de la liste mais voila)
        # nom_agence
        df_agence_unique = df_year[df_year["name_sheet"] == nom_agence].sort_values("Date")
        # df_agence_unique

        # Graph 1 (taux marge brute):
        self.fig, (self.ax1, self.ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 5))  # Create two subplots

        # Premier sous-tracé
        self.ax1.plot(df_agence_unique['Date'], df_agence_unique['Taux MARGE BRUTE'], marker='o')
        self.ax1.set_title('Évolution du Taux de marge brute par année pour ' + nom_agence)
        self.ax1.set_xlabel('Année')
        self.ax1.set_ylabel('Taux de marge brute (en %)')
        self.ax1.grid(True)

        # Deuxième sous-tracé
        self.ax2.plot(df_agence_unique['Date'], df_agence_unique['TOTAL CA + Prod Centralisées'], marker='o', color='red')
        self.ax2.set_title('Évolution du Chiffre d\'affaires par année pour ' + nom_agence)
        self.ax2.set_xlabel('Année')
        self.ax2.set_ylabel('Chiffre d\'affaire + Production Centralisée (en milliers)')
        self.ax2.grid(True)

        self.fig.patch.set_facecolor('#F1F1F1')

        self.menu_deroulant = ttk.Combobox(self.frame_menu_deroulant, values=noms, state='readonly', width=50)
        self.menu_deroulant.pack(padx=10, pady=20, side='right')

        # Créer le canvas et l'ajouter à la frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.partie_droite)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def update_graph(self):
        # Clear the existing axes
        self.ax1.clear()
        self.ax2.clear()

        # Get the selected agency
        nom_agence = self.menu_deroulant.get()

        # Generate the data for the selected agency
        df_agence_unique = self.df_year2[self.df_year2["name_sheet"] == nom_agence].sort_values("Date")

        # Update the first subplot
        self.ax1.plot(df_agence_unique['Date'], df_agence_unique['Taux MARGE BRUTE'], marker='o')
        print(df_agence_unique['Taux MARGE BRUTE'])
        print(df_agence_unique['Date'])
        self.ax1.set_title('Évolution du Taux de marge brute par année pour ' + nom_agence)
        self.ax1.set_xlabel('Année')
        self.ax1.set_ylabel('Taux de marge brute (en %)')
        self.ax1.grid(True)

        # Update the second subplot
        self.ax2.plot(df_agence_unique['Date'], df_agence_unique['TOTAL CA + Prod Centralisées'], marker='o',
                      color='red')
        self.ax2.set_title('Évolution du Chiffre d\'affaires par année pour ' + nom_agence)
        self.ax2.set_xlabel('Année')
        self.ax2.set_ylabel('Chiffre d\'affaire + Production Centralisée (en milliers)')
        self.ax2.grid(True)

        self.fig.patch.set_facecolor('#F1F1F1')

        # Redraw the canvas with the updated figure
        self.canvas.draw()