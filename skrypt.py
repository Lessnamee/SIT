# funkcja dot. dat, importowanie z moduły zewnętrznego
# funkcja dot. dat, importowanie z moduły zewnętrznego
from datetime import date

def importPunkty(path = './dane.txt'):
    '''
    funkcja do importu punktów do listy słówników. Pierwsza linia to nazwy słowników
    path - plik do importu,
    '''
    '''
    Import pliku podanego w zmiennej path
    '''
    file = open(path, "r+")
    lista = []
    while file:
        linia = file.readline()
        
        if linia == "":
            break
        else:
            lista.append(linia.split())
        
    file.close()
    '''
    Grupowanie otrzymanych punktow  w taki sposob, by po kazdej nowej pustej linii zostala stworzona nowa grupa punktow.
    Pozwala to na przyjecie dowolnej liczby dzialek.
    '''
    klucze = lista[0]
    listaPunktowTworzacychPola = []
    listaDict = []
    for i in range(1, len(lista)):
        if len(lista[i]) == 0:
            listaPunktowTworzacychPola.append(listaDict)
            listaDict = []
        else:
            listaDict.append(dict(zip(klucze,lista[i])))
    listaPunktowTworzacychPola.append(listaDict)
    return listaPunktowTworzacychPola

def importSzablon(path):
    '''
    import szablonu XML - dowolnego do ziennej tekstowej
    '''
    file = open(path, "r+", encoding = "utf-8")
    szablon = file.read()
    return szablon

def exportXML(path,dane):
    '''
    import szablonu XML do pliku tekstowego
    '''
    file = open(path, "w+", encoding = "utf-8")
    file.write(dane)
    file.close()


def pole(punkty):
    '''
    funkcja która liczy pole pow. ze współzednych
    brakuje poprawki ze względu na odwzorowanie kartograficzne
    samoedzielnie!!!
    '''
    '''
    Dodac ta cholerna poprawke! xD 
    '''
    for item in punkty:
        item['X'] = float(item['X'])
        item['Y'] = float(item['Y'])

    pole = 0
    for i in range(0,len(punkty)):
        if i == 0:
            pole += (punkty[i+1]['X']-punkty[len(punkty)-1]['X'])*punkty[i]['Y']
            print ('coś', i, pole)
        elif i == len(punkty)-1:
            pole += (punkty[0]['X']-punkty[i-1]['X'])*punkty[i]['Y']
            print ('coś innego', i, pole)
        else:
            pole += (punkty[i+1]['X']-punkty[i-1]['X'])*punkty[i]['Y']
            print ('reszta', i, pole)

    pole = - pole / 2 /10000
    return pole

def zamienPktwXML(punkt,szablon):
    '''
    tutaj zamian elementów XML w dla punktów granicznych
    przykłąd dla #1
    samodzielnie reszta!
    '''
    '''
    Funkcja mapujaca punkt na szablon Punktu Granicznego 
    W kazde ----x---- sa wstawiane odpowiednie wartosci do szablonu
    '''
    punktXML = '\n'.join(szablon.split("\n")[1:])

    stala = 'PL.PZGiK.307.EGiB_4EAF9C5D-413E-4BCF-B8E0-'
    numerPelny = stala+str(punkt['nr'])+'_'+str(date.today())+'T00-00-00'

    punktXML = punktXML.replace('----1-----',numerPelny)

    dwojka = 'urn:pzgik:id:'+ 'PL.PZGiK.307.EGiB:4EAF9C5D-413E-4BCF-B8E0-' + str(punkt['nr'])+':'+str(date.today())+'T00-00-00'
    punktXML = punktXML.replace('----2-----',dwojka)
    
    trojka = '4EAF9C5D-413E-4BCF-B8E0-' + str(punkt['nr'])
    punktXML = punktXML.replace('----3-----',trojka)

    drugaTrojka = str(date.today())+'T00-00-00'
    '''
    Na poczatku tu bylo ----3---, ale to chyba blad, bo to powinna byc chyba inna wartosc, 
    wiec zostalo to zastopiane 3v2 - tak samo w pliku punktuGraniczego.xml
    '''
    punktXML = punktXML.replace('----3v2-----',drugaTrojka)

    czworka = str(date.today())+'T00-00-00'
    punktXML = punktXML.replace('----4-----',czworka)

    wsp = str(float(punkt['X'])) + ' ' + str(float(punkt['Y']))
    punktXML = punktXML.replace('---wsp---',wsp)
    '''
    #99 zostal wstawiony specjalnie, by byl w stanie widziec numery punktow w Geoportalu
    '''
    punktXML = punktXML.replace('#99',punkt['nr'])
    return punktXML

def zmienXML(punkty, szablon):
    '''
    funkcja zmieniąca szablon dla punktów z listy
    odwołanie do funkcji zamienPktwXM() - funkcja zagnieżdzona
    '''
    xmlUpdate = ''
    for i in punkty:
        xmlUpdate += zamienPktwXML(i, szablon)
    return xmlUpdate

def listaWsp(punkty):
    '''
    funkcja przykładowa jak zrobić z listy punktów jedną linijkę
    z wsp. punktów zgodnie z GML - ten same wsp. na poczatku i na końcu
    '''

    tekst  = ''
    for i in punkty:
        tekst += str(i['X']) +' ' + str(i['Y'])
    tekst +=  str(punkty[0]['X']) +' ' + str(punkty[0]['Y'])
    return tekst

def zamienDZwXML(nrDz, punkty,szablon):
    '''
    tutaj zamian elementów XML dal dzialki
    przykład dla #7
    samodzielnie reszta!
    '''
    '''
    Funckja mapujaca nr dzialki oraz punkty dla tej dzialki na szablon dzialki ewidencyjnej
    '''

    dzXML = szablon
    tekstPomoc = ''
    szostka = ''
    for i in punkty:
        '''
        <egb:punktGranicyDzialki xlink:href="urn:pzgik:id:PL.PZGiK.307.EGiB:4EAF9C5D-413E-4BCF-B8E0-
        '''
        stale = '<egb:punktGranicyDzialki xlink:href="urn:pzgik:id:PL.PZGiK.307.EGiB:4EAF9C5D-413E-4BCF-B8E0-'
        popLinijka = stale + str(i['nr']) + '"/>'

        tekstPomoc += popLinijka + '\n'
        szostka += ' ' + str(float(i['X'])) + ' ' + str(float(i['Y']))

    tekstPomoc = tekstPomoc.rstrip()          # skasowanie przescia do nastepnej linii na koniec tekstu do podmiany
    dzXML = dzXML.replace('#7', tekstPomoc)
    dzXML = dzXML.replace('#6', szostka)

    piatka = str(pole(punkty))
    dzXML = dzXML.replace('#5', piatka)

    czworka = str(nrDz)
    dzXML = dzXML.replace('#4', czworka)

    trojka = str(date.today())+'T00-00-00'
    dzXML = dzXML.replace('#3', trojka)

    dwa = '942B7532-4FAC-4279-AC25-65D5128CFE72' +':'+str(date.today())+'T00:00:00'
    dzXML = dzXML.replace('#2', dwa)
    jeden = '"942B7532-4FAC-4279-AC25-65D5128CFE72' +'_'+str(date.today())+'T00-00-00"'
    dzXML = dzXML.replace('#1', jeden)
    
    return dzXML

def zamienListePunktowListeXML(listaPunktow, szablon):
    '''
    Zamiana listy list punktow w liste punktow zmapowanych na xml
    '''
    xmlListaPuntkow = []
    for punkty in listaPunktow:
        xmlListaPuntkow.append(zmienXML(punkty, szablon))
    return xmlListaPuntkow

def pobierzNrDzialek(listaPunktow):
    nrDzialek = []
    for _ in range(len(listaPunktow)):
        nrDzialek.append(input('Podaj nr dzialki -> '))
    return nrDzialek

def stworzListeDzialekXML(nrDzialek, listaPunktow, szablonDzEwid):
    xmlListaDzialek = []
    for i in range(len(nrDzialek)):
        xmlListaDzialek.append(zamienDZwXML(nrDzialek[i], listaPunktow[i], szablonDzEwid))
    return xmlListaDzialek


def zlaczDzialkiEwidIPunkty(xmlListaDzialek, xmlListaPunktow):
    dzialkiIPunkty = '<?xml version="1.0" encoding="UTF-8"?>\n' + '<gml:FeatureCollection xmlns:os="urn:gugik:specyfikacje:gmlas:osnowaGeodezyjna:1.0" xmlns:ges="urn:gugik:specyfikacje:gmlas:geodezyjnaEwidencjaSieciUzbrojeniaTerenu:1.0" xmlns:bdz="urn:gugik:specyfikacje:gmlas:bazaDanychObiektowTopograficznych500:1.0" xmlns:egb="urn:gugik:specyfikacje:gmlas:ewidencjaGruntowBudynkow:1.0" xmlns:bt="urn:gugik:specyfikacje:gmlas:modelPodstawowy:1.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rcw="urn:gugik:specyfikacje:gmlas:rejestrCenIWartosciNieruchomosci:1.0" xsi:schemaLocation="urn:gugik:specyfikacje:gmlas:modelPodstawowy:1.0 BT_ModelPodstawowy.xsd urn:gugik:specyfikacje:gmlas:osnowaGeodezyjna:1.0 OS_Osnowa.xsd urn:gugik:specyfikacje:gmlas:geodezyjnaEwidencjaSieciUzbrojeniaTerenu:1.0 GESUT.xsd urn:gugik:specyfikacje:gmlas:bazaDanychObiektowTopograficznych500:1.0 BDOT500.xsd urn:gugik:specyfikacje:gmlas:ewidencjaGruntowBudynkow:1.0 EGB_OgolnyObiekt.xsd urn:gugik:specyfikacje:gmlas:rejestrCenIWartosciNieruchomosci:1.0 RCW_RCiWN.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd" gml:id="_GML">' + '\n'
    for i in range(len(xmlListaDzialek)):
        dzialkiIPunkty += xmlListaPunktow[i] + '\n' + xmlListaDzialek[i]

    dzialkiIPunkty += '</gml:FeatureCollection>'
    return dzialkiIPunkty


print('--------------------------')
'''
Tutaj jest cale wykonanie programu:
'''
listaPunktow = importPunkty()
szablonPG = importSzablon('szablonPG.xml')
szablonDzEwid = importSzablon('szablonDzEwid.xml')

nrDzialek = pobierzNrDzialek(listaPunktow)

xmlListaPuntkow = zamienListePunktowListeXML(listaPunktow, szablonPG)
xmlListaDzialek = stworzListeDzialekXML(nrDzialek, listaPunktow, szablonDzEwid)

wersjaKoncowa = zlaczDzialkiEwidIPunkty(xmlListaDzialek, xmlListaPuntkow)

exportXML(r'daneXML.gml', wersjaKoncowa)
'''
Powodzenia, Mordy! XD 
'''