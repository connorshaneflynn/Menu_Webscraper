from urllib.request import urlopen, Request
from re import findall, sub, DOTALL, match
from datetime import date



def wochentag():
    """
    returns day of the week and stops script with message if it is the weekend
    """

    wochentage = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]
    tag_num = date.today().weekday()

    if tag_num >= 5:
        print("Mensas are closed over the weekend. (I think so)")
        input("")
        raise AssertionError
    
    return wochentage[tag_num]


def get_html(mensa_id):
    """
    returns html of menu for mensa with id mensa_id
    """
    if type(mensa_id) == str:
        url = f"https://www.mensa.uzh.ch/de/menueplaene/{mensa_id}/{wochentag()}"
    elif type(mensa_id) == int:
        url = f"https://ethz.ch/de/campus/erleben/gastronomie-und-einkaufen/gastronomie/menueplaene/offerDay.html?language=de&date={date.today()}&id={mensa_id}"

    else:
        raise NameError

    # User-Agent has to be specified, else opening the ethz.ch urls will throw an error. Exact User-Agent doesn't matter. (e.g. Safari/537.36, Mozilla/5.0, AppleWebKit/537.36)
    req = Request(url, headers={"User-Agent": "Chrome/102.0.0.0"})
    try:
        page = urlopen(req)
        
    except:
        # !!! make error more specific
        print(f"Something didn't work with this webpage (id={mensa_id}). Most likely the id is incorrect.\nPlease correct or remove this mensa and try again.")
        raise

    html = page.read().decode("utf-8")

    return html


def get_menu_name_uzh(source):
    """
    gets menu names from source (uzh), formats them and returns them as list of strings
    """
    
    pattern = "<h3>.*?<span>"
    menu_name = findall(pattern, source)
    for i in range(len(menu_name)):
        menu_name[i] = sub("<.*?>", "", menu_name[i])
    
    return menu_name

def get_menu_name_eth(source):
    """
    gets menu names from source (eth), formats them and returns them as list of strings
    """
    
    pattern = "<td> ?<strong>.*?</strong> ?</td>"
    menu_name = findall(pattern, source)
    for i in range(len(menu_name)):
        menu_name[i] = sub("<.*?>", "", menu_name[i])
        # optional: add sub for removing spaces before and after name in case source changes
    return menu_name


def get_menu_uzh(source):
    """
    gets menues from source (uzh), formats them and returns them as list of strings
    """

    pattern = "</span> </h3>.*?</p>"
    menu = findall(pattern, source, DOTALL)

    for i in range(len(menu)):
        menu[i] = sub("Fleisch:.*?$", "", menu[i])
        menu[i] = sub("<br>", ",", menu[i])
        menu[i] = sub("<.*?>", "", menu[i])
        menu[i] = sub("\n", "", menu[i])
        menu[i] = sub(" ,", ",", menu[i])
        menu[i] = sub("^ *", "", menu[i])
        menu[i] = sub(", *$", "", menu[i])

    return menu

def get_menu_eth(source):
    """
    gets menues from source (eth), formats them and returns them as list of strings
    """
    #(?!.*\b(?:ABEND)\b)
    pattern = "<td><strong>.*?<div class=\"allergene\">"
    menu = findall(pattern, source)
    
    for i in range(len(menu)):
        # filter
        #menu[i] = re.sub("<br>", ",", menu[i])
        menu[i] = sub("<.*?>", " ", menu[i])
        #menu[i] = re.sub("\n", "", menu[i])
        menu[i] = sub("  ", " ", menu[i])
        menu[i] = sub("Add on.*?$", "", menu[i]) # remove add ons, optional
        menu[i] = sub("^ *", "", menu[i])
        menu[i] = sub(" *$", "", menu[i])

    return menu


# backup:
def DailyMenu(mensas):
    """
    Prints menues of all mensas in "mensas"
    """
    for mensa, id in mensas.items():
        html = get_html(id)

        # ETH or UZH
        if type(id) == str:
            menu_name = get_menu_name_uzh(html)
            menu = get_menu_uzh(html)

        elif type(id) == int:
            menu_name = get_menu_name_eth(html)
            menu = get_menu_eth(html)

        else:
            raise NameError
        
        # in certain ethz menues one additional menu_name is found (ADD ONS), though length of menu is always correct
        print("|||  ", mensa, "  |||\n")
        for i in range(len(menu)):
            # remove evening menues, optional
            if match(".*?ABEND",menu_name[i]):
                continue

            print("  ●  " + menu_name[i] + ":\n\n        " + menu[i], "\n\n")

    return


# specify mensas to get menues from
mensas = {
    "Untere Mensa": "zentrum-mercato",
    "Obere Mensa": "zentrum-mensa",
    "Platte 14": "platte-14",
    "Rämi 59": "raemi59",
    "Zahnmedizin": "cafeteria-zzm",
    "Polymensa": 12,
    "Clausiusbar": 4,
    "Foodtrailer ETZ": 9,}


if __name__ == "__main__":

    DailyMenu(mensas)

    input("\n\n....................................................")