from cx_Freeze import setup, Executable
import os

base = None
executables = [Executable("ProxiData.py", base=base, icon="Images/icone_proxiserve.ico")]
packages = ["sklearn", "pandas", "numpy", "tkinter", "customtkinter",
            "matplotlib", "joblib", "plotly", "Pmw"]

# Récupérer tous les dossiers et fichiers de v8
v8_files = []
for dirpath, dirnames, filenames in os.walk('v8'):
    for filename in filenames:
        v8_files.append((os.path.join(dirpath, filename), os.path.join(dirpath, filename)))

# Récupérer tous les dossiers et fichiers de Images
image_files = []
for dirpath, dirnames, filenames in os.walk('Images'):
    for filename in filenames:
        image_files.append((os.path.join(dirpath, filename), os.path.join(dirpath, filename)))

# Récupérer tous les dossiers et fichiers de Fiches
fiches_files = []
for dirpath, dirnames, filenames in os.walk('Fiches'):
    for filename in filenames:
        fiches_files.append((os.path.join(dirpath, filename), os.path.join(dirpath, filename)))

# Récupérer tous les dossiers et fichiers de Fiches
modele_files = []
for dirpath, dirnames, filenames in os.walk('Modele'):
    for filename in filenames:
        modele_files.append((os.path.join(dirpath, filename), os.path.join(dirpath, filename)))

options = {
    'build_exe': {
        'build_exe': 'ProxiData',
        'packages': packages,
        'include_files': v8_files + image_files + fiches_files + modele_files,  # Ajouter les fichiers de v8 ici
    },
}

setup(
    name="ProxiData.exe",
    options=options,
    version="1.0",
    description='Première version de ProxiData',
    executables=executables
)
