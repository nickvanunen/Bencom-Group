# Dit sript kan de volgende informatie opzoeken van een ingegeven energieleverancier: Naam; Adres website; Logo
# Deze gegevens worden opgeslagen in een zogenaamd .json format
# Tevens is er een functie welke meldt wanneer er een nieuwe energieleverancier is gevonden en wanneer een energieleverancier gestopt is.
# Dit is de web versie en zal een pagina hosten op de localhost
import tkinter as tk
from googlesearch import search
from bs4 import BeautifulSoup
import urllib.request
import requests
import ssl
import datetime
import webbrowser
import json


ssl._create_default_https_context = ssl._create_unverified_context


def read_from_file(file):
    """Deze functie leest alle regels van een opgegeven bestand en slaat deze op in een list en geeft deze terug."""
    with open(file) as f:
        lines = [line.rstrip() for line in f]
    return lines


def get_website(company, search_term):
    """Deze functie doet een Google Search op basis van opgegeven zoekterm en geeft het hoogste resultaat in de vorm van een URL terug."""
    query = search_term + company
    print('Zoeken...')
    for r in search(query, tld='nl', lang='nl', num=1, stop=1, pause=2):
        website = r
    return website


def get_logo(url):
    """Deze functie zoekt op basis een website naar het eerst gevonden img tag met een naam indicatie "logo" binnen de website en geeft de url terug."""
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, 'html.parser')
    for img in soup.findAll('img'):
        if 'logo' in img.get('src') or 'logo' in img.get('id') or 'logo' in img.get('class') or 'logo' in img.get('alt'):
            logo = img.get('src')
            break
    if logo[0:2] == '//':
        logo = logo.replace('//','http://')
    elif logo[0:4] != 'http':
        logo = url + logo
    elif '///' in logo:
        logo = logo.replace('///','/')
    return logo


def check_energieleveranciers(new_file, old_file):
    """Deze functie vergelijkt 2 txt bestanden en geeft 2 lijsten waarvan 1 met nieuw toegevoegde items en 1 met verwijderde items."""
    new_items = []
    old_items = []
    new_list = read_from_file(new_file)
    old_list = read_from_file(old_file)
    for i in new_list:
        if i not in old_list:
            new_items.append(i)
    for i in old_list:
        if i not in new_list:
            old_items.append(i)
    return new_items, old_items


def download_file(logo, ingegeven_energieleverancier):
    """Deze functie download een image en slaat deze op in de img map, de bestandnaam is gebaseerd op de ingevoerde energieleverancier."""
    response = requests.get(logo)
    file_name = 'img/' + ingegeven_energieleverancier + '.png'
    file = open(file_name, "wb")
    file.write(response.content)
    file.close()
    return file_name


def show_website_and_logo(window, entry, website_label, show_website, panel,d ):
    """Deze functie haalt de energieleverancier op, haalt de relevante website op, geeft deze weer in het venster, haalt vervolgens het bijbehorende logo op, download deze en geeft deze weer in het venster."""
    ingegeven_energieleverancier = entry.get()
    website_label.config(text="\nJe hebt gekozen voor {}.\n".format(ingegeven_energieleverancier))
    website = get_website(ingegeven_energieleverancier, "Energieleverancier ")
    show_website.config(text="De website van {0} is: {1} (klik op de site om deze te bezoeken)".format(ingegeven_energieleverancier, website))
    show_website.bind("<Button-1>", lambda e: callback(website))
    logo = get_logo(website)
    image = download_file(logo, ingegeven_energieleverancier)
    d[ingegeven_energieleverancier] = [website,logo]
    write_to_json(d)
    try:
        new_image = tk.PhotoImage(file=image)
        panel.config(image=new_image)
        panel.image = new_image
    except:
        panel.config(text="Geen (png type) afbeeldingen gevonden...")


def write_to_json(d):
    """Deze functie schrijft een dictionary naar een json bestand genaamd resultaten.json"""
    with open('resultaten.json', 'w+') as fp:
        json.dump(d, fp)


def callback(url):
    """Deze functie opent de opgegeven url in de webbrowser (hyperlink)."""
    webbrowser.open_new(url)


# Check of er nieuwe energieleveranciers zijn of dat oude zijn gestopt en stop deze in 2 lijsten (nieuwe en oude)
energieleveranciers_txt = 'energieleveranciers_{0}.txt'.format(str(datetime.date.today()))
energieleveranciers_txt_old = 'energieleveranciers_{0}.txt'.format(str(datetime.date.today() - datetime.timedelta(days=1)))
nieuwe_energieleveranciers, oude_energieleveranciers = check_energieleveranciers(energieleveranciers_txt, energieleveranciers_txt_old)
d = {}

# Maak een venster aan inclusief titel en afmetingen
window = tk.Tk()
window.title("Energieleverancier Opzoeker!")
window.geometry("1050x800")

# Geef de nieuwe en de oude energieleveranciers weer in het vester
nieuwe_en_oude_energieleveranciers = tk.Label(text="\nDit zijn de nieuwe energieleveranciers: \n{0}\n\nDit zijn de gestopte energieleveranciers: \n{1}\n\n".format(nieuwe_energieleveranciers, oude_energieleveranciers))
nieuwe_en_oude_energieleveranciers.pack()

# Geef een welkomstbericht in het venster
greeting = tk.Label(text="Welkom in de energieleverancier zoeker!\n\nVul hieronder een energieleverancier in om de website en het logo op te halen:")
greeting.pack()

# Maak een entry waar input in gegeven kan worden
entry = tk.Entry(window, fg="black",width=50)
entry.pack()

# Maak een knop welke de functie kan aanspreken die de website en het logo ophaalt
b = tk.Button(window,text='Search',command= lambda: show_website_and_logo(window, entry, website_note,show_website, panel, d))
b.pack()

# Maak een label welke aangeeft waarop is gezocht
website_note = tk.Label(text="\nJe hebt nog geen energieleverancier gezocht...")
website_note.pack()

# Maak een label waar de website weergegeven gaat worden
show_website = tk.Label(text=" ")
show_website.pack()

# Maak een label met een image, start met een test image in gif format
start_image = tk.PhotoImage(file="img/test.png")
panel = tk.Label(window, image=start_image)
panel.pack(side="bottom", fill="both", expand="yes")

window.mainloop()
