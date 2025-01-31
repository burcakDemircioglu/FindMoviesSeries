from FindMoviesSeries.DTO.Value import Value
import customtkinter
import tkinter as tk
from CTkListbox import *

from FindMoviesSeries.backend import RetrieveInfo
from FindMoviesSeries.ui.DetailFrame import DetailFrame


class MainFrame(customtkinter.CTk):
    def getDefaultList(self):
        movies = RetrieveInfo.discoverMovies(self.bearer, 2)

        self.value = Value.movie
        self.valueDict = {}
        i = 0
        for movie in movies:
            self.valueDict[movie.title] = movie
            self.listbox.insert(i, movie.title)
            i += 1

    def discoverMoviesButtonClick(self):
        movies = RetrieveInfo.discoverMovies(self.bearer)

        self.value = Value.movie
        self.valueDict = {}
        i = 0
        for movie in movies:
            self.valueDict[movie.title] = movie
            self.listbox.insert(i, movie.title)
            i += 1

    def discoverSeriesButtonClick(self):
        series = RetrieveInfo.discoverSeries(self.bearer)

        self.value = Value.tv
        self.valueDict = {}
        i = 0
        for serie in series:
            self.valueDict[serie.name] = serie
            self.listbox.insert(i, serie.name)
            i += 1

    def selectListValue(self, selected_option):
        selectedValue = self.valueDict[selected_option]

        if self.value == Value.movie:
            self.details_frame.setMovieDetails(self.genres, selectedValue)
        if self.value == Value.tv:
            self.details_frame.setSerieDetails(self.genres, selectedValue)

    def __init__(self, secrets):
        super().__init__()
        self.bearer = secrets["API_BEARER"]

        self.genres = RetrieveInfo.getMovieGenres(self.bearer)

        customtkinter.set_appearance_mode("dark")
        self.title("FindMoviesSeries")
        self.geometry(f"1500x800")

        self.grid_columnconfigure((2), weight=2, minsize=500)
        self.grid_columnconfigure((0), weight=0, minsize=80)
        self.grid_columnconfigure((1), weight=1, minsize=80)
        self.grid_rowconfigure(0, weight=1)

        self.createSidebar()

        self.results_list_frame = customtkinter.CTkFrame(
            master=self, width=100, corner_radius=0
        )
        self.results_list_frame.grid(row=0, column=1, sticky="nsew")
        self.results_list_frame.grid_rowconfigure(4, weight=1)

        self.listbox = CTkListbox(self.results_list_frame, command=self.selectListValue)
        self.listbox.pack(pady=0, padx=0, fill="both", expand=True)
        self.getDefaultList()

        self.details_frame = DetailFrame(self)
        self.details_frame.grid(row=0, column=2, pady=0, padx=0, sticky="nsew")
        self.details_frame.setMovieDetails(
            self.genres, self.valueDict[list(self.valueDict.keys())[0]]
        )

    def createSidebar(self):

        self.sidebar_frame = customtkinter.CTkFrame(
            master=self, width=80, corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        genreNames = [genre.name for genre in self.genres]
        combobox_var = customtkinter.StringVar(value="Select/Type Genre")
        self.genreComboBox = customtkinter.CTkComboBox(
            self.sidebar_frame, values=genreNames, variable=combobox_var
        )
        self.genreComboBox.pack(pady=20, padx=10)

        self.discoverMoviesButton = customtkinter.CTkButton(
            master=self.sidebar_frame,
            text="Discover movies",
            command=self.discoverMoviesButtonClick,
        )
        self.discoverMoviesButton.pack(pady=20, padx=20)

        self.discoverSeriesButton = customtkinter.CTkButton(
            master=self.sidebar_frame,
            text="Discover series",
            command=self.discoverSeriesButtonClick,
        )
        self.discoverSeriesButton.pack(pady=20, padx=20)
