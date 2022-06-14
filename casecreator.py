import FGSBuddyLight
from lxml import etree
from xml.etree.ElementTree import QName
import uuid
import random
import string
import hashlib
import mimetypes
import os
import radar
from datetime import datetime
from reportlab.pdfgen import canvas
from docx import Document
from rich.progress import track


cwd = os.getcwd()
contentdir = '1'
path = os.path.join(cwd,contentdir)

os.makedirs(path, exist_ok=True)

# Variabler för om filer ska inkluderas samt i vilka filformat (txt, pdf och docx)
includefiles = True
filformatlista = ['.pdf', '.docx', '.txt']

# Antal ärenden i paketet
antalarenden = 10

# Antal handlingar i varje ärende
antalhandlingar = 2


fornamnslista = ['Adam','Adrian','Albin','Alexander','Alfred','Algot','Ali','Alvar','Alve','Alvin','Anton','Aron','Arvid','Aston','August','Axel','Benjamin','Björn','Carl','Casper','Charlie','Colin','Daniel','Dante','Ebbe','Edvin','Elias','Elis','Elliot','Elton','Elvin','Emil','Erik','Felix','Filip','Folke','Frank','Frans','Gabriel','Gustav','Harry','Henry','Hjalmar','Hugo','Isak','Ivar','Jack','Jacob','Joel','Jonathan','Josef','Julian','Kian','Leo','Leon','Levi','Liam','Loke','Louie','Love','Lucas','Ludvig','Malte','Matteo','Max','Melker','Melvin','Milo','Milton','Mohammed','Nicholas','Nils','Noah','Noel','Oliver','Olle','Omar','Oscar','Otis','Otto','Sam','Samuel','Sigge','Sixten','Svante','Tage','Ted','Theo','Theodor','Ture','Vidar','Vide','Viggo','Viktor','Vilgot','Vincent','Walter','Wilhelm','William', 'Wilmer']
efternamnslista = ['ANDERSSON','JOHANSSON','KARLSSON','NILSSON','ERIKSSON','LARSSON','OLSSON','PERSSON','SVENSSON','GUSTAFSSON','PETTERSSON','JONSSON','JANSSON','HANSSON','BENGTSSON','JÖNSSON','LINDBERG','JAKOBSSON','MAGNUSSON','LINDSTRÖM','OLOFSSON','LINDQVIST','LINDGREN','BERG','AXELSSON','BERGSTRÖM','LUNDBERG','LIND','LUNDGREN','LUNDQVIST','MATTSSON','BERGLUND','FREDRIKSSON','SANDBERG','HENRIKSSON','ALI','FORSBERG','MOHAMED','SJÖBERG','WALLIN','ENGSTRÖM','EKLUND','DANIELSSON','LUNDIN','HÅKANSSON','BJÖRK','BERGMAN','GUNNARSSON','WIKSTRÖM','HOLM','SAMUELSSON','ISAKSSON','FRANSSON','BERGQVIST','NYSTRÖM','HOLMBERG','ARVIDSSON','LÖFGREN','SÖDERBERG','NYBERG','AHMED','BLOMQVIST','CLAESSON','NORDSTRÖM','HASSAN','MÅRTENSSON','LUNDSTRÖM','VIKLUND','BJÖRKLUND','ELIASSON','BERGGREN','PÅLSSON','SANDSTRÖM','NORDIN','LUND','FALK','STRÖM','ÅBERG','EKSTRÖM','HERMANSSON','HOLMGREN','DAHLBERG','HELLSTRÖM','HEDLUND','SUNDBERG','SJÖGREN','EK','BLOM','ABRAHAMSSON','ÖBERG','MARTINSSON','ANDREASSON','STRÖMBERG','MÅNSSON','HANSEN','ÅKESSON','DAHL','LINDHOLM','NORBERG', 'HOLMQVIST']
arendemeningforled = ['Svar på remiss avseende','Yttrande över','Synpunkt på','Upphandling av','Beslut kring','Beslut rörande','Ny policy rörande','Kommunens nya strategi för','Överklagande av beslut rörarande' 'Riktlinjer för', 'Anmälningsärende kring','Ny avsiktsförklaring för', 'Rapport rörande', 'Taxa för tillsyn över']
arendemeningobjekt = ['korvkiosk','adress','advokat','affär','afton','apelsin','apparat','arbetsplats','arm','ask','askkopp','avdelning','axel','bagare','bakelse','balkong','bana','banan','bandspelare','bar','barnskötare','berättelse','bil','bild','biljett','blomma','blus','bok','boll','brandman','brevlåda','bro','bulle','buss','bussförare','butik','båt','bänk','chaufför','check','cigarrett','citron','cykel','dag','dator','deltagare','diskbänk','diskmaskin','dotter','dräkt','duk','dusch','dörr','elefant','elev','expedit','fabrik','familj','far','farbror','fax','film','fisk','fjärrkontroll','flaska','flicka','fluga','flygplats','fläkt','fot','fotboll','fotbollspelare','frisör','fru','frukost','frukt','frys','fysiker','fågel','fåtölj','färg','förman','förmiddag','förälder','gaffel','gardin','gata','glass','gran','grönsak','gurka','hall','hamn','hand','handduk','handske','hatt','hund','hustru','hylla','hållplats']
handlingstyperlista = ['Beslut', 'Skrivelse', 'PM', 'Yttrande', 'Remiss', 'Tjänsteskrivelse', ]

# Dict för namespades
ns = {  'xsi' :"http://www.w3.org/2001/XMLSchema-instance",
        'xsd': "http://www.w3.org/2001/XMLSchema",
        'xlink': "http://www.w3.org/1999/xlink"}

# Skapar variabel för xsi:schemaLocation
schemaLocation = str(QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation"))

# Skapar rotelement
rotelement = etree.Element('Leveransobjekt', nsmap=ns)
rotelement.set('xmlns', 'http://xml.ra.se/e-arkiv/FGS-ERMS')
rotelement.set(schemaLocation, 'http://xml.ra.se/e-arkiv/FGS-ERMS Arendehantering.xsd')

#rotelement.set('xmlns', 'http://xml.ra.se/e-arkiv/FGS-ERMS')
#rotelement.set(schemaLocation, 'http://xml.ra.se/e-arkiv/FGS-ERMS Arendehantering.xsd')


xmlFile = etree.ElementTree(rotelement)
ArkivobjektListaArenden = etree.SubElement(rotelement, 'ArkivobjektListaArenden')




# Skapar ärende
for arenden in track(range(antalarenden), 'Genererar ärenden och filer'):
    #Skapar Random-variabler
    handlaggare = f'{random.choice(fornamnslista)} {random.choice(efternamnslista).capitalize()}'
    registrator = f'{random.choice(fornamnslista)} {random.choice(efternamnslista).capitalize()}'
    motpartagent = f'{random.choice(fornamnslista)} {random.choice(efternamnslista).capitalize()}'
    arendemeningtext = f'{random.choice(arendemeningforled)} {random.choice(arendemeningobjekt)}' 
    objektID = radar.random_datetime(start='2000-01-01T00:01:01', stop='2022-01-01T23:59:59').strftime('%Y') + '/GBG/' + str(random.randint(1,10000))
    


    ArkivobjektArende = etree.SubElement(ArkivobjektListaArenden, 'ArkivobjektArende')
    ArkivobjektArende.set('Systemidentifierare', str(uuid.uuid4()))

    ArkivobjektID = etree.SubElement(ArkivobjektArende, 'ArkivobjektID').text = objektID
    ArendeTyp = etree.SubElement(ArkivobjektArende, 'ArendeTyp')
    Avslutat = etree.SubElement(ArkivobjektArende, 'Avslutat').text = radar.random_datetime(start='2000-01-01T00:01:01', stop='2022-01-01T23:59:59').strftime('%Y-%m-%dT%H:%M:%S')
    Gallring = etree.SubElement(ArkivobjektArende, 'Gallring')
    Gallring.set('Gallras', 'false')

    # Handläggare
    Agent1 = etree.SubElement(ArkivobjektArende, 'Agent')
    Roll = etree.SubElement(Agent1, 'Roll').text = 'Handläggare'
    Namn= etree.SubElement(Agent1, 'Namn').text = handlaggare
    Organisationsnamn = etree.SubElement(Agent1, 'Organisationsnamn').text = 'Göteborgs Stad'
    Enhentsnamn = etree.SubElement(Agent1, 'Enhetsnamn').text = 'Enheten'
    
    # Registrator
    Agent2 = etree.SubElement(ArkivobjektArende, 'Agent')
    Roll = etree.SubElement(Agent2, 'Roll').text = 'Registrator'
    Namn = etree.SubElement(Agent2, 'Namn').text = registrator
    Organisationsnamn = etree.SubElement(Agent2, 'Organisationsnamn').text = 'Göteborgs Stad'
    Enhetsnamn = etree.SubElement(Agent2, 'Enhetsnamn').text = 'Enheten'
    
    Klass = etree.SubElement(ArkivobjektArende, 'Klass')
    
    # Motpart
    Motpart = etree.SubElement(ArkivobjektArende, 'Motpart')
    Namn = etree.SubElement(Motpart, 'Namn').text = motpartagent
    Organisation = etree.SubElement(Motpart, 'Organisation')

    SistaAnvandandetidpunkt = etree.SubElement(ArkivobjektArende, 'SistaAnvandandetidpunkt').text =  radar.random_datetime(start='2000-01-01T00:01:01', stop='2022-01-01T23:59:59').strftime('%Y-%m-%dT%H:%M:%S')
    Skapad = etree.SubElement(ArkivobjektArende, 'Skapad').text = radar.random_datetime(start='2000-01-01T00:01:01', stop='2022-01-01T23:59:59').strftime('%Y-%m-%dT%H:%M:%S')
    Inkommen = etree.SubElement(ArkivobjektArende, 'Inkommen').text = radar.random_datetime(start='2000-01-01T00:01:01', stop='2022-01-01T23:59:59').strftime('%Y-%m-%dT%H:%M:%S')
    StatusArande = etree.SubElement(ArkivobjektArende, 'StatusArande').text = 'Stängt'
    Arendemening = etree.SubElement(ArkivobjektArende, 'Arendemening').text = arendemeningtext
    ArkivobjektListaHandlingar = etree.SubElement(ArkivobjektArende, 'ArkivobjektListaHandlingar')
    
    # Loopa genom handlingar -- Lägg till Random!
    for handlingar in range(antalhandlingar):
        # Varibler för värden
        handlingstypsvarde = random.choice(handlingstyperlista)
        handlingsID = objektID +'-'+ str(handlingar + 1)

        # Skapar element och attribut
        ArkivobjektHandling = etree.SubElement(ArkivobjektListaHandlingar, 'ArkivobjektHandling')
        ArkivobjektHandling.set("Systemidentifierare", str(uuid.uuid4()))
        ArkivobjektID = etree.SubElement(ArkivobjektHandling, 'ArkivobjektID').text = handlingsID
        Handlingstyp = etree.SubElement(ArkivobjektHandling, 'Handlingstyp').text = handlingstypsvarde
        
        if (handlingar + 1) == True:
            Avsandare = etree.SubElement(ArkivobjektHandling, 'Avsandare')
            AvsandareNamn = etree.SubElement(Avsandare, 'Namn').text = f'{random.choice(fornamnslista)} {random.choice(efternamnslista).capitalize()}'        
        
        Beskrivning = etree.SubElement(ArkivobjektHandling, 'Beskrivning')
        
        if (handlingar + 1) != True:
            Expedierad = etree.SubElement(ArkivobjektHandling, 'Expedierad').text = radar.random_datetime(start='2000-01-01T00:01:01', stop='2022-01-01T23:59:59').strftime('%Y-%m-%dT%H:%M:%S')
        
        Gallring = etree.SubElement(ArkivobjektHandling, 'Gallring')
        Gallring.set("Gallras", 'false')

        # Handläggare
        Agent1 = etree.SubElement(ArkivobjektHandling, 'Agent')
        Roll = etree.SubElement(Agent1, 'Roll').text = 'Handläggare'
        Namn= etree.SubElement(Agent1, 'Namn').text = handlaggare
        Organisationsnamn = etree.SubElement(Agent1, 'Organisationsnamn').text = 'Göteborgs Stad'
        Enhentsnamn1 = etree.SubElement(Agent1, 'Enhetsnamn').text = 'Enheten'
    
        # Registrator
        Agent2 = etree.SubElement(ArkivobjektHandling, 'Agent')
        Roll = etree.SubElement(Agent2, 'Roll').text = 'Registrator'
        Namn = etree.SubElement(Agent2, 'Namn').text = registrator
        Organisationsnamn = etree.SubElement(Agent2, 'Organisationsnamn').text = 'Göteborgs Stad'
        Enhetsnamn = etree.SubElement(Agent2, 'Enhetsnamn').text = 'Enheten'
        
        if (handlingar + 1) == True:
            Inkommen = etree.SubElement(ArkivobjektHandling, 'Inkommen').text = radar.random_datetime(start='2000-01-01T00:01:01', stop='2022-01-01T23:59:59').strftime('%Y-%m-%dT%H:%M:%S')
            
        Lopnummer = etree.SubElement(ArkivobjektHandling, 'Lopnummer').text = str(handlingar + 1)

        if (handlingar + 1) != True:
            Mottagare = etree.SubElement(ArkivobjektHandling, 'Mottagare')        
            MottagareNamn = etree.SubElement(Mottagare, 'Namn').text = f'{random.choice(fornamnslista)} {random.choice(efternamnslista).capitalize()}'        

        #Rubrik = etree.SubElement(ArkivobjektHandling, 'Rubrik')
        Skapad = etree.SubElement(ArkivobjektHandling, 'Skapad').text = radar.random_datetime(start='2000-01-01T00:01:01', stop='2022-01-01T23:59:59').strftime('%Y-%m-%dT%H:%M:%S')
        SistaAnvandandetidpunkt = etree.SubElement(ArkivobjektHandling, 'SistaAnvandandetidpunkt').text = radar.random_datetime(start='2000-01-01T00:01:01', stop='2022-01-01T23:59:59').strftime('%Y-%m-%dT%H:%M:%S')

        if (handlingar + 1) == True:
            StatusHandling= etree.SubElement(ArkivobjektHandling, 'StatusHandling').text = "Inkommen"        
        else:
            StatusHandling= etree.SubElement(ArkivobjektHandling, 'StatusHandling').text = "Expedierad"        
        
        # Plockar ett random filformat för att skapa fil.
        filformat = random.choice(filformatlista)
    
        # Skapar filerna
        if includefiles:
            bokstaver = string.ascii_lowercase
            match filformat:
                case '.txt':
                    filenamebara = ''.join(random.choice(bokstaver) for i in range(10)) + '.txt'
                    filename = os.path.join(path,filenamebara)
                    textfile = open(filename, 'w')
                    textfile.write(''.join(random.choice(bokstaver) for i in range(10000)))
                    textfile.close
                case '.docx':
                    filenamebara= ''.join(random.choice(bokstaver) for i in range(10)) + '.docx'
                    filename = os.path.join(path,filenamebara)
                    docxfilen= Document()
                    sentence = ''.join(random.choice(bokstaver) for i in range(100))
                    docxfilen.add_paragraph(sentence)
                    docxfilen.save(filename)
                case '.pdf':
                    filenamebara = ''.join(random.choice(bokstaver) for i in range(10)) + '.pdf'
                    filename = os.path.join(path,filenamebara)
                    pdffilen = canvas.Canvas(filename)
                    sentence = ''.join(random.choice(bokstaver) for i in range(100))
                    pdffilen.drawString(100, 750, sentence)
                    pdffilen.save()
                case _:
                    print('FEL')
                    break
        
            # Genererar checksumma
            with open(filename, "rb") as f:
                fileHash = hashlib.sha256()
                while bits := f.read(8192):
                    fileHash.update(bits)
            hashValue = fileHash.hexdigest()
            f.close

        # Lägger till metatdata för Bilaga
            Bilaga = etree.SubElement(ArkivobjektHandling, 'Bilaga')
            Bilaga.set('Namn',filenamebara)
            Bilaga.set('Lank',f'Content/1/{filenamebara}')
            Bilaga.set('Storlek', str(os.stat(filename).st_size))
            Bilaga.set('Mimetyp', mimetypes.guess_type(filename)[0])
            Bilaga.set('Checksumma', hashValue)
            Bilaga.set('ChecksummaMetod','SHA256')

#Skriver xml-filen
xmlFile.write(f'content.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)


fgsPackage = FGSBuddyLight.FgsMaker()
fgsPackage.inputValues()
fgsPackage.collectFiles(fgsPackage.pathToFiles, fgsPackage.subfolders)
fgsPackage.createSip()
fgsPackage.createFgsPackage(cwd)

