import requests
import json
import FindMoviesSeries.DTO.Movie as MovieClass
import FindMoviesSeries.DTO.Serie as SerieClass
import FindMoviesSeries.DTO.Genre as GenreClass
from FindMoviesSeries.DTO.MediaType import MediaType

base_url = "https://api.themoviedb.org/3/"
base_url_discover = f"{base_url}discover/"
base_url_search = f"{base_url}search/"

class InfoRetriever():
    def __init__(self, secrets):
        self.bearer=secrets["API_BEARER"]

    def sendRequest(self, url, page=0):
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + self.bearer,
        }

        if page != 0:
            url = url + f"?page={page}"
        response = requests.get(url, headers=headers)
        return json.decoder.JSONDecoder().decode(response.text)


    def getAll(self, url, maxPage=10):
        print(url)

        decoded_first = self.sendRequest(url)
        total_page = decoded_first["total_pages"]
        decoded_results = decoded_first["results"]

        page_range = range(1, maxPage if total_page > maxPage else total_page)
        for page in page_range:
            decoded = self.sendRequest(url, page)
            decoded_results_cont = decoded["results"]
            decoded_results.extend(decoded_results_cont)

        return decoded_results


    def getAllMovies(self, maxPage, url):
        results = self.getAll(url, maxPage)

        movies = []
        for movieDict in results:
            movie = MovieClass.Movie(**movieDict)
            movies.append(movie)

        return movies


    def getAllSeries(self, maxPage, url):
        results = self.getAll(url, maxPage)

        series = []
        for serieDict in results:
            serie = SerieClass.Serie(**serieDict)
            series.append(serie)
        return series


    def getGenres(self, valueType):
        results = self.sendRequest(f"{base_url}genre/{valueType.name}/list")

        genres = []
        for result in results["genres"]:
            genre = GenreClass.Genre(**result)
            genres.append(genre)

        return genres


    def discoverMovies(
        self, maxPage=10, genre_ids=[], release_year="", origin_country=""
    ):

        filters = []

        if genre_ids:
            filters.append(f"with_genres={",".join(str(id) for id in genre_ids)}")
        if release_year:
            filters.append(f"primary_release_year={release_year}")
        if origin_country:
            filters.append(f"with_origin_country={origin_country}")

        url = f"{base_url_discover}{MediaType.movie.name}"

        if filters:
            url += f"?{"&".join(filters)}"

        return self.getAllMovies(maxPage, url)


    def searchMovies(self, maxPage=10, searchText=""):


        url = f"{base_url_search}{MediaType.movie.name}"
        if searchText:
            url += f"?query={searchText.replace(" ","+")}"

        return self.getAllMovies(maxPage, url)


    def searchSeries(self, maxPage=10, searchText=""):

        url = f"{base_url_search}{MediaType.tv.name}"
        if searchText:
            url += f"?query={searchText.replace(" ","+")}"

        return self.getAllSeries(maxPage, url)


    def discoverSeries(self, maxPage=10, genre_ids=[], first_air_year="", origin_country=""
    ):
        filters = []
        if genre_ids:
            filters.append(f"with_genres={",".join(str(id) for id in genre_ids)}")
        if first_air_year:
            filters.append(f"first_air_date_year={first_air_year}")
        if origin_country:
            filters.append(f"with_origin_country={origin_country}")

        url = f"{base_url_discover}{MediaType.tv.name}"
        if filters:
            url += f"?{"&".join(filters)}"
            
        return self.getAllSeries(maxPage, url)
