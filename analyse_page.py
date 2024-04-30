import pickle
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from joblib import load
import numpy as np
import os
import Pmw

cols = ["CA Contrats Collectif", "ETP EFFECTIF Exploitation (Présence)", "Nbre de véhicules Exploitation",
        "TOTAL AUTRES COUTS_1", "TOTAL FRAIS GENERAUX_1", "ETP Chef Agence", "ETP Responsable Exploitation",
        "ETP Secrétaire/Assitant(e) Agence",
        "ETP EFFECTIF Agence (Présence)", "TOTAL VEHICULES_2", "TOTAL AUTRES COUTS_2", "TOTAL FRAIS GENERAUX_2",
        "Nombre de Tech. moyen par Chef Equipe", "Nombre de Tech. moyen par Magasinier",
        "Nombre de Techniciens par Secrétaire"]


class AnalysePage:

    def __init__(self, master):
        self.master = master

        # Styles
        s = ttk.Style()
        s.configure('partie_droite.TFrame', background="green")
        s.configure('frame_graphe_gauche.TFrame', background="blue")
        s.configure('frame_graphe_droite.TFrame', background="black")

        # Partie droite
        self.partie_droite = ttk.Frame(master)
        self.partie_droite.place(relx=0.15, y=0, relwidth=0.85, relheight=1)

        # Titre Proxidata
        self.agence = ttk.Label(
            self.partie_droite,
            text="Analyse Globale",
            foreground="#8F9093",
            font=("Inter", 25, 'bold'))
        self.agence.pack(pady=50)

        # Trait
        self.trait = ttk.Separator(self.partie_droite, orient='horizontal')
        self.trait.pack(fill='x', padx=50)

        # Frame segmented button
        self.frame_segmented_button = ttk.Frame(self.partie_droite)
        self.frame_segmented_button.pack(fill='x')

        # Segmented button
        self.type_agence = "BTB"
        self.agence_affichee = "Meilleures agences"
        self.segmented_button1_var = ctk.StringVar(value="Meilleures agences")
        self.segmented_button1 = ctk.CTkSegmentedButton(master=self.frame_segmented_button,
                                                        values=["Meilleures agences", "Pires agences",
                                                                "Toutes les agences"],
                                                        variable=self.segmented_button1_var,
                                                        font=("Inter", 16),
                                                        fg_color='#F54E59',
                                                        selected_color='#DE3A45',
                                                        selected_hover_color='#CC2F39',
                                                        unselected_color='#F54E59',
                                                        unselected_hover_color='#DE3A45',
                                                        command=self.afficher_graphe_gauche)
        self.segmented_button1.pack(padx=(100, 0), pady=(10, 0), side='left')

        self.segmented_button2_var = ctk.StringVar(value="   BTB   ")
        self.segmented_button2 = ctk.CTkSegmentedButton(master=self.frame_segmented_button,
                                                        values=["   BTB   ", "   BTC   "],
                                                        variable=self.segmented_button2_var,
                                                        font=("Inter", 16),
                                                        fg_color='#F54E59',
                                                        selected_color='#DE3A45',
                                                        selected_hover_color='#CC2F39',
                                                        unselected_color='#F54E59',
                                                        unselected_hover_color='#DE3A45',
                                                        command=self.afficher_both_graphes)
        self.segmented_button2.pack(padx=(0, 100), pady=(10, 0), side='right')

        self.tooltip_label = ttk.Label(self.partie_droite, text="Informations ici !")
        self.tooltip_label.pack()

        tooltip_text = """  Que signifie l'importance d'une KPI ? L'importance d'une KPI, déterminée ici par un modèle
  de machine Learning de type Random Forest, ne correspond pas à son impact direct sur le TMB (Taux de Marge
  Brute), mais à son lien statistique avec le TMB. Plus clairement, un changement sur une KPI avec une grande
  importance se traduira par un changement conséquent du TMB. À l'inverse, la variation d'une KPI peu
  importante ne modifiera que très peu le TMB.

  À gauche, le graphique montre l'importance des KPI clés pour différents groupes d'agences (les 15
  meilleures, les 15 pires ou toutes les agences), le tout selon leur domaine d'activité (BTB ou BTC).

  À droite, le graphique montre la différence d'importance entre les 15 meilleures agences et les 15
  pires, toujours selon le domaine d'activité."""
        self.balloon = Pmw.Balloon(self.tooltip_label)
        self.balloon.bind(self.tooltip_label, tooltip_text)

        # Frame graphes
        self.frame_graphes = ttk.Frame(self.partie_droite)
        self.frame_graphes.pack(fill='both', expand=True, pady=(120, 0))

        # Frame graphe gauche
        self.frame_graphe_gauche = ttk.Frame(self.frame_graphes)
        self.frame_graphe_gauche.pack(fill='both', side='left', expand=True)

        # Images analyse agences
        self.image_analyse_meilleures_BTB = tk.PhotoImage(file="Images/analyse_meilleures_BTB.png")
        self.image_analyse_pires_BTB = tk.PhotoImage(file="Images/analyse_pires_BTB.png")
        self.image_analyse_toutes_BTB = tk.PhotoImage(file="Images/analyse_toutes_BTB.png")
        self.image_analyse_meilleures_BTC = tk.PhotoImage(file="Images/analyse_meilleures_BTC.png")
        self.image_analyse_pires_BTC = tk.PhotoImage(file="Images/analyse_pires_BTC.png")
        self.image_analyse_toutes_BTC = tk.PhotoImage(file="Images/analyse_toutes_BTC.png")

        # Labels d'analyse
        self.label_analyse_meilleures_BTB = ttk.Label(self.frame_graphe_gauche,
                                                      image=self.image_analyse_meilleures_BTB)
        self.label_analyse_pires_BTB = ttk.Label(self.frame_graphe_gauche,
                                                 image=self.image_analyse_pires_BTB)
        self.label_analyse_toutes_BTB = ttk.Label(self.frame_graphe_gauche,
                                                  image=self.image_analyse_toutes_BTB)
        self.label_analyse_meilleures_BTC = ttk.Label(self.frame_graphe_gauche,
                                                      image=self.image_analyse_meilleures_BTC)
        self.label_analyse_pires_BTC = ttk.Label(self.frame_graphe_gauche,
                                                 image=self.image_analyse_pires_BTC)
        self.label_analyse_toutes_BTC = ttk.Label(self.frame_graphe_gauche,
                                                  image=self.image_analyse_toutes_BTC)

        # Frame graphe droite
        self.frame_graphe_droite = ttk.Frame(self.frame_graphes)
        self.frame_graphe_droite.pack(fill='both', side='right', expand=True)

        # Images analyse différences
        self.image_analyse_differences_BTB = tk.PhotoImage(file="Images/analyse_differences_BTB.png")
        self.image_analyse_differences_BTC = tk.PhotoImage(file="Images/analyse_differences_BTC.png")

        self.label_analyse_differences_BTB = ttk.Label(self.frame_graphe_droite,
                                                       image=self.image_analyse_differences_BTB)
        self.label_analyse_differences_BTC = ttk.Label(self.frame_graphe_droite,
                                                       image=self.image_analyse_differences_BTC)

        # Afficher le premier graphe de gauche
        self.label_analyse_meilleures_BTB.pack()
        # # Afficher le premier graphe de droite
        self.label_analyse_differences_BTB.pack()

    # Afficher le graphe de gauche
    def afficher_graphe_gauche(self, value):

        if self.type_agence == "BTB":
            if value == "Meilleures agences":
                self.agence_affichee = "Meilleures agences"
                self.label_analyse_meilleures_BTB.pack()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.forget()

            elif value == "Pires agences":
                self.agence_affichee = "Pires agences"
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.pack()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.forget()

            elif value == "Toutes les agences":
                self.agence_affichee = "Toutes les agences"
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.pack()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.forget()

        elif self.type_agence == "BTC":
            if value == "Meilleures agences":
                self.agence_affichee = "Meilleures agences"
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.pack()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.forget()

            elif value == "Pires agences":
                self.agence_affichee = "Pires agences"
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.pack()
                self.label_analyse_toutes_BTC.forget()

            elif value == "Toutes les agences":
                self.agence_affichee = "Toutes les agences"
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.pack()

        if value == "   BTB   ":
            self.type_agence = "BTB"

            if self.agence_affichee == "Meilleures agences":
                self.label_analyse_meilleures_BTB.pack()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.forget()

            elif self.agence_affichee == "Pires agences":
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.pack()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.forget()

            elif self.agence_affichee == "Toutes les agences":
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.pack()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.forget()

        if value == "   BTC   ":
            self.type_agence = "BTC"

            if self.agence_affichee == "Meilleures agences":
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.pack()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.forget()

            elif self.agence_affichee == "Pires agences":
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.pack()
                self.label_analyse_toutes_BTC.forget()

            elif self.agence_affichee == "Toutes les agences":
                self.label_analyse_meilleures_BTB.forget()
                self.label_analyse_pires_BTB.forget()
                self.label_analyse_toutes_BTB.forget()
                self.label_analyse_meilleures_BTC.forget()
                self.label_analyse_pires_BTC.forget()
                self.label_analyse_toutes_BTC.pack()

    # Afficher le graphe de droite
    def afficher_graphe_droite(self, value):

        if value == "   BTB   ":
            self.type_agence = "BTB"
            self.label_analyse_differences_BTB.pack()
            self.label_analyse_differences_BTC.forget()

        if value == "   BTC   ":
            self.type_agence = "BTC"
            self.label_analyse_differences_BTB.forget()
            self.label_analyse_differences_BTC.pack()

    # Afficher les deux graphes
    def afficher_both_graphes(self, value):
        self.afficher_graphe_gauche(value)
        self.afficher_graphe_droite(value)
