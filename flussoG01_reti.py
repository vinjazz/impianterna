import sqlite3
import xml.etree.cElementTree as ET
import csv
from datetime import date, datetime
from recupero_log import log_summary

def flussoG01Reti():
    try:
        with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\reti+\\G01\\G01.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            root = ET.Element("GESTIONE_POD", COD_SERVIZIO="G01", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                              GESTORE_PIVA="04152790962")

            for row in csv_reader:

                if line_count == 0:

                    pass
                else:

                    CODICE_RINTACCIABILITA = row[0]
                    POD = row[1]
                    POTENZA_IMMISSIONE_KW = row[2].replace(',', '.')
                    POTENZA_PRELIEVO_KW = row[3].replace(',', '.')
                    PUNTO_DI_SOLA_IMMISSIONE = row[4]
                    SSPC_TIPOLOGIA_DICHIARATA = row[5]
                    TIPO_CONNESSIONE = row[6]
                    LIVELLO_TENSIONE = row[7]
                    TIPO_ITER = row[8]


                    doc = ET.SubElement(root, "POD", CODICE= POD, TIPO_OPERAZIONE= "U")
                    ET.SubElement(doc, "POTENZA_IMMISSIONE_KW").text = str(POTENZA_IMMISSIONE_KW)
                    ET.SubElement(doc, "POTENZA_PRELIEVO_KW").text = str(POTENZA_PRELIEVO_KW)
                    ET.SubElement(doc, "LIVELLO_TENSIONE_V").text = str(LIVELLO_TENSIONE)
                    ET.SubElement(doc, "PUNTO_DI_SOLA_IMMISSIONE").text = str(PUNTO_DI_SOLA_IMMISSIONE)
                    ET.SubElement(doc, "TIPO_IMMISSIONE").text = str(TIPO_CONNESSIONE)
                    ET.SubElement(doc, "CABINA_PRIMARIA").text = None
                    ET.SubElement(doc, "SSPC_TIPOLOGIA_RICHIESTA").text = str(SSPC_TIPOLOGIA_DICHIARATA)
                    ET.SubElement(doc, "SSPC_TIPOLOGIA_POD").text = "P"
                    ET.SubElement(doc, "SSPC_POD_ASSOCIATO")
                    ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = str(CODICE_RINTACCIABILITA)
                    ET.SubElement(doc, "TIPO_ITER").text = str(TIPO_ITER)
                    # tree = ET.ElementTree(root)
                    # tree.write(f"C:\\ImpiantiTerna\\G01\\G1_{row[0]}.xml")
                    log(row[0], row)
                    print(row[0])
                line_count += 1
    except Exception as e:
        print(e)

    tree = ET.ElementTree(root)
    #tree.write(f"C:\\ImpiantiTerna\\G01\\G01_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml")
    tree.write(
        f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\reti+\\G01_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
        short_empty_elements=False)


def log(preventivo, row):
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\reti+\\G01\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()

#flussoG01New()
# log_summary('G01')