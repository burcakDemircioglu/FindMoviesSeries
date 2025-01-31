import urllib.request
import io
from PIL import ImageTk, Image
import customtkinter


class DetailFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=500)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.detailsFrame = customtkinter.CTkFrame(master=self)
        self.detailsFrame.grid(row=0, column=0, pady=0, padx=0)
        self.overviewFrame = customtkinter.CTkFrame(master=self)
        self.overviewFrame.grid(row=1, pady=0, padx=0)
        self.title_label = customtkinter.CTkLabel(
            master=self.detailsFrame,
            width=250,
            wraplength=500,
            justify="left",
            text="",
            font=("Helvetica", 30),
            # bg_color="red",
        )
        self.title_label.pack(pady=10, padx=10)

        self.details_label = customtkinter.CTkLabel(
            master=self.detailsFrame,
            width=250,
            wraplength=500,
            justify="left",
            text="",
            font=("Helvetica", 20),
            # bg_color="green",
        )
        self.details_label.pack(pady=10, padx=10)

        self.poster = customtkinter.CTkLabel(
            master=self, width=250, height=200, justify="left", text=""
        )
        self.poster.grid(row=0, column=1, pady=0, padx=0)

        self.overview_label = customtkinter.CTkLabel(
            master=self.overviewFrame, wraplength=500, justify="left", text=""
        )
        self.overview_label.pack(pady=20, padx=10)

    def setMovieDetails(self, genres, movie):

        detailsLabelText = f"""
        Original title: {movie.original_title}        
        Release date: {movie.release_date}
        Vote: {movie.vote_average} ({movie.vote_count})
        Original Language: {movie.original_language}
        Popularity: {movie.popularity}
        Genres: {self.getGenreNames(genres, movie)}
        """

        self.title_label.configure(text=movie.title)
        self.details_label.configure(text=detailsLabelText)
        self.overview_label.configure(text=movie.overview)

        posterUrl = f"https://image.tmdb.org/t/p/original{movie.poster_path}"
        self.setPoster(posterUrl)

    def setSerieDetails(self, genres, serie):

        detailsLabelText = f"""
        Original title: {serie.original_name}        
        First air date: {serie.first_air_date}
        Vote: {serie.vote_average} ({serie.vote_count})
        Original Language: {serie.original_language}
        Popularity: {serie.popularity}
        Genres: {self.getGenreNames(genres, serie)}
        """

        self.title_label.configure(text=serie.name)
        self.details_label.configure(text=detailsLabelText)
        self.overview_label.configure(text=serie.overview)

        posterUrl = f"https://image.tmdb.org/t/p/original{serie.poster_path}"
        self.setPoster(posterUrl)

    def setPoster(self, posterUrl):
        with urllib.request.urlopen(posterUrl) as u:
            raw_data = u.read()

        img = Image.open(io.BytesIO(raw_data))
        img.thumbnail((500, 500), Image.LANCZOS)
        photoImage = ImageTk.PhotoImage(img)
        self.poster.configure(image=photoImage)

    def getGenreNames(self, genres, value):
        genres = [genre.name for genre in genres if genre.id in value.genre_ids]

        return ", ".join(genres)
