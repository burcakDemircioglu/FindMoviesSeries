from FindMoviesSeries.DTO.MediaType import MediaType
import customtkinter
import tkinter as tk
from CTkListbox import *

from FindMoviesSeries.ui.DetailFrame import DetailFrame
from FindMoviesSeries.ui.SidebarFrame import SidebarFrame


class MainFrame(customtkinter.CTk):
    def setDefaultMediaList(self):
        movies = self.infoRetriever.discoverMovies(2)

        self.mediaType = MediaType.movie
        self.resetValuesWithMovies(movies)

    def selectListValue(self, selected_option):
        selectedValue = self.valueDict[selected_option]

        if self.mediaType == MediaType.movie:
            self.details_frame.setMovieDetails(self.genres, selectedValue)
        if self.mediaType == MediaType.tv:
            self.details_frame.setSerieDetails(self.genres, selectedValue)

    def resetValuesWithSeries(self, values):
        self.valueDict = {}

        for value in values:
            self.valueDict[value.name] = value

        valueNameList = [serie.title for serie in values]
        self.resetListBox(valueNameList)

    def resetValuesWithMovies(self, values):
        self.valueDict = {}

        for value in values:
            self.valueDict[value.title] = value
        
        valueNameList = [movie.title for movie in values]
        self.resetListBox(valueNameList)

    def resetListBox(self, values):
        self.listbox.delete(0, customtkinter.END)

        i = 0
        for value in values:
            self.listbox.insert(i, value)
            i += 1

    def __init__(self, infoRetriever):
        super().__init__()
        self.infoRetriever = infoRetriever

        self.genres = self.infoRetriever.getGenres(MediaType.movie)
        self.selectedGenreIds = []

        customtkinter.set_appearance_mode("dark")
        self.title("FindMoviesSeries")
        self.geometry(f"1500x800")

        self.grid_columnconfigure((2), weight=2, minsize=500)
        self.grid_columnconfigure((0), weight=0, minsize=80)
        self.grid_columnconfigure((1), weight=1, minsize=80)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = SidebarFrame(self, self.infoRetriever)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.results_list_frame = customtkinter.CTkFrame(
            master=self, width=100, corner_radius=0
        )
        self.results_list_frame.grid(row=0, column=1, sticky="nsew")
        self.results_list_frame.grid_rowconfigure(4, weight=1)

        self.listbox = CTkListbox(self.results_list_frame, command=self.selectListValue)
        self.listbox.pack(pady=0, padx=0, fill="both", expand=True)
        self.setDefaultMediaList()

        self.details_frame = DetailFrame(self)
        self.details_frame.grid(row=0, column=2, pady=0, padx=0, sticky="nsew")
        self.details_frame.setMovieDetails(
            self.genres, self.valueDict[list(self.valueDict.keys())[0]]
        )
