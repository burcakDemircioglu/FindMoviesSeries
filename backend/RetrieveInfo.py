import requests

def retrieveMovies(bearer):    
    # url = "https://api.themoviedb.org/3/authentication"
    url = "https://api.themoviedb.org/3/discover/movie"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + bearer,
    }

    response = requests.get(url, headers=headers)

    print(response.text)

    f = open("result.json", "a", encoding="utf-8")
    f.write(response.text)
    f.close()

    return response.text