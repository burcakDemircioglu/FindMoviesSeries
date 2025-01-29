import requests
from dotenv import dotenv_values
import os
import FindMoviesSeries.backend.RetrieveInfo as RetrieveInfo

BASEDIR = os.path.abspath(os.path.dirname(__file__))
secrets = dotenv_values(os.path.join(BASEDIR, '.env'))

def main():

    RetrieveInfo.retrieveMovies(secrets["API_BEARER"])


if __name__ == "__main__":
    main()
