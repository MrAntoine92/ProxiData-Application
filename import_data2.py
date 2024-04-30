# Ce module permet d'importer les données 
# A partir de fichiers excel de référence
import pandas as pd
# Permer de lire tous les xls d un répertoire donné
import glob
import os


def import_ref(ref_path):
    """
    Importe les données de référence à partir d'un fichier Excel spécifié.

    Parameters:
    - ref_path (str): Le chemin du fichier Excel contenant les données de référence.

    Returns:
    - pd.DataFrame: Un DataFrame contenant les données de référence importées.

    Description:
    Cette fonction prend en entrée le chemin d'un fichier Excel contenant des données
    de référence. Elle extrait les informations nécessaires des feuilles BTB et BTC du
    fichier Excel, puis les organise dans un DataFrame structuré et propre.

    Exemple d'utilisation :
    ```
    ref_data = import_ref('Data/Benchmark Classement Agences REEL 2022 et REEL 2023.xlsx')
    ```

    Note : Assurez-vous que le fichier Excel spécifié contient les feuilles BTB et BTC
    avec la structure attendue pour le bon fonctionnement de cette fonction.
    """
    # Set le dataframe à retourner
    df_return = pd.DataFrame()
    # Récupère les feuilles Excel
    excel_file = pd.ExcelFile(ref_path)
    sheet_names = excel_file.sheet_names
    #
    # Récupère le BTB
    #
    sheet_BTB = excel_file.parse(sheet_names[0])
    # Récupère les noms des colonnes
    df_columns = sheet_BTB.iloc[1, 1:23].values
    # Récupère les années nécessaires sur certaines colonnes
    df_columns[18] = 'EBIT 2023'
    df_columns[19] = 'Taux EBIT 2023'
    df_columns[20] = 'EBIT 2022'
    df_columns[21] = 'Taux EBIT 2022'
    # Récupère les lignes de données correspondantes aux agences
    for i, column in enumerate(df_columns):
        df_return[column] = sheet_BTB.iloc[2:67, i + 1].values
    #
    # Récupère le BTC
    #
    df_btc = pd.DataFrame()
    sheet_BTC = excel_file.parse(sheet_names[1])
    # Récupère les noms des colonnes
    df_columns = sheet_BTC.iloc[2, 19:41].values
    # Récupère les années nécessaires sur certaines colonnes
    df_columns[18] = 'EBIT 2023'
    df_columns[19] = 'Taux EBIT 2023'
    df_columns[20] = 'EBIT 2022'
    df_columns[21] = 'Taux EBIT 2022'
    # Récupère les lignes de données correspondantes aux agences
    for i, column in enumerate(df_columns):
        df_btc[column] = sheet_BTC.iloc[3:36, i + 19].values
    #
    # Effectue la concaténation
    #
    df_return = pd.concat([df_return, df_btc], ignore_index=True)
    #
    # Nettoie le dataframe
    #
    df_return = df_return.dropna(subset=['Filtre Agence'])
    return df_return


def trouver_doublons(liste_mots):
    """
    Trouve les doublons dans une liste de mots et retourne un dictionnaire contenant les mots et tous les indices où
    ils apparaissent.

    :param liste_mots: La liste de mots dans laquelle chercher les doublons :return: Dictionnaire
    avec les mots comme clés et les indices où ils apparaissent comme valeurs
    """
    mots_vus = {}  # set vide pour stocker les mots déjà rencontrés
    for i, mot in enumerate(liste_mots):
        # On garde que les mots de type string (autre type = valeur manquante ou NaN)
        if type(mot) == float:
            continue
        # Vérifier si le mot a déjà été rencontré
        if mot in mots_vus:
            # Ajouter l'indice actuel du mot dans la liste des indices
            mots_vus[mot].append(i)
        else:
            # Si le mot n'a pas encore été rencontré, enregistrer son indice actuel dans le dictionnaire
            mots_vus[mot] = [i]
    return mots_vus

def test_colonne(fiche_path):
    # Récupère les feuilles excels
    if os.path.exists(fiche_path):
        # Get the file extension
        file_extension = os.path.splitext(fiche_path)[1]

    # Check if it's a CSV file
    if file_extension.lower() == ".csv":
        # It's a CSV file, so read it using read_csv()
        df_test = pd.read_csv(fiche_path)
        # Process the DataFrame as needed
    # Check if it's an Excel file
    elif file_extension.lower() in [".xls", ".xlsx"]:
        # It's an Excel file, so read it using read_excel()
        df_test = pd.read_excel(fiche_path)
        # Process the DataFrame as needed
    
    # Expected column names
    expected_columns = ["CA Contrats Collectif","ETP EFFECTIF Exploitation (Présence)","Nbre de véhicules Exploitation",
        "TOTAL AUTRES COUTS_1","TOTAL FRAIS GENERAUX_1","ETP Chef Agence","ETP Responsable Exploitation","ETP Secrétaire/Assitant(e) Agence",
        "ETP EFFECTIF Agence (Présence)","TOTAL VEHICULES_2","TOTAL AUTRES COUTS_2","TOTAL FRAIS GENERAUX_2",
        "Nombre de Tech. moyen par Chef Equipe","Nombre de Tech. moyen par Magasinier","Nombre de Techniciens par Secrétaire", '% / (CA+Prod.Centralisées)_1', '% / (CA+Prod.Centralisées)_2',
        '% / (CA+Prod.Centralisées)_3', '% / (CA+Prod.Centralisées)_4', '% / (CA+Prod.Centralisées)_5', '% / (CA+Prod.Centralisées)_6', '% / (CA+Prod.Centralisées)_7',
        '% / (CA+Prod.Centralisées)_8', '% / (CA+Prod.Centralisées)_9', '% / (CA+Prod.Centralisées)_10', '% / (CA+Prod.Centralisées)_11', '% / (CA+Prod.Centralisées)_12',
        '% / (CA+Prod.Centralisées)_13', '% / (CA+Prod.Centralisées)_14', '% / (CA+Prod.Centralisées)_15', '% / (CA+Prod.Centralisées)_16', '% Absences_1', '% Absences_2', 
        "MARGE BRUTE" ,"TOTAL CA + Prod Centralisées", "ACTIVITE", "Date", "Agence"] 

    
    # Check if all expected columns are present
    if set(expected_columns).issubset(df_test.columns):
        return True
    else:
        missing_columns = set(expected_columns) - set(df_test.columns)
        return f"Le fichier n'a pas les colonnes: {missing_columns}"
    
def import_fiche(fiche_path,
                 filtre_agence_loc=(7, 5),
                 row_loc=(slice(9, None), 5),
                 col_loc=(slice(7, 9), slice(7, None))):
    """
    Importe les données de fiches à partir d'un fichier Excel spécifié.

    Parameters:
    - fiche_path (str): Le chemin du fichier Excel contenant les données de fiches.
    - no_sheet_tab (list): Liste des noms de feuilles à exclure du traitement.
    - filtre_agence_loc (tuple, optional): Position (ligne, colonne) du filtre agence dans chaque feuille.
      Par défaut, positionné à (7, 5).
    - row_loc (tuple, optional): Position des lignes de données dans chaque feuille.
      Par défaut, positionné à (slice(9, None), 5).
    - col_loc (tuple, optional): Position des colonnes de données dans chaque feuille.
      Par défaut, positionné à (slice(7, 9), slice(7, None)).

    Returns:
    - pd.DataFrame: Un DataFrame contenant les données de fiches importées.

    Description :
    Cette fonction prend en entrée le chemin d'un fichier Excel contenant des données
    de fiches. Elle parcourt les feuilles du fichier Excel, extrait les informations
    nécessaires en fonction des paramètres spécifiés, et organise les données dans un
    DataFrame structuré.

    Exemple d'utilisation :
    ```
    fiche_data = import_fiche('/chemin/vers/le/fichier/fiche.xlsx', ['FeuilleA', 'FeuilleB'])
    ```

    Note : Assurez-vous que le fichier Excel spécifié contient les feuilles nécessaires
    avec la structure attendue pour le bon fonctionnement de cette fonction.
    """
    # Set le dataframe à retourner
    df_return = pd.DataFrame()
    # Récupère les feuilles excels
    if os.path.exists(fiche_path):
        # Get the file extension
        file_extension = os.path.splitext(fiche_path)[1]

    # Check if it's a CSV file
    if file_extension.lower() == ".csv":
        # It's a CSV file, so read it using read_csv()
        df_test = pd.read_csv(fiche_path)
        # Process the DataFrame as needed
    # Check if it's an Excel file
    elif file_extension.lower() in [".xls", ".xlsx"]:
        # It's an Excel file, so read it using read_excel()
        df_test = pd.read_excel(fiche_path)
        # Process the DataFrame as needed
    
    # Expected column names
    expected_columns = ["CA Contrats Collectif","ETP EFFECTIF Exploitation (Présence)","Nbre de véhicules Exploitation",
        "TOTAL AUTRES COUTS_1","TOTAL FRAIS GENERAUX_1","ETP Chef Agence","ETP Responsable Exploitation","ETP Secrétaire/Assitant(e) Agence",
        "ETP EFFECTIF Agence (Présence)","TOTAL VEHICULES_2","TOTAL AUTRES COUTS_2","TOTAL FRAIS GENERAUX_2",
        "Nombre de Tech. moyen par Chef Equipe","Nombre de Tech. moyen par Magasinier","Nombre de Techniciens par Secrétaire", '% / (CA+Prod.Centralisées)_1', '% / (CA+Prod.Centralisées)_2',
        '% / (CA+Prod.Centralisées)_3', '% / (CA+Prod.Centralisées)_4', '% / (CA+Prod.Centralisées)_5', '% / (CA+Prod.Centralisées)_6', '% / (CA+Prod.Centralisées)_7',
        '% / (CA+Prod.Centralisées)_8', '% / (CA+Prod.Centralisées)_9', '% / (CA+Prod.Centralisées)_10', '% / (CA+Prod.Centralisées)_11', '% / (CA+Prod.Centralisées)_12',
        '% / (CA+Prod.Centralisées)_13', '% / (CA+Prod.Centralisées)_14', '% / (CA+Prod.Centralisées)_15', '% / (CA+Prod.Centralisées)_16', '% Absences_1', '% Absences_2', 
        "MARGE BRUTE" ,"TOTAL CA + Prod Centralisées", "ACTIVITE", "Date", "Agence"] 
    
    # List of sheets to exclude
    no_sheet_tab = []
    correction_bug = ['A' + str(i) for i in range(150,700)] + ['C' + str(i).zfill(3) for i in range(1,100)]
    no_sheet_tab.extend(correction_bug)
    
    # Check if all expected columns are present
    if set(expected_columns).issubset(df_test.columns):
        excel_file = pd.ExcelFile(fiche_path)
        sheet_tab = excel_file.sheet_names
        for sheet in sheet_tab:
            # Sélectionne uniquement les feuilles qui ne contiennent pas
            # les mots à retirer de no_sheet_tab
            excel_name = sheet.upper()
            if not(sheet in no_sheet_tab):
                # Regarde si l'on peut directement trier les données dans BTB ou BTC           
                if ('COLL' in sheet or 'BTB' in sheet) and not ('IND' in sheet or 'BTC' in sheet):
                    Activite = 'BTB'
                elif not ('COLL' in sheet or 'BTB' in sheet) and ('IND' in sheet or 'BTC' in sheet):
                    Activite = 'BTC'
                elif ('COLL' in sheet or 'BTB' in sheet or 'IND' in sheet or 'BTC' in sheet):
                    Activite = 'BTB + BTC'
                else:
                    Activite = 'NON_IDENTIFIÉ'
                sheet = excel_file.parse(sheet)
                # Récupère le filtre agence
                filtre_agence = sheet.iloc[filtre_agence_loc[0], filtre_agence_loc[1]]
                # Récupère les données des lignes
                df_rows = sheet.iloc[row_loc[0], row_loc[1]]

                df_rows = df_rows.reset_index(drop=True)
                # Appel à la fonction pour trouver les doublons dans les futurs noms de colonne
                doublons = trouver_doublons(list(df_rows))
                # Renomme les colonnes en ajoutant un numéro pour les doublons
                for row in doublons:
                    if len(doublons[row]) > 1:
                        for i in range(0, len(doublons[row])):
                            df_rows[doublons[row][i]] = str(row) + '_' + str(i + 1)

                # Récupère les données des colonnes
                df_col = sheet.iloc[col_loc[0], col_loc[1]]
                #
                # Permet de créer une ligne en fonction de la date, et du type de l'info
                #
                for j, col in enumerate(df_col):
                    if df_col.iloc[0, j] in ['REEL', 'BUDGET', 'ACTU']:
                        new_row = {
                            'name_file': fiche_path,
                            'name_sheet': excel_name,
                            'Filtre Agence': filtre_agence,
                            'Date': sheet.iloc[col_loc[0].start + 1, j + col_loc[0].start],
                            'Type': sheet.iloc[col_loc[0].start, j + col_loc[0].start],
                            'ACTIVITE': Activite}
                        # print(df_rows.shape)
                        for i, row in enumerate(df_rows):
                            if (not pd.isna(row)) and (not pd.isna(sheet.iloc[i + row_loc[0].start, j + col_loc[0].start])):
                                new_row[row] = sheet.iloc[i + row_loc[0].start, j + col_loc[0].start]
                        #
                        # Effectue la concaténation
                        #
                        df_return = pd.concat([df_return, pd.DataFrame([new_row])], ignore_index=True)
        return df_return
    else:
        missing_columns = set(expected_columns) - set(df_test.columns)
        return f"Le fichier n'a pas les colonnes: {missing_columns}"


#fiche_data = import_fiche('Data/Fiches/Reporting_SOATL 12_2023_Occitanie.xlsb', ['Bezier BTB'])


# for i in fiche_data.columns:
# print(i)

def import_all_fiches(fiches_path, no_sheet_tab, silence=True):
    """
    """
    # Set le dataframe à retourner
    df_return = pd.DataFrame()
    # Récupère toutes les fiches dans le dossier
    all_fiches = glob.glob(f'{fiches_path}/*.xlsx')
    xlsb_fiches = glob.glob(f'{fiches_path}/*.xlsb')
    all_fiches.extend(xlsb_fiches)
    # Boucle pour chaque fiches : 
    for i, fiche in enumerate(all_fiches):
        if not silence:
            print(fiche)
        df_fiche = import_fiche(fiche, no_sheet_tab)
        df_fiche.to_excel(f'Data/Output/test/{i}.xlsx', index=False)

        df_return = pd.concat([df_fiche, df_return], ignore_index=True)
    return df_return

def select_agences(df, glob_df):
    """
    Permet de sélectionner les agences d'un DataFrame en fonction des agences disponibles dans un DataFrame global.

    Args:
        df (DataFrame): Le DataFrame contenant les données des agences.
        glob_df (DataFrame): Le DataFrame global contenant les références des agences disponibles.

    Returns:
        DataFrame: Le DataFrame filtré contenant uniquement les lignes des agences disponibles dans le DataFrame global.
    """
    agence_dispo_ref = glob_df['Filtre Agence'].unique()
    agence_dispo_df = df['Filtre Agence'].unique()
    agence_non_dispo = [agence for agence in agence_dispo_df if agence not in agence_dispo_ref]
    df_a_filtrer = df[df['Filtre Agence'].isin(agence_non_dispo)]
    df_clean = df.drop(df_a_filtrer.index)
    df_clean = df_clean.drop(['name_file', 'name_sheet'], axis=1)
    nb_col_a_conserver = len(df_clean.columns) - 71
    # Supprimer les 71 dernières colonnes
    df_clean = df_clean.iloc[:, :nb_col_a_conserver]

    # Suppression des lignes de budgets
    df_clean = df_clean[df_clean['Type'].isin(['REEL', 'ACTU'])]

    # Ajouter les colonnes 'Agence' et 'Region' de glob_df dans df_clean
    df_clean = df_clean.merge(glob_df[['Filtre Agence', 'AGENCE', 'REGION']], on='Filtre Agence', how='left')

    return df_clean


def main():
    df = import_fiche('Fiches/test_import_fiche.xlsx')
    glob_df = import_ref("Fiches/Benchmark Classement Agences REEL 2022 et REEL 2023.xlsx")
    final_df = select_agences(df, glob_df)
    print(final_df.shape)
    test_colonne('Fiches/test_import_fiche.xlsx')
if __name__ == '__main__':
    main()