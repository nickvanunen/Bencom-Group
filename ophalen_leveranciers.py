# Dit betreft een applicatie (in Python) die elke dag van de site van de ACM alle energieleveranciers opslaat.
# Dit script zou aangeroepen moeten worden met een cronjob zodat de data elke dag opgehaald kan worden (om dit script 24/7 aan te laten staan zou inefficient zijn en onnodig)
import pandas as pd
import datetime


def get_two_lists_from_url(url, t1, t2):
    """Deze functie krijgt een URL en 2 tabelnamen. Vervolgens verhaald deze alle namen uit de
    opgegeven website en de onderliggende 2 tabbelen. Duplicaten en nan waardes worden niet meegenomen."""
    table = pd.read_html(url)
    list1 = table[0][t1].tolist()
    list2 = table[1][t2].tolist()
    complete_list = list1 + list2
    complete_list = [x for x in complete_list if pd.isnull(x) == False]
    return list(dict.fromkeys(complete_list))


def save_to_file(list, file_name):
    """Deze functie ontvangt een lijst en schrijft deze naar een bestand en noemt deze naar een opgegeven bestandsnaam."""
    file = open(file_name, "w")
    for i in list:
        file.write(i + '\n')
    file.close()

def main():

    # De tabelnamen definieren en meegeven in de functie om alle energieleveranciers op te halen
    # Vervolgens alle energie leveranciers ophalen vanaf https://www.acm.nl/nl/onderwerpen/energie/energiebedrijven/vergunningen/vergunninghouders-elektriciteit-en-gas
    url = 'https://www.acm.nl/nl/onderwerpen/energie/energiebedrijven/vergunningen/vergunninghouders-elektriciteit-en-gas'
    table_elek = 'Naam vergunninghouder elektriciteit'
    table_gas = 'Naam vergunninghouder gas'
    print('##### Ophalen van energieleveranciers uit ACM...')
    energieleveranciers = get_two_lists_from_url(url, table_elek, table_gas)
    print('Energieleveranciers opgehaald!\n')

    # Huidige energieleveranciers opslaan naar bestand met de datum van vandaag in de bestandsnaam
    print('##### Energieleveranciers opslaan naar bestand genaamd energieleveranciers_{0}.txt...'.format(str(datetime.date.today())))
    energieleveranciers_txt = 'energieleveranciers_{0}.txt'.format(str(datetime.date.today()))
    save_to_file(energieleveranciers, energieleveranciers_txt)
    print('Bestand {0} gereed!'.format(energieleveranciers_txt))

if __name__ == '__main__':
    main()
