import requests
import json
import FindMoviesSeries.DTO.Movie as MovieClass
import FindMoviesSeries.DTO.Serie as SerieClass


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


def discoverMovies(bearer):
    results = getAll(bearer, "https://api.themoviedb.org/3/discover/movie")

    movies = []
    for movieDict in results:
        movie = MovieClass.Movie(**movieDict)
        movies.append(movie)

    return movies


def discoverSeries(bearer):
    results = getAll(bearer, "https://api.themoviedb.org/3/discover/tv")

    series = []
    for serieDict in results:
        serie = SerieClass.Serie(**serieDict)
        series.append(serie)

    return series
