from datetime import datetime, timedelta

class Berles:
    def __init__(self, auto, kezdo_idopont, berlo_neve):
        self.auto = auto
        self.kezdo_idopont = kezdo_idopont
        self.vege_idopont = kezdo_idopont + timedelta(hours=24)
        self.berlo_neve = berlo_neve

    def get_info(self):
        kezdo = self.kezdo_idopont.strftime("%Y-%m-%d %H:%M")
        vege = self.vege_idopont.strftime("%Y-%m-%d %H:%M")
        return f"Bérlő: {self.berlo_neve}, Bérelt autó: {self.auto.get_info()}, Kezdés: {kezdo}, Vége: {vege}"