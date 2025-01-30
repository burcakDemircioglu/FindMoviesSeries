import requests
import json
import FindMoviesSeries.DTO.Movie as MovieClass
import FindMoviesSeries.DTO.Serie as SerieClass


def sendRequest(bearer, url):

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + bearer,
    }

    response = requests.get(url, headers=headers)
    decoded = json.decoder.JSONDecoder().decode(response.text)
    print(decoded["total_pages"])
    print(decoded["total_results"])
    decoded_results = decoded["results"]

    return decoded_results


def discoverMovies(bearer):
    results = sendRequest(bearer, "https://api.themoviedb.org/3/discover/movie")

    movies = []
    for movieDict in results:
        movie = MovieClass.Movie(**movieDict)
        movies.append(movie)

    return movies


def discoverSeries(bearer):
    results = sendRequest(bearer, "https://api.themoviedb.org/3/discover/tv")

    series = []
    for serieDict in results:
        serie = SerieClass.Serie(**serieDict)
        series.append(serie)

    return series
