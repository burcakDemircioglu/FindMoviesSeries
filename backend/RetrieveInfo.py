import requests
import json
import FindMoviesSeries.DTO.Movie as MovieClass
import FindMoviesSeries.DTO.Serie as SerieClass


def discoverMovies(bearer):
    url = "https://api.themoviedb.org/3/discover/movie"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + bearer,
    }

    response = requests.get(url, headers=headers)
    decoded = json.decoder.JSONDecoder().decode(response.text)["results"]

    movies = []
    for movieDict in decoded:
        movie = MovieClass.Movie(**movieDict)
        movies.append(movie)

    return movies


def discoverSeries(bearer):
    url = "https://api.themoviedb.org/3/discover/tv"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + bearer,
    }

    response = requests.get(url, headers=headers)

    decoded = json.decoder.JSONDecoder().decode(response.text)["results"]

    series = []
    for serieDict in decoded:
        serie = SerieClass.Serie(**serieDict)
        series.append(serie)

    return series