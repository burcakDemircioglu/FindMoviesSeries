import os
from dotenv import dotenv_values

import FindMoviesSeries.ui.MainFrame as MainFrame
import FindMoviesSeries.backend.InfoRetriever as InfoRetriever

BASEDIR = os.path.abspath(os.path.dirname(__file__))
secrets = dotenv_values(os.path.join(BASEDIR, ".env"))


def main():
    infoRetreiver = InfoRetriever.InfoRetriever(secrets)
    app = MainFrame.MainFrame(infoRetreiver)
    app.mainloop()


if __name__ == "__main__":
    main()
