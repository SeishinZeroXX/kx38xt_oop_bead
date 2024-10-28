from datetime import datetime, timedelta
from berles import Berles

class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaadasa(self, auto):
        self.autok.append(auto)

    def auto_berlese(self, rendszam, kezdo_idopont, berlo_neve):
        most = datetime.now()
        if kezdo_idopont < most:
            return None

        auto = next((a for a in self.autok if a.rendszam == rendszam), None)
        if auto:
            vege_idopont = kezdo_idopont + timedelta(hours=24)
            if not any(b.auto.rendszam == rendszam and 
                    ((b.kezdo_idopont <= kezdo_idopont < b.vege_idopont) or
                        (b.kezdo_idopont < vege_idopont <= b.vege_idopont) or
                        (kezdo_idopont <= b.kezdo_idopont and vege_idopont >= b.vege_idopont))
                    for b in self.berlesek):
                berles = Berles(auto, kezdo_idopont, berlo_neve)
                self.berlesek.append(berles)
                return auto.berleti_dij
        return None
    
    def berles_lemondasa(self, rendszam, kezdo_idopont, berlo_neve):
        berles = next((b for b in self.berlesek if 
                       b.auto.rendszam.upper() == rendszam.upper() and 
                       abs((b.kezdo_idopont - kezdo_idopont).total_seconds()) < 3600 and
                       b.berlo_neve.lower() == berlo_neve.lower()), None)
        if berles:
            self.berlesek.remove(berles)
            return True
        return False
        
    def berlesek_listazasa(self):
        headers = ["Bérlő", "Rendszám", "Típus", "Kezdés", "Vége"]
        data = []
        for b in self.berlesek:
            data.append([
                b.berlo_neve,
                b.auto.rendszam,
                b.auto.tipus,
                b.kezdo_idopont.strftime("%Y-%m-%d %H:%M"),
                b.vege_idopont.strftime("%Y-%m-%d %H:%M")
            ])
        return headers, data