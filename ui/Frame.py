import customtkinter
from PIL import Image
import FindMoviesSeries.backend.RetrieveInfo as RetrieveInfo

class Frame(customtkinter.CTk):
    def buttonClick(self):
        response = RetrieveInfo.retrieveMovies(self.secrets["API_BEARER"])
        self.textbox.insert("0.0", response)

    def __init__(self, secrets):
        super().__init__()
        self.secrets=secrets

        customtkinter.set_appearance_mode("dark")

        self.title("FindMoviesSeries")
        self.geometry("700x450")

        self.textbox=customtkinter.CTkTextbox(master=self, width=400, height=400)
        self.textbox.pack(pady=10, padx=10)

        self.button = customtkinter.CTkButton(master=self, text="find movies", command=self.buttonClick)
        self.button.pack(pady=10, padx=10)
    
