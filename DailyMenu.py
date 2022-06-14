from urllib.request import urlopen
from urllib.error import HTTPError
import re
from datetime import datetime

# !!! check if correct day

def wochentag():
    wochentage = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]
    tag_num = datetime.today().weekday()

    if tag_num >= 5:
        print("Mensas are closed over the weekend. (I think so)")
        raise AssertionError
    
    return wochentage[tag_num]


def get_html(mensa_id):
    """
    returns html of menu for mensa with id mensa_id
    """
    url = "https://www.mensa.uzh.ch/de/menueplaene/" + mensa_id + "/" + wochentag()
    
    try:
        page = urlopen(url)
    except:
        # !!! make error more specific
        print("Something didn't work with this webpage (id={}). Most likely the id is incorrect.\nPlease correct or remove this mensa and try again.".format(mensa_id))
        raise

    html = page.read().decode("utf-8")

    return html


def get_menu_name(source):
    """
    gets menu names from source, formats them and returns them as list of strings
    """
    
    pattern = "<h3>.*?<span>"
    menu_name = re.findall(pattern, source, re.IGNORECASE)
    for i in range(len(menu_name)):
        menu_name[i] = re.sub("<.*?>", "", menu_name[i])
    
    return menu_name


def get_menu(source):
    """
    gets menues from source, formats them and returns them as list of strings
    """

    pattern = "</span> </h3>.*?</p>"
    menu = re.findall(pattern, source, re.DOTALL)

    for i in range(len(menu)):
        menu[i] = re.sub("Fleisch:.*?$", "", menu[i])
        menu[i] = re.sub("<br>", ",", menu[i])
        menu[i] = re.sub("<.*?>", "", menu[i])
        menu[i] = re.sub("\n", "", menu[i])
        menu[i] = re.sub(" ,", ",", menu[i])
        menu[i] = re.sub("^ *", "", menu[i])
        menu[i] = re.sub(", *$", "", menu[i])

    return menu


def menu_uzh(mensas):
    """
    Prints menues of all mensas in "mensas"
    """
    for mensa, id in mensas.items():
        html = get_html(id)
        menu_name = get_menu_name(html)
        menu = get_menu(html)
        
        print("|||  ", mensa, "  |||\n")
        for i in range(len(menu_name)):
            print("   " + menu_name[i] + ":\n\n        " + menu[i], "\n\n")
    return


mensas = {
    "Untere Mensa": "zentrum-mercato",
    "Obere Mensa": "zentrum-mensa",
    "Platte 14": "platte-14",
    "Rämi 59": "raemi59",
    "Zahnmedizin": "cafeteria-zzm",
    } # Polymensa, Clausius, Foodtruck


if __name__ == "__main__":
    menu_uzh(mensas)