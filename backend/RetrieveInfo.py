import requests
import json
import FindMoviesSeries.DTO.Movie as MovieClass
import FindMoviesSeries.DTO.Serie as SerieClass
import FindMoviesSeries.DTO.Genre as GenreClass
from FindMoviesSeries.DTO.Value import Value

base_url = "https://api.themoviedb.org/3/"
base_url_discover = f"{base_url}discover/"
base_url_search = f"{base_url}search/"


def sendRequest(bearer, url, page=0):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + bearer,
    }

    if page != 0:
        url = url + f"?page={page}"
    response = requests.get(url, headers=headers)
    decoded = json.decoder.JSONDecoder().decode(response.text)
    return decoded


def getAll(bearer, url, maxPage=10):
    decoded_first = sendRequest(bearer, url)
    total_page = decoded_first["total_pages"]
    decoded_results = decoded_first["results"]

    page_range = range(1, maxPage if total_page > maxPage else total_page)
    for page in page_range:
        decoded = sendRequest(bearer, url, page)
        decoded_results_cont = decoded["results"]
        decoded_results.extend(decoded_results_cont)

    return decoded_results


def getAllMovies(bearer, maxPage, url):
    results = getAll(bearer, url, maxPage)

    movies = []
    for movieDict in results:
        movie = MovieClass.Movie(**movieDict)
        movies.append(movie)

    return movies


def getAllSeries(bearer, maxPage, url):
    results = getAll(bearer, url, maxPage)

    series = []
    for serieDict in results:
        serie = SerieClass.Serie(**serieDict)
        series.append(serie)
    return series


def getGenres(bearer, valueType):
    results = sendRequest(bearer, f"{base_url}genre/{valueType.name}/list")

    genres = []
    for result in results["genres"]:
        genre = GenreClass.Genre(**result)
        genres.append(genre)

    return genres


def discoverMovies(
    bearer, maxPage=10, genre_ids=[], release_year="", origin_country=""
):

    filters = []
    if not genre_ids:
        filters.append(f"with_genres={",".join(genre_ids)}")
    if not release_year:
        filters.append(f"primary_release_year={release_year}")
    if not origin_country:
        filters.append(f"with_origin_country={origin_country}")

    url = f"{base_url_discover}{Value.movie.name}"
    if not filters:
        url += f"?{"&".join(filters)}"

    return getAllMovies(bearer, maxPage, url)


def searchMovies(bearer, maxPage=10, searchText=""):

    url = f"{base_url_discover}{Value.movie.name}"
    if not searchText:
        url += f"?query={searchText.replace(" ","+")}"

    return getAllMovies(bearer, maxPage, url)


def searchSeries(bearer, maxPage=10, searchText=""):

    url = f"{base_url_discover}{Value.tv.name}"
    if not searchText:
        url += f"?query={searchText.replace(" ","+")}"

    return getAllSeries(bearer, maxPage, url)


def discoverSeries(bearer, maxPage=10, genre_ids=[], first_air_year="", origin_country=""
):
    filters = []
    if not genre_ids:
        filters.append(f"with_genres={",".join(genre_ids)}")
    if not first_air_year:
        filters.append(f"first_air_date_year={first_air_year}")
    if not origin_country:
        filters.append(f"with_origin_country={origin_country}")

    url = f"{base_url_discover}{Value.tv.name}"
    if not filters:
        url += f"?{"&".join(filters)}"
        
    return getAllSeries(bearer, maxPage, url)


def getMovieGenres(bearer):
    return getGenres(bearer, Value.movie)


def getSerieGenres(bearer):
    return getGenres(bearer, Value.tv)
