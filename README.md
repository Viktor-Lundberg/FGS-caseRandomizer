# FGS-caseRandomizer
Verktyg för att skapa SIP-paket till ett e-arkiv med slumpmässiga ärenden, handlingar och filer i enlighet med FGS ärendehantering.
Kan exempelvis användas för att testa funktionalitet eller göra kontroller av ett e-arkivsystem alternativt för att skapa "dummy-data" till e-arkivet som kan visas upp externt utan att man behöver vara orolig för att röja personuppgifter eller sekretess.

### ANVÄNDNING
* Lägg filerna "casecreator.py, FGSBuddyLight.py och Arendehantering.xsd" i en tom katalog.
* Öppna filen casecreator.py om du vill ändra några inställningar. Variabeln "includefiles" (True/False) anger om skriptet ska skapa filer till FGS-paketet. I "filformatlista" anges vilka filformat som ska genereras i paketet (.pdf, .txt och/eller .docx). Variabeln "antalarenden" anger hur många ärenden paketet ska innehålla medan "antalhandlingar" anger hur många handlingar som ska skapas i respektive ärende.
* Om man vill ändra Arkivbildare och producerande system etc för Sip.xml görs detta i FGSBuddyLight.py i funktionen "def inputValues".
* När inställningarna är färdiga kör "casecreator.py" för att generera SIP-paketet.
* Om nytt paket ska skapas måste katalogen rensas från alla filer/mappar utom "casecreator.py, FGSBuddyLight.py och Arendehantering.xsd"


### Output
* Ett FGS-paket "FGS_Package_{YYYY}_{MM}_{DD}T{HH}_{Min}_{SS}.zip" i cwd.
* Strukturen i paketet är:
* NIVÅ1 = Sip.xml, Content
* NIVÅ2 = Arendehantering.xsd, content.xml, 1 
* NIVÅ3 = file1.pdf, file2.docx, file3,txt osv.
