import tkinter as tk
from tkinter import ttk

import Pmw
import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from import_data import import_fiche, import_ref, select_agences
import Pmw

class CourbesPage:
    
    def __init__(self, master):
        self.master = master
        self.canvas = None

        # Styles
        s = ttk.Style()
        s.configure('frame_menu_deroulant.TFrame', background='#F1F1F1')
        s.configure('partie_droite.TFrame', background='#F1F1F1')
        s.configure('trait.TSeparator', background='black')

        # Partie droite
        self.partie_droite = ttk.Frame(master, style='partie_droite.TFrame')
        self.partie_droite.place(relx=0.15, y=0.3, relwidth=0.85, relheight=1)

        # Titre Proxidata
        self.agence = ttk.Label(
            self.partie_droite,
            text="Analyse des performances des agences",
            foreground='#8F9093',
            font=("Inter", 25, 'bold'))
        self.agence.pack(pady=50)

        # Trait
        self.trait = ttk.Separator(self.partie_droite, orient='horizontal')
        self.trait.pack(fill='x', padx=(50))

        # Frame Menu déroulant
        self.frame_menu_deroulant = ttk.Frame(self.partie_droite, style='frame_menu_deroulant.TFrame')
        self.frame_menu_deroulant.pack(pady=25)

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

        # Menu déroulant
        self.menu_deroulant = ttk.Combobox(self.frame_menu_deroulant, values=noms, state='readonly', width=50)
        self.menu_deroulant.pack(padx=10, pady=20, side='left')

        # Menu déroulant
        self.menu_deroulant2 = ttk.Combobox(self.frame_menu_deroulant, values=["% / (CA+Prod.Centralisées)_Marge_Agence", "% / (CA+Prod.Centralisées)_Marge_Brute", "% / (CA+Prod.Centralisées)_Depences_exploitation",
            "% / (CA+Prod.Centralisées)_Total_Salaire_Exploitation", "% Absences Exploitation", '% / (CA+Prod.Centralisées)_Total_Fourniture',
            "% TOTAL FRAIS GENERAUX_1", "% TOTAL FRAIS GENERAUX_2"], state='readonly', width=50)
        self.menu_deroulant2.pack(padx=10, pady=20, side='left')

        # Bouton
        self.bouton = ctk.CTkButton(
            self.frame_menu_deroulant,
            text='Valider',
            fg_color='#F54E59',
            hover_color='#C33841',
            height=25,
            width=100,
            font=("Inter", 16),
            corner_radius=80,
            command=self.plot_data)
        self.bouton.pack(side='right')

        self.tooltip_label = ttk.Label(self.partie_droite, text="Informations ici!")
        self.tooltip_label.pack()

        tooltip_text = """
                                Ce graphique en nuage de points permet de situer l'agence à analyser par rapport 
                                aux autres agences du même domaine d'activité (BTB ou BTC) selon plusieurs KPI. 
                                Sur l'axe des abscisses, on retrouve le taux de marge brute et sur l'axe des ordonnées, 
                                le KPI sélectionné. Chaque point bleu correspond à une agence 
                                et le point noir correspond à l'agence à analyser.
                            
                        Ce graphique en nuage de points permet de situer l'agence à analyser par rapport 
                        aux autres agences du même domaine d'activité (BTB ou BTC) selon plusieurs KPI. 
                        Sur l'axe des abscisses, on retrouve le taux de marge brute et sur l'axe des ordonnées, 
                        le KPI sélectionné. Chaque point bleu correspond à une agence 
                        et le point noir correspond à l'agence à analyser.
                        """
        self.balloon = Pmw.Balloon(self.tooltip_label)
        self.balloon.bind(self.tooltip_label, tooltip_text)

        rename_dict = {
            '% / (CA+Prod.Centralisées)_1': '% / (CA+Prod.Centralisées)_Total_Fourniture',
            '% / (CA+Prod.Centralisées)_2': '% / (CA+Prod.Centralisées)_Total_Salaire_Exploitation',
            '% / (CA+Prod.Centralisées)_3': '% / (CA+Prod.Centralisées)_Total_Vehicules_Exploitation',
            '% / (CA+Prod.Centralisées)_4': '% / (CA+Prod.Centralisées)_Total_Autres_couts_Exploitation',
            '% / (CA+Prod.Centralisées)_5': '% / (CA+Prod.Centralisées)_Total_Frais_Generaux_Exploitation',
            '% / (CA+Prod.Centralisées)_6': '% / (CA+Prod.Centralisées)_Depences_exploitation',
            '% / (CA+Prod.Centralisées)_7': '% / (CA+Prod.Centralisées)_Marge_Brute',
            '% / (CA+Prod.Centralisées)_8': '% / (CA+Prod.Centralisées)_Total_Salaire_Agence',
            '% / (CA+Prod.Centralisées)_9': '% / (CA+Prod.Centralisées)_Total_Vehicules_Agence',
            '% / (CA+Prod.Centralisées)_10': '% / (CA+Prod.Centralisées)_Total_Autres_Couts_Agence',
            '% / (CA+Prod.Centralisées)_11': '% / (CA+Prod.Centralisées)_Total_Frais_Generaux_Agence',
            '% / (CA+Prod.Centralisées)_12': '% / (CA+Prod.Centralisées)_Resultat_Exceptionel',
            '% / (CA+Prod.Centralisées)_13': '% / (CA+Prod.Centralisées)_Depence_Agence',
            '% / (CA+Prod.Centralisées)_14': '% / (CA+Prod.Centralisées)_Marge_Agence',
            '% / (CA+Prod.Centralisées)_15': '% / (CA+Prod.Centralisées)_Depenses_DR',
            '% / (CA+Prod.Centralisées)_16': '% / (CA+Prod.Centralisées)_Marge_Region',
            '% Absences_1': '% Absences Exploitation',
            '% Absences_2': '% Absences Agence',
        }

        selected_axe_y = '% TOTAL FRAIS GENERAUX_1'

        

        agence_choisie["% CA Contrat Collectif"] = agence_choisie["CA Contrats Collectif"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["CA Contrats Collectif"], inplace=True)

        agence_choisie["% ETP EFFECTIF Exploitation (Présence)"] = agence_choisie["ETP EFFECTIF Exploitation (Présence)"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["ETP EFFECTIF Exploitation (Présence)"], inplace=True)

        agence_choisie["% Nbre de véhicules Exploitation"] = agence_choisie["Nbre de véhicules Exploitation"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["Nbre de véhicules Exploitation"], inplace=True)

        agence_choisie["% TOTAL AUTRES COUTS_1"] = agence_choisie["TOTAL AUTRES COUTS_1"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["TOTAL AUTRES COUTS_1"], inplace=True)

        agence_choisie["% TOTAL FRAIS GENERAUX_1"] = agence_choisie["TOTAL FRAIS GENERAUX_1"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["TOTAL FRAIS GENERAUX_1"], inplace=True)

        agence_choisie["% ETP Chef Agence"] = agence_choisie["ETP Chef Agence"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["ETP Chef Agence"], inplace=True)

        agence_choisie["% ETP Responsable Exploitation"] = agence_choisie["ETP Responsable Exploitation"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["ETP Responsable Exploitation"], inplace=True)

        agence_choisie["% ETP Secrétaire/Assitant(e) Agence"] = agence_choisie["ETP Secrétaire/Assitant(e) Agence"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["ETP Secrétaire/Assitant(e) Agence"], inplace=True)

        agence_choisie["% ETP EFFECTIF Agence (Présence)"] = agence_choisie["ETP EFFECTIF Agence (Présence)"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["ETP EFFECTIF Agence (Présence)"], inplace=True)

        agence_choisie["% TOTAL VEHICULES_2"] = agence_choisie["TOTAL VEHICULES_2"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["TOTAL VEHICULES_2"], inplace=True)

        agence_choisie["% TOTAL AUTRES COUTS_2"] = agence_choisie["TOTAL AUTRES COUTS_2"]/agence_choisie["TOTAL CA + Prod Centralisées"]
        agence_choisie.drop(columns=["TOTAL AUTRES COUTS_2"], inplace=True)

        agence_choisie.rename(columns=rename_dict, inplace=True)

        nom = agence_choisie["name_sheet"].iloc[0]
        # Setup figure and axes
        fig, ax = plt.subplots(figsize=(14, 5))
        fig.patch.set_facecolor('#F1F1F1')

        axe_x = 'Taux MARGE BRUTE'
        # axe_x = 'classement'
        axe_y = selected_axe_y

        # Check if the chosen agency has any data
        if not agence_choisie.empty:
            activity_type = agence_choisie["ACTIVITE"].iloc[0]  # Get activity type from data

            if activity_type == "BTC":
                ax.plot(norm_btc[axe_x], norm_btc[axe_y], marker='o', color='blue', label='BTC Data')
                z_btc = np.polyfit(norm_btc[axe_x].astype(float), norm_btc[axe_y].astype(float), 1)  # Fit trend line for BTC
                p_btc = np.poly1d(z_btc)
                ax.plot(norm_btc[axe_x], p_btc(norm_btc[axe_x]), "r--", label='BTC Trend Line')
            elif activity_type == "BTB":
                ax.plot(norm_btb[axe_x], norm_btb[axe_y], marker='o', color='green', label='BTB Data')
                z_btb = np.polyfit(norm_btb[axe_x].astype(float), norm_btb[axe_y].astype(float), 1)  # Fit trend line for BTB
                p_btb = np.poly1d(z_btb)
                ax.plot(norm_btb[axe_x], p_btb(norm_btb[axe_x]), "r--", label='BTB Trend Line')
            # Annotate and highlight specific data points for the chosen agency
            for _, row in agence_choisie.iterrows():
                ax.scatter(row[axe_x], row[axe_y], facecolor='black', edgecolors='black', s=50, zorder=5)  # Plot the point in black
                ax.annotate(f"{row[axe_y]:.2f}", (row[axe_x], row[axe_y]), textcoords="offset points", xytext=(0,10), ha='center', color='black')

            # Setting titles and labels
            ax.set_title(f"{axe_y} en fonction du Taux de marge brute : Agence {nom}")
            ax.set_xlabel(axe_x)
            ax.set_ylabel(f"{axe_y}")
            ax.legend()

            # variable y
            # Clear the existing plot
            if self.canvas is not None:
                self.canvas.get_tk_widget().destroy()

            # Embed the new plot into the tkinter canvas
            self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.partie_droite)
            self.canvas.get_tk_widget().pack()
            self.canvas.draw()
            
        else:
            print("No data available for the specified agency.")

    def plot_data(self):

        # Get the selected agency from the combobox
        selected_agency = self.menu_deroulant.get()

        # Get the selected agency from the combobox
        selected_axe_y = self.menu_deroulant2.get()
    
        # Filter the DataFrame based on the selected agency
        agence_choisie = agencies[agencies["name_sheet"] == selected_agency]

        nom = agence_choisie["name_sheet"].iloc[0]
        # Setup figure and axes
        fig, ax = plt.subplots(figsize=(14, 5))
        fig.patch.set_facecolor('#F1F1F1')

        axe_x = 'Taux MARGE BRUTE'
        # axe_x = 'classement'
        axe_y = selected_axe_y

        # Check if the chosen agency has any data
        if not agence_choisie.empty:
            activity_type = agence_choisie["ACTIVITE"].iloc[0]  # Get activity type from data

            if activity_type == "BTC":
                ax.plot(norm_btc[axe_x], norm_btc[axe_y], marker='o', color='blue', label='BTC Data')
                z_btc = np.polyfit(norm_btc[axe_x].astype(float), norm_btc[axe_y].astype(float), 1)  # Fit trend line for BTC
                p_btc = np.poly1d(z_btc)
                ax.plot(norm_btc[axe_x], p_btc(norm_btc[axe_x]), "r--", label='BTC Trend Line')
            elif activity_type == "BTB":
                ax.plot(norm_btb[axe_x], norm_btb[axe_y], marker='o', color='green', label='BTB Data')
                z_btb = np.polyfit(norm_btb[axe_x].astype(float), norm_btb[axe_y].astype(float), 1)  # Fit trend line for BTB
                p_btb = np.poly1d(z_btb)
                ax.plot(norm_btb[axe_x], p_btb(norm_btb[axe_x]), "r--", label='BTB Trend Line')
            # Annotate and highlight specific data points for the chosen agency
            for _, row in agence_choisie.iterrows():
                ax.scatter(row[axe_x], row[axe_y], facecolor='black', edgecolors='black', s=50, zorder=5)  # Plot the point in black
                ax.annotate(f"{row[axe_y]:.2f}", (row[axe_x], row[axe_y]), textcoords="offset points", xytext=(0,10), ha='center', color='black')

            # Setting titles and labels
            ax.set_title(f"{axe_y} en fonction du Taux de marge brute : Agence {nom}")
            ax.set_xlabel(axe_x)
            ax.set_ylabel(f"{axe_y}")
            ax.legend()


            # Clear the existing plot
            if self.canvas is not None:
                self.canvas.get_tk_widget().destroy()

            # Embed the new plot into the tkinter canvas
            self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.partie_droite)
            self.canvas.get_tk_widget().pack()
            self.canvas.draw()

        else:
            print("No data available for the specified agency.")

