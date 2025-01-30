import os
from dotenv import dotenv_values

import FindMoviesSeries.ui.MainFrame as MainFrame

BASEDIR = os.path.abspath(os.path.dirname(__file__))
secrets = dotenv_values(os.path.join(BASEDIR, '.env'))

def main():
    app = MainFrame.MainFrame(secrets)
    app.mainloop()

if __name__ == "__main__":
    main()
