import lectio
import os
from colorama import Fore
from dotenv import load_dotenv

load_dotenv()

HOLD = {
    "h21hx3u-MA": "Matematik",
    "h21hx3u-EN": "Engelsk",
    "h23hx-3a-SOP": "SOP",
    "h21hx3u-DA": "Dansk",
    "h21hx3u-FYA": "Fysik",
    "h22hx3u-Ih": "Idéhistorie",
    "h23hx3u24-div": "Diverse",
    "h21hx3u-teamlærer": "Teamlærer",
    "h23hx-3u-eamv": "Erhvervsakademi Midtvest",
    "h23hx-3u-livsmestring": "Livsmestring",
    "h23hx-3u-minimesse": "Minimesse",
    "h23hx-3u-påskefrokost": "Påskefrokost",
    "h23hx-3u-SOP intro": "SOP intro",
    "h23hx-3u-tour": "Tur",
    "h23hxin-vf": "Innovation",
    "h23hxTK-MAS": "Maskinværksted",
    "h21hx3a-FY, h21hx3u-FYA": "Fysik"
}

class LectioHandler:
    def __init__(self, username: str, password: str, skoleID: str) -> None:
        self.client = lectio.sdk(brugernavn=username, adgangskode=password, skoleId=skoleID)
        self.user = self.client.fåElev(self.client.elevId)
        print(f"{Fore.GREEN}Logget ind til lektio som elevID: " + Fore.YELLOW + self.client.elevId, Fore.RESET)
        print(f"{Fore.GREEN}Elev: " + Fore.YELLOW + self.client.fåElev(self.client.elevId)['navn'], Fore.RESET)

    def få_skema_for_dag(self, dag: int | str, uge: int, år: int):
        daglige_skema = {}
        skema = self.client.skema(uge=uge, år=år)
        
        for i, modul in enumerate(skema["moduler"][dag], 1):
            daglige_skema[f"{i}. modul"] = f"{HOLD[modul['hold']]}"

        return daglige_skema
    
    