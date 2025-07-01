import traceback
import xml.etree.cElementTree as ET
import csv
from datetime import date, datetime
from recupero_log import log_summary
import xml.etree.ElementTree as Xet
import os

def flussoG02duereti():
    try:
        basepath = r'\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\duereti\4-Registrati'
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                name = entry
        xmlparse = Xet.parse(r'\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\duereti\4-Registrati\\' + name)
        root = xmlparse.getroot()
        rows = []
        for i in root:
            CODICE_RICHIESTA = i.find("CODICE_RICHIESTA").text
            CODICE_RINTRACCIABILITA = i.find("CODICE_RINTRACCIABILITA").text
            CODICE_SAPR = i.find("CODICE_SAPR").text
            STATO_OPERATIVO = i.find("STATO_OPERATIVO").text
            STATO_IMPIANTO = i.find("STATO_IMPIANTO").text
            DATA_CONVALIDA = i.find("DATA_CONVALIDA").text
            VERSIONE_ATTESTATO = i.find("VERSIONE_ATTESTATO").text
            TIPO_TECNOLOGIA = i.find("TIPO_TECNOLOGIA").text
            NOMEIMP = i.find("NOMEIMP").text
            COD_ISTAT_COMUNE = i.find("COD_ISTAT_COMUNE").text
            LOCALITA = i.find("LOCALITA").text
            INDIRIZZO = i.find("INDIRIZZO").text
            CAP = i.find("CAP").text
            PARTITA_IVA_PROD = i.find("PARTITA_IVA_PROD").text
            CODICE_FISCALE_PROD = i.find("CODICE_FISCALE_PROD").text
            CODICE_ISTAT_PROD = i.find("CODICE_ISTAT_PROD").text
            EMAIL_PROD = i.find("EMAIL_PROD").text
            TENSIONE_COLL_RETE = i.find('SEZIONE')[0].text
            POTENZA_ATTIVA_NOMINALE = i.find('SEZIONE')[1].text

            POTENZA_INVERTER = i.find('SEZIONE')[2].text
            CODICE_POD = i.find('SEZIONE')[3].text
            REGIME_COMMERCIALE = i.find('SEZIONE')[4].text


            rows.append((list(i.attrib.values())[0],
                         CODICE_RICHIESTA,
                         CODICE_RINTRACCIABILITA,
                         CODICE_SAPR,
                         STATO_OPERATIVO,
                         STATO_IMPIANTO,
                         DATA_CONVALIDA,
                         VERSIONE_ATTESTATO,
                         TIPO_TECNOLOGIA,
                         NOMEIMP,
                         COD_ISTAT_COMUNE,
                         LOCALITA,
                         INDIRIZZO,
                         CAP,
                         PARTITA_IVA_PROD,
                         CODICE_FISCALE_PROD,
                         CODICE_ISTAT_PROD,
                         EMAIL_PROD,
                         TENSIONE_COLL_RETE,
                         POTENZA_ATTIVA_NOMINALE,
                         POTENZA_INVERTER,
                         CODICE_POD,
                         REGIME_COMMERCIALE))
        with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\duereti\\G12\\G12.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            root = ET.Element("VALIDA_IMPIANTI", COD_SERVIZIO="G02", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                              GESTORE_PIVA="13632560960")

            print("-------------------------------G02--------------------------------------")

            for row in csv_reader:

                print(row[7])
                if line_count == 0:
                    pass
                else:
                    for item in rows:
                        if item[2] == row[7]:
                            doc = ET.SubElement(root, "IMPIANTO", CODICE=item[0], TIPO_OPERAZIONE="V")
                            VERSIONE_ATTESTATO = '1'
                            FLAG_CONNESSIONE_CONDIVISA = 'N'
                            MOTIVAZIONE_RIGETTO = ''
                            CODICE_RINTRACCIABILITA = item[2]
                            CODICE_SCARTO = '000'

                            ET.SubElement(doc, "VERSIONE_ATTESTATO").text = str(VERSIONE_ATTESTATO)
                            ET.SubElement(doc, "FLAG_CONNESSIONE_CONDIVISA").text = str(FLAG_CONNESSIONE_CONDIVISA)
                            ET.SubElement(doc, "MOTIVAZIONE_RIGETTO").text = str(MOTIVAZIONE_RIGETTO)
                            ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = str(CODICE_RINTRACCIABILITA)
                            ET.SubElement(doc, "CODICE_SCARTO").text = str(CODICE_SCARTO)

                            # tree = ET.ElementTree(root)
                            # tree.write(f"C:\\ImpiantiTerna\\G01\\G1_{row[0]}.xml")
                            #log(row[0], row)
                tree = ET.ElementTree(root)
                            # tree.write(f"C:\\ImpiantiTerna\\G02\\G02_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml")
                tree.write(
                    f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\duereti\\G02_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
                    short_empty_elements=False)





                line_count += 1
    except Exception as e:
        print(e)
        traceback.print_exc()





def log(preventivo, row):
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"C:\\ImpiantiTerna\\G02\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()




#log_summary('G02')
