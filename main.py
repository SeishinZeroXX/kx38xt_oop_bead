from datetime import datetime, timedelta
from auto import Szemelyauto, Teherauto
from autokolcsonzo import Autokolcsonzo

def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Hiba: Az üres bemenet nem megengedett. Kérem, hogy adjon meg egy értéket.")
    
def main():
    kolcsonzo = Autokolcsonzo("Ocskó Bianka (KX38XT) autókölcsönzője")

    kolcsonzo.auto_hozzaadasa(Szemelyauto("AAA-111", "Opel Astra", 5000, 5))
    kolcsonzo.auto_hozzaadasa(Szemelyauto("BBB-222", "Toyota Corolla", 6000, 5))
    kolcsonzo.auto_hozzaadasa(Teherauto("CCC-333", "Ford Transit", 8000, 1500))

    most = datetime.now()
    kolcsonzo.auto_berlese("AAA-111", most, "Gipsz Jakab")
    kolcsonzo.auto_berlese("BBB-222", most + timedelta(hours=1), "Teszt Elek")
    kolcsonzo.auto_berlese("CCC-333", most + timedelta(hours=2), "Vincs Eszter")
    kolcsonzo.auto_berlese("AAA-111", most + timedelta(days=1), "Eszet Lenke")

    while True:
        print("\n1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Bérlések listázása")
        print("4. Kilépés")

        valasztas = get_non_empty_input("Válasszon egy műveletet (1-4): ")

        if valasztas == "1":
            while True:
                datum_str = get_non_empty_input("Adja meg a bérlés kezdő időpontját (ÉÉÉÉ-HH-NN ÓÓ:PP), vagy írjon 'q'-t a menühöz való visszatéréshez: ")
                if datum_str.lower() == 'q':
                    break
                try:
                    kezdo_idopont = datetime.strptime(datum_str, "%Y-%m-%d %H:%M")
                    most = datetime.now()
                    if kezdo_idopont < most:
                        print("Hiba: A megadott dátum vagy időpont a mai nap előtti. Kérem, hogy adjon meg egy jövőbeli dátumot.")
                        continue
                    
                    elerheto_autok = [auto for auto in kolcsonzo.autok if not any(
                        berles.auto.rendszam == auto.rendszam and 
                        (berles.kezdo_idopont <= kezdo_idopont < berles.vege_idopont or
                         berles.kezdo_idopont < kezdo_idopont + timedelta(hours=24) <= berles.vege_idopont or
                         kezdo_idopont <= berles.kezdo_idopont < kezdo_idopont + timedelta(hours=24))
                        for berles in kolcsonzo.berlesek
                    )]
                    
                    if elerheto_autok:
                        print("Elérhető autók:")
                        headers = ["Rendszám", "Típus", "Kategória", "Jellemző"]
                        data = []
                        for auto in elerheto_autok:
                            if isinstance(auto, Szemelyauto):
                                data.append([auto.rendszam, auto.tipus, "Személyautó", f"Utasok száma: {auto.utasok_szama}"])
                            elif isinstance(auto, Teherauto):
                                data.append([auto.rendszam, auto.tipus, "Teherautó", f"Teherbírás: {auto.teherbiras} kg"])
                        
                        col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *data)]
                
                        header_row = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
                        print(header_row)
                        print("-" * len(header_row))
                        
                        for row in data:
                            print(" | ".join(f"{str(item):<{w}}" for item, w in zip(row, col_widths)))

                        rendszam = get_non_empty_input("Adja meg a bérelni kívánt autó rendszámát, vagy írjon 'uj'-at új dátum megadásához, vagy 'q'-t a menühöz való visszatéréshez: ").upper()
                        if rendszam.lower() == 'q':
                            break
                        elif rendszam.lower() == 'uj':
                            continue
                        
                        berlo_neve = get_non_empty_input("Adja meg a bérlő személy teljes nevét: ")
                        
                        ar = kolcsonzo.auto_berlese(rendszam, kezdo_idopont, berlo_neve)
                        if ar:
                            vege_idopont = kezdo_idopont + timedelta(hours=24)
                            auto = next(auto for auto in kolcsonzo.autok if auto.rendszam == rendszam)
                            print(f"Az autó sikeresen kibérelve!")
                            headers = ["Bérlő", "Rendszám", "Típus", "Kategória", "Jellemző", "Kezdés", "Vége", "Bérleti díj"]
                            kategoria = "Személyautó" if isinstance(auto, Szemelyauto) else "Teherautó"
                            jellemzo = f"Utasok száma: {auto.utasok_szama}" if isinstance(auto, Szemelyauto) else f"Teherbírás: {auto.teherbiras} kg"
                            data = [[
                                berlo_neve,
                                auto.rendszam,
                                auto.tipus,
                                kategoria,
                                jellemzo,
                                kezdo_idopont.strftime("%Y-%m-%d %H:%M"),
                                vege_idopont.strftime("%Y-%m-%d %H:%M"),
                                f"{ar} Ft / 24 óra"
                            ]]

                            col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *data)]
    
                            header_row = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
                            print(header_row)
                            print("-" * len(header_row))
    
                            print(" | ".join(f"{str(item):<{w}}" for item, w in zip(data[0], col_widths)))
                            break
                        else:
                            print("Hiba: Az autó nem bérelhető a megadott időpontra vagy érvénytelen rendszám.")
                    else:
                        print("Sajnos nincs elérhető autó a megadott időpontban.")
                        valasz = input("Szeretne új dátumot megadni? (Igen / Nem): ")
                        if valasz.lower() != 'igen':
                            break
                except ValueError:
                    print("Hiba: A beírt dátum formátuma nem megfelelő (Helyes: ÉÉÉÉ-HH-NN ÓÓ:PP), vagy visszamenőleges dátumra mutat!")

        elif valasztas == "2":
            rendszam = get_non_empty_input("Adja meg a lemondani kívánt autó rendszámát: ").upper()
            datum_str = get_non_empty_input("Adja meg a bérlés kezdő időpontját (ÉÉÉÉ-HH-NN ÓÓ:PP): ")
            berlo_neve = get_non_empty_input("Adja meg a bérlő személy teljes nevét: ").lower()
            try:
                kezdo_idopont = datetime.strptime(datum_str, "%Y-%m-%d %H:%M")
                if kolcsonzo.berles_lemondasa(rendszam, kezdo_idopont, berlo_neve):
                    print("A bérlés sikeresen lemondva.")
                else:
                    print("Hiba: A megadott bérlés nem található.")
            except ValueError:
                print("Hiba: Érvénytelen időpont formátum. Használja az ÉÉÉÉ-HH-NN ÓÓ:PP formátumot.")

        elif valasztas == "3":
            headers, berlesek = kolcsonzo.berlesek_listazasa()
            if berlesek:
                print("Aktuális bérlések:")

                col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *berlesek)]
                
                header_row = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
                print(header_row)
                print("-" * len(header_row))
                
                for row in berlesek:
                    print(" | ".join(f"{str(item):<{w}}" for item, w in zip(row, col_widths)))
            else:
                print("Nincs aktív bérlés.")

        elif valasztas == "4":
            print("Köszönjük, hogy Ocskó Bianka (KX38XT) Autókölcsönzőjét választotta! Reméljük, hogy 5 csillagra értékel bennünket a Neptunon :)")
            break
        else:
            print("Hiba: Érvénytelen választás. Kérem, válasszon 1 és 4 között.")

if __name__ == "__main__":
    main()