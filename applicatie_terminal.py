# Dit sript kan de volgende informatie opzoeken van een ingegeven energieleverancier: Naam; Adres website; Logo
# Deze gegevens worden opgeslagen in een zogenaamd .json format
# Tevens is er een functie welke meldt wanneer er een nieuwe energieleverancier is gevonden en wanneer een energieleverancier gestopt is.
from googlesearch import search
from bs4 import BeautifulSoup
import urllib.request
import ssl
import datetime
import json


ssl._create_default_https_context = ssl._create_unverified_context


def read_from_file(file):
    """Deze functie leest alle regels van een opgegeven bestand en slaat deze op in een list.
    Mits er geen bestand is gevonden zal de applicatie worden afgesloten."""
    try:
        with open(file) as f:
            lines = [line.rstrip() for line in f]
        return lines
    except:
        print('{0} is niet gevonden...\n'.format(file))
        print('Applicatie wordt afgesloten.')
        quit()


def get_website(company, search_term):
    """Deze functie doet een Google Search op basis van opgegeven zoekterm en geeft het hoogste resultaat in de vorm van een URL terug."""
    query = search_term + company
    for r in search(query, tld='nl', lang='nl', num=1, stop=1, pause=10):
        website = r
    return website


def get_logo(url):
    """Deze functie zoekt op basis een website naar het eerst gevonden img tag met een naam indicatie "logo" binnen de website en geeft de url terug."""
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, 'html.parser')
    for img in soup.findAll('img'):
        if 'logo' in img.get('src').lower() or 'logo' in img.get('id').lower() or 'logo' in img.get('class').lower() or 'logo' in img.get('alt').lower():
            logo = img.get('src')
            break
    if logo[0:4] != 'http':
        logo = url + logo
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


def write_to_json(d):
    """Deze functie schrijft een dictionary naar een json bestand genaamd resultaten.json"""
    with open('resultaten.json', 'w') as fp:
        json.dump(d, fp)


def main():

    # Check of er nieuwe energieleveranciers zijn of dat oude zijn gestopt op basis van bestanden en stop de resultaten in lijsten (nieuwe items en oude items).
    print('##### Controleren of er nieuwe energieleveranciers zijn bijgekomen of dat er energieleveranciers zijn gestopt...')
    energieleveranciers_txt = 'energieleveranciers_{0}.txt'.format(str(datetime.date.today()))
    energieleveranciers_txt_old = 'energieleveranciers_{0}.txt'.format(str(datetime.date.today() - datetime.timedelta(days=1)))
    nieuwe_energieleveranciers, oude_energieleveranciers = check_energieleveranciers(energieleveranciers_txt, energieleveranciers_txt_old)

    # Vermelden welke nieuwe en oude items er zijn, mits deze er zijn.
    if nieuwe_energieleveranciers != []:
        print('Nieuwe energieleveranciers: {}'.format(nieuwe_energieleveranciers))
    else:
        print('Er zijn geen nieuwe energieleveranciers ten opzichte van gisteren.')
    if oude_energieleveranciers != []:
        print('Oude energieleveranciers: {}'.format(oude_energieleveranciers))
    else:
        print('Er zijn geen energieleveranciers gestopt ten opzichte van gisteren.')
    print('Nieuwe en gestopte energieleveranciers gecontroleerd!\n')

    # Haal de website en het logo op van een ingegeven leverancier.
    # Wachten op de gebruikers input totdat deze 'q' invoert om de applicatie te stoppen.
    # Sla voor elke ingegeven leverancier op in een dictionary welke aan het einde wordt weggeschreven naar een json file.
    i = ' '
    d = {}
    while i != 'q':
        i = input('Voer een energieleverancier in (press "q" to quit): ')
        if i == 'q':
            write_to_json(d)
            print('\nGezochte resultaten zijn opgeslagen in resultaten.json!')
            print('Applicatie wordt afgesloten.')
            quit()
        ingegeven_energieleverancier = i
        print('\n##### Ophalen van website middels Google Seach...')
        website = get_website(ingegeven_energieleverancier, 'energieleverancier ')
        print('Website succesvol opgezocht!\n')
        print('##### Ophalen logo van energieleverancier...')
        logo = get_logo(website)
        print('Logo succesvol opgehaald!\n')
        d[ingegeven_energieleverancier] = [website,logo]
        print(d[ingegeven_energieleverancier])
    else:
        write_to_json(d)
        print('\nGezochte resultaten zijn opgeslagen in resultaten.json!')
        print('Applicatie wordt afgesloten.')
        quit()


if __name__ == '__main__':
    main()
