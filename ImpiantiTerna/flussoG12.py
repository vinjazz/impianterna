import xml.etree.cElementTree as ET
import csv
import traceback
from datetime import date, datetime


def flussoG12New():
    try:
        with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\G12\\G12.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            root = ET.Element("CARICA_IMPIANTO", COD_SERVIZIO="G12", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                              GESTORE_PIVA="12883450152")
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    print(row)
                    NOME_IMP = row[0]
                    INDIRIZZO_IMP = row[1]
                    CAP_IMP = row[2]
                    COD_ISTAT_IMP = row[3]
                    TIPO_TECNOLOGIA_IMP = row[4]
                    SOTTOTIPO_TECNOLOGIA_IMP = row[5]
                    FLAG_GSE = row[6]
                    CODICE_RINTRACCIABILITA = row[7]
                    INDIRIZZO_PROD = row[8]
                    RAG_SOC_PROD = row[9]
                    PIVA_CFIS_PROD = row[10]
                    TELEFONO_PROD = row[11]
                    CELLULARE_PROD = row[12]
                    EMAIL_PROD = row[13]
                    CAP_PROD = row[14]

                    if len(row[15]) == 6:
                        COD_ISTAT_PROD = row[15]
                    else:
                        COD_ISTAT_PROD = row[15][1:]
                        print(row[15][1:])
                    DICHIARAZIONE_ACC = row[16]
                    NUMERO_SEZIONE = row[17]
                    INCENTIVO = row[18]
                    REGIME_COMMERCIALE = row[19]
                    TIPO_TECNOLOGIA_SEZ = row[20]
                    SOTTOTIPO_TECNOLOGIA_SEZ = row[21]
                    TIPO_ISTANZA = row[22]
                    PIVA_CFIS_UDDI = row[23]
                    CODICE_POD_SEZ = row[24]
                    LIVELLO_TENSIONE_SEZ = row[25]
                    POT_DI_PICCO_SEZ = row[26].replace(',', '.')
                    POT_APPARENTE_NOMINALE_SEZ = row[27]
                    PROD_ANNUA_LORDA_SEZ = row[28]
                    FATTORE_POTENZA_NOMINALE_SEZ = row[29]
                    POT_ATTIVA_NOMINALE_SEZ = row[30].replace(',', '.')
                    POT_ATTIVA_INVERTER_SEZ = row[31].replace(',', '.')
                    TENSIONE_NOMINALE = row[32].replace(',', '.')
                    POT_EFF_LORDA = row[33].replace(',', '.')
                    POT_EFF_NETTA = row[34].replace(',', '.')
                    MARCA_UNITA_MCOGEN = row[35]
                    MODELLO_UNITA_MCOGEN = row[36]
                    POTENZA_TERMICA_MCOGEN = row[37]
                    POTENZA_IMMESSA_MCOGEN = row[38]
                    PROD_IMMESSA_IN_RETE_SEZ = row[39]
                    if row[16] == '2':
                        TIPO_INSTALLAZIONE_ACC = row[40]
                    else:
                        TIPO_INSTALLAZIONE_ACC = ''
                    if row[16] == '2':
                        TIPO_TECNOLOGIA_ACC = row[41]
                    else:
                        TIPO_TECNOLOGIA_ACC = ''
                    if row[16] == '2':
                        SOTTOTIPO_TECNOLOGIA_ACC = row[42]
                    else:
                        SOTTOTIPO_TECNOLOGIA_ACC = ''
                    if row[16] == '2':
                        MODELLO_ACC = row[43]
                    else:
                        MODELLO_ACC = 'N.D.'
                    if row[16] == '2':
                        COSTRUTTORE_ACC = row[44]
                    else:
                        COSTRUTTORE_ACC = 'N.D.'

                    ALIMENTAZIONE_IMPIANTO = row[45]
                    ALIMENTAZIONE_RETE = row[46]
                    FLAG_CC_CA_ACC = row[47]
                    try:
                        POT_NOMINALE_ASSORBIMENTO_ACC = row[48].replace(',', '.')
                    except AttributeError:
                        POT_NOMINALE_ASSORBIMENTO_ACC = ''
                    try:
                        POT_ATTIVA_NOMINALE_RILASCIO_ACC = row[49].replace(',', '.')
                    except AttributeError:
                        POT_ATTIVA_NOMINALE_RILASCIO_ACC = ''
                    try:
                        POT_APPARENTE_NOMINALE_ACC = row[50].replace(',', '.')
                    except AttributeError:
                        POT_APPARENTE_NOMINALE_ACC = ''
                    if row[47] == 'C':
                        POT_ATTIVA_INVERTER_ACC = ''
                    else:
                        POT_ATTIVA_INVERTER_ACC = row[51].replace(',', '.')
                    try:
                        TENSIONE_NOMINALE_ACC =row[52].replace(',', '.')
                    except AttributeError:
                        TENSIONE_NOMINALE_ACC = ''
                    try:
                        CAPACITA_NOMINALE_ACC = row[53].replace(',', '.')
                    except AttributeError:
                        CAPACITA_NOMINALE_ACC = ''
                    try:
                        CAPACITA_UTILIZZATA_MASSIMA_ACC = row[54].replace(',', '.')
                    except AttributeError:
                        CAPACITA_UTILIZZATA_MASSIMA_ACC = ''

                    doc = ET.SubElement(root, "IMPIANTO")
                    ET.SubElement(doc, "NOME_IMP").text = str(NOME_IMP)
                    ET.SubElement(doc, "INDIRIZZO_IMP").text = str(INDIRIZZO_IMP)
                    ET.SubElement(doc, "CAP_IMP").text = str(CAP_IMP)
                    ET.SubElement(doc, "COD_ISTAT_IMP").text = str(COD_ISTAT_IMP)
                    ET.SubElement(doc, "TIPO_TECNOLOGIA_IMP").text = str(TIPO_TECNOLOGIA_IMP)
                    ET.SubElement(doc, "SOTTOTIPO_TECNOLOGIA_IMP").text = str(SOTTOTIPO_TECNOLOGIA_IMP)
                    ET.SubElement(doc, "FLAG_GSE").text = str(FLAG_GSE)
                    ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = str(CODICE_RINTRACCIABILITA)
                    ET.SubElement(doc, "INDIRIZZO_PROD").text = str(INDIRIZZO_PROD)
                    ET.SubElement(doc, "RAG_SOC_PROD").text = str(RAG_SOC_PROD)
                    ET.SubElement(doc, "PIVA_CFIS_PROD").text = str(PIVA_CFIS_PROD)
                    ET.SubElement(doc, "TELEFONO_PROD").text = str(TELEFONO_PROD)
                    ET.SubElement(doc, "CELLULARE_PROD").text = str(CELLULARE_PROD)
                    ET.SubElement(doc, "EMAIL_PROD").text = str(EMAIL_PROD)
                    ET.SubElement(doc, "CAP_PROD").text = str(CAP_PROD)
                    ET.SubElement(doc, "COD_ISTAT_PROD").text = str(COD_ISTAT_PROD)
                    ET.SubElement(doc, "DICHIARAZIONE_ACC").text = str(DICHIARAZIONE_ACC)
                    ET.SubElement(doc, "NUMERO_SEZIONE").text = str(NUMERO_SEZIONE)
                    ET.SubElement(doc, "INCENTIVO").text = str(INCENTIVO)
                    ET.SubElement(doc, "REGIME_COMMERCIALE").text = str(REGIME_COMMERCIALE)
                    ET.SubElement(doc, "TIPO_TECNOLOGIA_SEZ").text = str(TIPO_TECNOLOGIA_SEZ)
                    ET.SubElement(doc, "SOTTOTIPO_TECNOLOGIA_SEZ").text = str(SOTTOTIPO_TECNOLOGIA_SEZ)
                    ET.SubElement(doc, "TIPO_ISTANZA").text = str(TIPO_ISTANZA)
                    ET.SubElement(doc, "PIVA_CFIS_UDDI").text = str(PIVA_CFIS_UDDI)
                    ET.SubElement(doc, "CODICE_POD_SEZ").text = str(CODICE_POD_SEZ)
                    ET.SubElement(doc, "LIVELLO_TENSIONE_SEZ").text = str(LIVELLO_TENSIONE_SEZ)
                    ET.SubElement(doc, "POT_DI_PICCO_SEZ").text = str(POT_DI_PICCO_SEZ)
                    ET.SubElement(doc, "POT_APPARENTE_NOMINALE_SEZ").text = str(POT_APPARENTE_NOMINALE_SEZ)
                    ET.SubElement(doc, "PROD_ANNUA_LORDA_SEZ").text = str(PROD_ANNUA_LORDA_SEZ)
                    ET.SubElement(doc, "FATTORE_POTENZA_NOMINALE_SEZ").text = str(FATTORE_POTENZA_NOMINALE_SEZ)
                    ET.SubElement(doc, "POT_ATTIVA_NOMINALE_SEZ").text = str(POT_ATTIVA_NOMINALE_SEZ)
                    ET.SubElement(doc, "POT_ATTIVA_INVERTER_SEZ").text = str(POT_ATTIVA_INVERTER_SEZ)
                    ET.SubElement(doc, "TENSIONE_NOMINALE").text = str(TENSIONE_NOMINALE)
                    ET.SubElement(doc, "POT_EFF_LORDA").text = str(POT_EFF_LORDA)
                    ET.SubElement(doc, "POT_EFF_NETTA").text = str(POT_EFF_NETTA)
                    ET.SubElement(doc, "MARCA_UNITA_MCOGEN").text = str(MARCA_UNITA_MCOGEN)
                    ET.SubElement(doc, "MODELLO_UNITA_MCOGEN").text = str(MODELLO_UNITA_MCOGEN)
                    ET.SubElement(doc, "POTENZA_TERMICA_MCOGEN").text = str(POTENZA_TERMICA_MCOGEN)
                    ET.SubElement(doc, "POTENZA_IMMESSA_MCOGEN").text = str(POTENZA_IMMESSA_MCOGEN)
                    ET.SubElement(doc, "PROD_IMMESSA_IN_RETE_SEZ").text = str(PROD_IMMESSA_IN_RETE_SEZ)
                    ET.SubElement(doc, "TIPO_INSTALLAZIONE_ACC").text = str(TIPO_INSTALLAZIONE_ACC)
                    ET.SubElement(doc, "TIPO_TECNOLOGIA_ACC").text = str(TIPO_TECNOLOGIA_ACC)
                    ET.SubElement(doc, "SOTTOTIPO_TECNOLOGIA_ACC").text = str(SOTTOTIPO_TECNOLOGIA_ACC)
                    ET.SubElement(doc, "MODELLO_ACC").text = str(MODELLO_ACC)
                    ET.SubElement(doc, "COSTRUTTORE_ACC").text = str(COSTRUTTORE_ACC)
                    if str(DICHIARAZIONE_ACC) == '2':
                        ET.SubElement(doc, "ALIMENTAZIONE_IMPIANTO").text = str(ALIMENTAZIONE_IMPIANTO)
                    else:
                        ET.SubElement(doc, "ALIMENTAZIONE_IMPIANTO").text = None
                    if str(DICHIARAZIONE_ACC) == '2':
                        ET.SubElement(doc, "ALIMENTAZIONE_RETE").text = str(ALIMENTAZIONE_RETE)
                    else:
                        ET.SubElement(doc, "ALIMENTAZIONE_RETE").text = None
                    if str(DICHIARAZIONE_ACC) == '2':
                        ET.SubElement(doc, "FLAG_CC_CA_ACC").text = str(FLAG_CC_CA_ACC)
                    else:
                        ET.SubElement(doc, "FLAG_CC_CA_ACC").text = None
                    if str(DICHIARAZIONE_ACC) == '2':
                        ET.SubElement(doc, "POT_NOMINALE_ASSORBIMENTO_ACC").text = str(POT_NOMINALE_ASSORBIMENTO_ACC)
                    else:
                        ET.SubElement(doc, "POT_NOMINALE_ASSORBIMENTO_ACC").text = None
                    if str(DICHIARAZIONE_ACC) == '2':
                        ET.SubElement(doc, "POT_ATTIVA_NOMINALE_RILASCIO_ACC").text = str(POT_ATTIVA_NOMINALE_RILASCIO_ACC)
                    else:
                        ET.SubElement(doc, "POT_ATTIVA_NOMINALE_RILASCIO_ACC").text = None
                    if str(DICHIARAZIONE_ACC) == '2':
                        ET.SubElement(doc, "POT_APPARENTE_NOMINALE_ACC").text = str(POT_APPARENTE_NOMINALE_ACC)
                    else:
                        ET.SubElement(doc, "POT_APPARENTE_NOMINALE_ACC").text = None
                    if FLAG_CC_CA_ACC == 'A':

                        ET.SubElement(doc, "POT_ATTIVA_INVERTER_ACC").text = str(POT_ATTIVA_INVERTER_ACC)
                    else:
                        ET.SubElement(doc, "POT_ATTIVA_INVERTER_ACC").text = None
                    if str(DICHIARAZIONE_ACC) == '2':
                        ET.SubElement(doc, "TENSIONE_NOMINALE_ACC").text = str(TENSIONE_NOMINALE_ACC)
                    else:
                        ET.SubElement(doc, "TENSIONE_NOMINALE_ACC").text = None
                    if str(DICHIARAZIONE_ACC) == '2':
                        ET.SubElement(doc, "CAPACITA_NOMINALE_ACC").text = str(CAPACITA_NOMINALE_ACC)
                    else:
                        ET.SubElement(doc, "CAPACITA_NOMINALE_ACC").text = None
                    if str(DICHIARAZIONE_ACC) == '2':
                        ET.SubElement(doc, "CAPACITA_UTILIZZATA_MASSIMA_ACC").text = str(CAPACITA_UTILIZZATA_MASSIMA_ACC)
                    else:
                        ET.SubElement(doc, "CAPACITA_UTILIZZATA_MASSIMA_ACC").text = None

                    ET.SubElement(doc, "CODICE_ELABORAZIONE").text = None
                    ET.SubElement(doc, "DESCRIZIONE_ELABORAZIONE").text = None
                    log(row[7], row)

                line_count += 1


    except Exception as e:
        print(e)
        traceback.print_exc()

    tree = ET.ElementTree(root)
    tree.write(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\G12_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml", short_empty_elements=False)


def log(preventivo, row):
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\G12\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()

