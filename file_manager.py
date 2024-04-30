# file_manager.py
class FileManager:
    filename = None  # Initialisation de la variable de nom de fichier

    @staticmethod
    def set_filename(filename):
        FileManager.filename = filename

    @staticmethod
    def get_filename():
        return FileManager.filename