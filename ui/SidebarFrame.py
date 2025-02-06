import customtkinter
import tkinter as tk


from FindMoviesSeries.DTO.MediaType import MediaType


class SidebarFrame(customtkinter.CTkFrame):
    def __init__(self, master, infoRetriever):
        super().__init__(master, width=80, corner_radius=0)

        self.infoRetriever = infoRetriever
        self.mainFrame = master
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        defaultMediaType = MediaType.movie
        self.setMediaType(defaultMediaType.name)
        self.mediaTypeOption = customtkinter.CTkOptionMenu(
            master=self,
            values=[e.name for e in MediaType],
            command=self.setMediaType,
        )
        self.mediaTypeOption.pack(pady=20, padx=10)
        self.mediaTypeOption.set(defaultMediaType.name)

        self.SearchTextBox = customtkinter.CTkEntry(
            self, placeholder_text="Search..", corner_radius=5
        )
        self.SearchTextBox.pack(pady=0, padx=0)

        self.searchButton = customtkinter.CTkButton(
            master=self,
            text="Search",
            command=self.searchButtonClick,
        )
        self.searchButton.pack(pady=20, padx=20)

        genreNames = [genre.name for genre in self.genres]
        genreMenu = tk.Menubutton(
            self, text="Select Genre", indicatoron=True, borderwidth=1
        )
        genreChoiceMenu = tk.Menu(genreMenu, tearoff=False)
        genreMenu.configure(menu=genreChoiceMenu)
        genreMenu.pack(padx=0, pady=0)

        self.genreChoices = {}
        for choice in genreNames:
            self.genreChoices[choice] = tk.IntVar(value=0)
            genreChoiceMenu.add_checkbutton(
                label=choice,
                variable=self.genreChoices[choice],
                onvalue=1,
                offvalue=0,
                command=self.setGenre,
            )

        self.discoverButton = customtkinter.CTkButton(
            master=self,
            text="Discover",
            command=self.discoverButtonClick,
        )
        self.discoverButton.pack(pady=20, padx=20)

    def searchButtonClick(self):
        if self.mediaType == MediaType.movie:
            movies = self.infoRetriever.searchMovies(
                searchText=self.SearchTextBox.get()
            )
            self.mainFrame.resetValuesWithMovies(movies)

        if self.mediaType == MediaType.tv:
            series = self.infoRetriever.discoverSeries(
                searchText=self.SearchTextBox.get()
            )
            self.mainFrame.resetValuesWithSeries(series)

    def discoverButtonClick(self):
        if self.mediaType == MediaType.movie:
            movies = self.infoRetriever.discoverMovies(genre_ids=self.selectedGenreIds)
            self.mainFrame.resetValuesWithMovies(movies)

        if self.mediaType == MediaType.tv:
            series = self.infoRetriever.discoverSeries(genre_ids=self.selectedGenreIds)
            self.mainFrame.resetValuesWithSeries(series)

    def setGenre(self):
        self.selectedGenreNames = [
            name for (name, var) in self.genreChoices.items() if var.get() == 1
        ]

        self.selectedGenreIds = [
            genre.id for genre in self.genres if genre.name in self.selectedGenreNames
        ]

    def setMediaType(self, choice):
        self.mediaType = MediaType[choice]
        self.genres = self.infoRetriever.getGenres(MediaType.movie)
