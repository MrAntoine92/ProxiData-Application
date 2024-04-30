import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.io as pio
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dash_canvas import DashCanvas
import plotly.offline as pyo
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO
from import_data import import_fiche, import_ref, select_agences


class ComparaisonPage:
    def __init__(self, master):
        self.master = master

        # Styles
        s = ttk.Style()
        s.configure('partie_droite.TFrame', background='green')
        s.configure('trait.TSeparator', background='black')

        # Partie droite
        self.partie_droite = ttk.Frame(master)
        self.partie_droite.place(relx=0.15, y=0, relwidth=0.85, relheight=1)

        # Titre Proxidata
        self.agence = ttk.Label(
            self.partie_droite,
            text="Comparaison avec la meilleure agence",
            foreground='#8F9093',
            font=("Inter", 25, 'bold'))
        self.agence.pack(pady=50)

        # Trait
        self.trait = ttk.Separator(self.partie_droite, orient='horizontal')
        self.trait.pack(fill='x', padx=50)

        global df, norm

        df_year2 = pd.read_excel('Fiches/df_year.xlsx')
        norm = pd.read_excel('Fiches/norm.xlsx')

        global norm_btc, norm_btb, rename_dict

        best_agence_BTC = \
            df_year2[(df_year2["Date"] == "2023-01-01") & (df_year2["ACTIVITE"] == "BTC")].groupby("Filtre Agence")[
                "Taux MARGE BRUTE"].mean().sort_values(ascending=False).head(15)
        best_agence_BTB = \
            df_year2[(df_year2["Date"] == "2023-01-01") & (df_year2["ACTIVITE"] == "BTB")].groupby("Filtre Agence")[
                "Taux MARGE BRUTE"].mean().sort_values(ascending=False).head(15)

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

        # Choisir le filtre de l'agence
        filtre_agence = agence_choisie["Filtre Agence"].iloc[0]

        nom_agence = agence_choisie[agence_choisie["Filtre Agence"] == filtre_agence]["AGENCE"].iloc[0]
        tab_agence = norm[norm["Filtre Agence"] == filtre_agence].drop(columns=["Filtre Agence"]).mean()
        tab_agence.rename(nom_agence, inplace=True)

        tab_best_BTC = norm[norm["Filtre Agence"].isin(best_agence_BTC.index)].drop(columns=["Filtre Agence"]).mean()
        tab_best_BTB = norm[norm["Filtre Agence"].isin(best_agence_BTB.index)].drop(columns=["Filtre Agence"]).mean()

        tab_best_BTB.rename("Meilleures agences", inplace=True)
        tab_best_BTC.rename("Meilleures agences", inplace=True)

        if agence_choisie[agence_choisie["Filtre Agence"] == filtre_agence]["ACTIVITE"].iloc[0] == "BTC":
            print("Agence BTC")
            tab_best = tab_best_BTC
        else:
            print("Agence BTB")
            tab_best = tab_best_BTB

        tab = pd.concat([tab_agence, tab_best], axis=1)
        tab.index.name = "KPIs"
        for i in range(3, tab.shape[0]):
            tab.iloc[i] = (tab.iloc[i] * 100)
        tab = tab.round(3)
        tab.reset_index(inplace=True)

        ecart = np.abs((tab['Meilleures agences'] - tab[nom_agence]) / tab['Meilleures agences']) * 8
        ecart[ecart > 8] = 8

        color_scale = [n_colors('rgb(68,206,27)', 'rgb(187,219,68)', 3, colortype='rgb') +
                       n_colors('rgb(187,219,68)', 'rgb(247,227,121)', 3, colortype='rgb')[1:] +
                       n_colors('rgb(247,227,121)', 'rgb(242,161,52)', 3, colortype='rgb')[1:] +
                       n_colors('rgb(242,161,52)', 'rgb(229,31,31)', 3, colortype='rgb')[1:]
                       ][0]
        colors = [color_scale[int(i)] for i in ecart]

        # Create the Plotly table
        fig = go.Figure(data=[go.Table(
            header=dict(values=tab.columns.tolist(),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[tab["KPIs"], tab[nom_agence], tab['Meilleures agences']],
                       fill_color=['lavender', colors, 'lavender'],  # apply the color array to the second column
                       align='left',
                       line=dict(color='white', width=0.01)
                       ))
        ])

        fig.update_layout(
            autosize=True,
            paper_bgcolor="#F1F1F1",
        )

        fig.update_layout(
            autosize=False,
            margin=dict(
                l=0,  # left margin
                r=0,  # right margin
                b=0,  # bottom margin
                t=0,  # top margin
                pad=0  # padding
            )
        )
        # Convert the Plotly figure to a bytes object
        fig_bytes = go.Figure(fig).to_image(format="png")

        # Convert bytes to numpy array
        s = BytesIO(fig_bytes)
        img = mpimg.imread(s, format='PNG')

        # Create a new matplotlib figure and set its data
        mpl_fig, ax = plt.subplots()
        mpl_fig.patch.set_facecolor('#F1F1F1')
        ax.imshow(img, aspect='equal')
        ax.set_facecolor('#F1F1F1')
        ax.axis('off')


        # Create a new tkinter canvas
        canvas = FigureCanvasTkAgg(mpl_fig, master=self.partie_droite)
        canvas.draw()

        # Pack the canvas into the frame
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=0, pady=0)