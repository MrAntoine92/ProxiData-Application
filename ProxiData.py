import tkinter as tk
from proxidata_app import ProxiDataApp


if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    root.iconbitmap('Images/icone_proxiserve.ico')
    app = ProxiDataApp(root)
    root.mainloop()
