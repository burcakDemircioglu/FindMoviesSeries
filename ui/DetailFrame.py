import urllib.request
import io
from PIL import ImageTk, Image
import customtkinter

class DetailFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=500)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.title_label = customtkinter.CTkLabel(master=self, wraplength=500, justify="left", text="")
        self.title_label.grid(row=0, column=0, pady=0, padx=0)

        self.poster = customtkinter.CTkLabel(master=self, width=200, height=200, justify="left", text="")
        self.poster.grid(row=0, column=1, pady=0, padx=0)

        self.overview_label = customtkinter.CTkLabel(master=self, wraplength=500, justify="left", text="")
        self.overview_label.grid(row=1, pady=0, padx=0)

    def setDetails(self, movie):
        self.title_label.configure(text=movie.title)
        self.overview_label.configure(text=movie.overview)

        posterUrl=f"https://image.tmdb.org/t/p/original{movie.poster_path}"
        with urllib.request.urlopen(posterUrl) as u:
            raw_data = u.read()

        img=Image.open(io.BytesIO(raw_data))
        img.thumbnail((300,300), Image.LANCZOS)
        photoImage = ImageTk.PhotoImage(img)
        self.poster.configure(image=photoImage)