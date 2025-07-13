import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys

class SpotifyDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de Música de Spotify")
        self.root.geometry("600x380")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        self.url_var = ctk.StringVar()
        self.download_path = ctk.StringVar(value=os.path.expanduser("~") + "/Music")

        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self.root, text="Descargador de Música de Spotify",
                                   font=ctk.CTkFont(size=20, weight="bold"),
                                   text_color="white")
        title_label.pack(pady=20)

        url_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        url_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(url_frame, text="URL de la Canción/Playlist:", text_color="white").pack(side="left", padx=(0, 10))
        url_entry = ctk.CTkEntry(url_frame, textvariable=self.url_var, width=400,
                                 fg_color="#333333", text_color="white", border_color="#1DB954")
        url_entry.pack(side="left", expand=True, fill="x")

        path_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        path_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(path_frame, text="Guardar en:", text_color="white").pack(side="left", padx=(0, 10))
        path_entry = ctk.CTkEntry(path_frame, textvariable=self.download_path, state="readonly", width=350,
                                  fg_color="#333333", text_color="white", border_color="#1DB954")
        path_entry.pack(side="left", expand=True, fill="x")
        browse_button = ctk.CTkButton(path_frame, text="Explorar", command=self.browse_path,
                                      fg_color="#1DB954", hover_color ="#1ED760", text_color="white")
        browse_button.pack(side="left", padx=(10, 0))

        download_button = ctk.CTkButton(self.root, text="Descargar", command=self.start_download,
                                        font=ctk.CTkFont(size=16, weight="bold"), height=40,
                                        fg_color="#1DB954", hover_color ="#1ED760", text_color="white")
        download_button.pack(pady=20)

        self.status_label = ctk.CTkLabel(self.root, text="", text_color="#1DB954",
                                         font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=5)

    def browse_path(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path.set(folder_selected)

    def start_download(self):
        url = self.url_var.get().strip()
        path = self.download_path.get().strip()

        if not url:
            messagebox.showerror("Error", "Introduce una URL de Spotify.")
            return
        if not path:
            messagebox.showerror("Error", "Selecciona una ruta de descarga.")
            return
        
        self.status_label.configure(text="Iniciando descarga...", text_color="orange")
        self.root.update_idletasks()

        cmd = [sys.executable, "-m", "spotdl", "download", url, "--output", path]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                self.status_label.configure(text="Descarga completada 🎉", text_color="#1DB954")
                messagebox.showinfo("Éxito", f"Descarga completada en:\n{path}")
            else:
                self.status_label.configure(text="Error en descarga", text_color="red")
                messagebox.showerror("Error", f"No se pudo descargar:\n{result.stderr}")

        except Exception as e:
            self.status_label.configure(text="Error inesperado", text_color="red")
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")



if __name__ == "__main__":
    root = ctk.CTk()
    app = SpotifyDownloaderApp(root)
    root.mainloop()

