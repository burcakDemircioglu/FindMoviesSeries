import customtkinter
from CTkListbox import *

from FindMoviesSeries.backend import RetrieveInfo
from FindMoviesSeries.ui.DetailFrame import DetailFrame

class MainFrame(customtkinter.CTk):
    def discoverMoviesButtonClick(self):
        movies = RetrieveInfo.discoverMovies(self.secrets["API_BEARER"])

        self.valueDict = {}
        i = 0
        for movie in movies:
            self.valueDict[movie.title] = movie
            self.listbox.insert(i, movie.title)
            i += 1

    def selectListValue(self, selected_option):
        selectedValue = self.valueDict[selected_option]
        self.details_frame.setDetails(selectedValue)

    def __init__(self, secrets):
        super().__init__()
        self.secrets = secrets

        customtkinter.set_appearance_mode("dark")
        self.title("FindMoviesSeries")
        self.geometry(f"1500x800")

        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure((0), weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(
            master=self, width=50, corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.discoverButton = customtkinter.CTkButton(
            master=self.sidebar_frame,
            text="Discover movies",
            command=self.discoverMoviesButtonClick,
        )
        self.discoverButton.pack(pady=20, padx=20)

        self.results_list_frame = customtkinter.CTkFrame(
            master=self, width=100, corner_radius=0
        )
        self.results_list_frame.grid(row=0, column=1, sticky="nsew")
        self.results_list_frame.grid_rowconfigure(4, weight=1)

        self.listbox = CTkListbox(self.results_list_frame, command=self.selectListValue)
        self.listbox.pack(pady=0, padx=0, fill="both", expand=True)

        self.details_frame = DetailFrame(self)
        self.details_frame.grid(row=0, column=2, pady=0, padx=0, sticky="nsew")
