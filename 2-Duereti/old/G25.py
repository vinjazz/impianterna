import xml.etree.cElementTree as ET
import csv
from datetime import date, datetime

def log(preventivo, row):
    try:
        line = f'{date.today()};{preventivo}'
        file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G25\\Log\\{preventivo}.csv", "w")
        file_uno.write(line)
        for data in row:
            file_uno.write(f"\n {data};")
        file_uno.close()
    except Exception as e:
        print(e)

def flussoG25():
    try:
        with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G25\\G25.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            root = ET.Element("COMUNICAZIONE_UNICA", COD_SERVIZIO="G25", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                              GESTORE_PIVA="13632560960")

            for row in csv_reader:
                print(row)
                if line_count == 0:
                    pass
                else:
                    log(row[4],row)
                    CODICE_POD = row[0]
                    POTENZA_IMMISSIONE_KW = row[1].replace(',', '.')
                    POTENZA_PRELIEVO_KW = row[2].replace(',', '.')
                    LIVELLO_TENSIONE_V = row[3]
                    CODICE_RINTRACCIABILITA = row[4]
                    INDIRIZZO_IMP = row[5]
                    CAP_IMP = row[6]
                    COD_ISTAT_IMP = row[7]
                    SOTTOTIPO_TECNOLOGIA_IMP = row[8]
                    INDIRIZZO_PROD = row[9]
                    RAG_SOC_PROD = row[10]
                    PIVA_CFIS_PROD = row[11]
                    TELEFONO_PROD = row[12]
                    CELLULARE_PROD = row[13]
                    EMAIL_PROD = row[14]
                    CAP_PROD = row[15]
                    COD_ISTAT_PROD = row[16]
                    DICHIARAZIONE_ACC = row[17]
                    POT_ATTIVA_NOMINALE_SEZ = row[18].replace(',', '.')
                    POT_ATTIVA_INVERTER_SEZ = row[19].replace(',', '.')
                    if row[17] == '2':
                        TIPO_INSTALLAZIONE_ACC = row[20]
                    else:
                        TIPO_INSTALLAZIONE_ACC = ''
                    if row[17] == '2':
                        TIPO_TECNOLOGIA_ACC = row[21]
                    else:
                        TIPO_TECNOLOGIA_ACC = ''
                    if row[17] == '2':
                        SOTTOTIPO_TECNOLOGIA_ACC = row[22]
                    else:
                        SOTTOTIPO_TECNOLOGIA_ACC = ''
                    if row[17] == '2':
                        MODELLO_ACC = row[23]
                    else:
                        MODELLO_ACC = 'N.D.'

                    if row[17] == '2':
                        COSTRUTTORE_ACC = row[23]
                    else:
                        COSTRUTTORE_ACC = 'N.D.'

                    ALIMENTAZIONE_IMPIANTO = row[25]
                    ALIMENTAZIONE_RETE = row[26]
                    FLAG_CC_CA_ACC = row[27]
                    if row[17] == '2':
                        CAPACITA_NOMINALE_ACC = row[28]
                    else:
                        CAPACITA_NOMINALE_ACC = ''
                    if row[17] == '2':
                        POT_NOMINALE_ASSORBIMENTO_ACC = row[29].replace(',', '.')
                    else:
                        POT_NOMINALE_ASSORBIMENTO_ACC = ''
                    if row[17] == '2':
                        POT_ATTIVA_NOMINALE_RILASCIO_ACC = row[30].replace(',', '.')
                    else:
                        POT_ATTIVA_NOMINALE_RILASCIO_ACC = ''
                    if row[17] == '2':
                        POT_APPARENTE_NOMINALE_ACC = row[31].replace(',', '.')
                    else:
                        POT_APPARENTE_NOMINALE_ACC = ''
                    if row[17] == '2':
                        POT_ATTIVA_INVERTER_ACC = row[32].replace(',', '.')
                    else:
                        POT_ATTIVA_INVERTER_ACC = ''
                    if row[17] == '2':
                        TENSIONE_NOMINALE_ACC = row[33].replace(',', '.')
                    else:
                        TENSIONE_NOMINALE_ACC = ''

                    DATA_ATTIVAZIONE_CONNESSIONE = row[34]
                    TIPO_TECNOLOGIA_GENERATORE = row[35]
                    NUM_AEROGENERATORI = row[36]
                    ALTEZZA_MEDIA_AEROGENERATORI = row[37]
                    DIAMETRO_ROTORI = row[38]
                    POTENZA_AEROGENERATORI = row[39]
                    VELOCITA_NOMINALE = row[40]

                    doc = ET.SubElement(root, "IMPIANTO")
                    ET.SubElement(doc, "CODICE_POD").text = str(CODICE_POD)
                    ET.SubElement(doc, "POTENZA_IMMISSIONE_KW").text = str(POTENZA_IMMISSIONE_KW)
                    ET.SubElement(doc, "POTENZA_PRELIEVO_KW").text = str(POTENZA_PRELIEVO_KW)
                    ET.SubElement(doc, "LIVELLO_TENSIONE_V").text = str(LIVELLO_TENSIONE_V)
                    ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = str(CODICE_RINTRACCIABILITA)
                    ET.SubElement(doc, "INDIRIZZO_IMP").text = str(INDIRIZZO_IMP)
                    ET.SubElement(doc, "CAP_IMP").text = str(CAP_IMP)
                    ET.SubElement(doc, "COD_ISTAT_IMP").text = str(COD_ISTAT_IMP)
                    ET.SubElement(doc, "SOTTOTIPO_TECNOLOGIA_IMP").text = str(SOTTOTIPO_TECNOLOGIA_IMP)
                    ET.SubElement(doc, "INDIRIZZO_PROD").text = str(INDIRIZZO_PROD)
                    ET.SubElement(doc, "RAG_SOC_PROD").text = str(RAG_SOC_PROD)
                    ET.SubElement(doc, "PIVA_CFIS_PROD").text = str(PIVA_CFIS_PROD)
                    ET.SubElement(doc, "TELEFONO_PROD").text = str(TELEFONO_PROD)
                    ET.SubElement(doc, "CELLULARE_PROD").text = str(CELLULARE_PROD)
                    ET.SubElement(doc, "EMAIL_PROD").text = str(EMAIL_PROD)
                    ET.SubElement(doc, "CAP_PROD").text = str(CAP_PROD)
                    ET.SubElement(doc, "COD_ISTAT_PROD").text = str(COD_ISTAT_PROD)
                    ET.SubElement(doc, "DICHIARAZIONE_ACC").text = str(DICHIARAZIONE_ACC)
                    ET.SubElement(doc, "POT_ATTIVA_NOMINALE_SEZ").text = str(POT_ATTIVA_NOMINALE_SEZ)
                    ET.SubElement(doc, "POT_ATTIVA_INVERTER_SEZ").text = str(POT_ATTIVA_INVERTER_SEZ)
                    ET.SubElement(doc, "TIPO_INSTALLAZIONE_ACC").text = str(TIPO_INSTALLAZIONE_ACC)
                    ET.SubElement(doc, "TIPO_TECNOLOGIA_ACC").text = str(TIPO_TECNOLOGIA_ACC)
                    ET.SubElement(doc, "SOTTOTIPO_TECNOLOGIA_ACC").text = str(SOTTOTIPO_TECNOLOGIA_ACC)
                    ET.SubElement(doc, "MODELLO_ACC").text = str(MODELLO_ACC)
                    ET.SubElement(doc, "COSTRUTTORE_ACC").text = str(COSTRUTTORE_ACC)
                    ET.SubElement(doc, "ALIMENTAZIONE_IMPIANTO").text = str(ALIMENTAZIONE_IMPIANTO)
                    ET.SubElement(doc, "ALIMENTAZIONE_RETE").text = str(ALIMENTAZIONE_RETE)
                    ET.SubElement(doc, "FLAG_CC_CA_ACC").text = str(FLAG_CC_CA_ACC)
                    ET.SubElement(doc, "CAPACITA_NOMINALE_ACC").text = str(CAPACITA_NOMINALE_ACC)
                    ET.SubElement(doc, "POT_NOMINALE_ASSORBIMENTO_ACC").text = str(POT_NOMINALE_ASSORBIMENTO_ACC)
                    ET.SubElement(doc, "POT_ATTIVA_NOMINALE_RILASCIO_ACC").text = str(POT_ATTIVA_NOMINALE_RILASCIO_ACC)
                    ET.SubElement(doc, "POT_APPARENTE_NOMINALE_ACC").text = str(POT_APPARENTE_NOMINALE_ACC)
                    ET.SubElement(doc, "POT_ATTIVA_INVERTER_ACC").text = str(POT_ATTIVA_INVERTER_ACC)
                    ET.SubElement(doc, "TENSIONE_NOMINALE_ACC").text = str(TENSIONE_NOMINALE_ACC)
                    ET.SubElement(doc, "DATA_ATTIVAZIONE_CONNESSIONE").text = str(DATA_ATTIVAZIONE_CONNESSIONE)
                    ET.SubElement(doc, "TIPO_TECNOLOGIA_GENERATORE").text = str(TIPO_TECNOLOGIA_GENERATORE)
                    ET.SubElement(doc, "NUM_AEROGENERATORI").text = str(NUM_AEROGENERATORI)
                    ET.SubElement(doc, "ALTEZZA_MEDIA_AEROGENERATORI").text = str(ALTEZZA_MEDIA_AEROGENERATORI)
                    ET.SubElement(doc, "DIAMETRO_ROTORI").text = str(DIAMETRO_ROTORI)
                    ET.SubElement(doc, "POTENZA_AEROGENERATORI").text = str(POTENZA_AEROGENERATORI)
                    ET.SubElement(doc, "VELOCITA_NOMINALE").text = str(VELOCITA_NOMINALE)

                line_count += 1


    except Exception as e:
        print(e)

    tree = ET.ElementTree(root)
    tree.write(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G025_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml")


flussoG25()