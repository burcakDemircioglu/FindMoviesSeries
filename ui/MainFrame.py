from FindMoviesSeries.DTO.MediaType import MediaType
import customtkinter
import tkinter as tk
from CTkListbox import *

from FindMoviesSeries.ui.DetailFrame import DetailFrame


class MainFrame(customtkinter.CTk):
    def getDefaultList(self):
        movies = self.infoRetriever.discoverMovies(2)

        self.mediaType = MediaType.movie
        self.valueDict = {}
        i = 0
        for movie in movies:
            self.valueDict[movie.title] = movie
            self.listbox.insert(i, movie.title)
            i += 1

    def discoverButtonClick(self):
        media = []
        self.valueDict = {}
        i = 0

        if self.mediaType == MediaType.movie:
            media = self.infoRetriever.discoverMovies(genre_ids=self.selectedGenreIds)
            for m in media:
                self.valueDict[m.title] = m
                self.listbox.insert(i, m.title)
                i += 1
        if self.mediaType == MediaType.tv:
            media = self.infoRetriever.discoverSeries(genre_ids=self.selectedGenreIds)
            for m in media:
                self.valueDict[m.name] = m
                self.listbox.insert(i, m.name)
                i += 1

    def selectListValue(self, selected_option):
        selectedValue = self.valueDict[selected_option]

        if self.mediaType == MediaType.movie:
            self.details_frame.setMovieDetails(self.genres, selectedValue)
        if self.mediaType == MediaType.tv:
            self.details_frame.setSerieDetails(self.genres, selectedValue)

    def __init__(self, infoRetriever):
        super().__init__()
        self.infoRetriever = infoRetriever

        self.genres = self.infoRetriever.getGenres(MediaType.movie)

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

    def setMediaType(self, choice):
        self.mediaType = MediaType[choice]
        self.genres = self.infoRetriever.getGenres(MediaType.movie)

    def setGenre(self, choice):
        self.selectedGenreIds = [
            genre.id for genre in self.genres if genre.name == choice
        ]

    def createSidebar(self):
        self.sidebar_frame = customtkinter.CTkFrame(
            master=self, width=80, corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.mediaTypeOption = customtkinter.CTkOptionMenu(
            master=self.sidebar_frame,
            values=[e.name for e in MediaType],
            command=self.setMediaType,
        )
        self.mediaTypeOption.pack(pady=20, padx=10)
        self.mediaTypeOption.set(MediaType.movie.name)

        genreNames = [genre.name for genre in self.genres]
        combobox_var = customtkinter.StringVar(value="Select/Type Genre")
        self.genreComboBox = customtkinter.CTkComboBox(
            self.sidebar_frame,
            values=genreNames,
            variable=combobox_var,
            command=self.setGenre,
        )
        self.genreComboBox.pack(pady=20, padx=10)

        self.discoverButton = customtkinter.CTkButton(
            master=self.sidebar_frame,
            text="Discover",
            command=self.discoverButtonClick,
        )
        self.discoverButton.pack(pady=20, padx=20)
