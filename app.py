import requests
from dotenv import dotenv_values


secrets = dotenv_values(".env")

def main():
    # url = "https://api.themoviedb.org/3/authentication"
    url = "https://api.themoviedb.org/3/discover/movie"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer "+secrets["API_BEARER"]
    }

    response = requests.get(url, headers=headers)

    print(response.text)

    f = open("result.json", "a", encoding="utf-8")
    f.write(response.text)
    f.close()

if __name__=="__main__":
    main()