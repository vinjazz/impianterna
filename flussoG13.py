import xml.etree.cElementTree as ET
import csv
import traceback
import os
from datetime import date, datetime
from recupero_log import log_summary
import xml.etree.ElementTree as Xet
import Move_file

def flussoG13():
    basepath = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Registrati'
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            name = entry
    xmlparse = Xet.parse('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Registrati\\' + name)
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

    with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\G12\\G12.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        root = ET.Element("CARICA_UPNR", COD_SERVIZIO="G13", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                          GESTORE_PIVA="12883450152")

        print("-------------------------------G13--------------------------------------")
        try:
            for row in csv_reader:

                if line_count == 0:
                    pass
                else:
                    print(row[7])
                    for item in rows:
                        if item[2] == row[7]:


                            DICHIARAZIONE_ACC = row[16]
                            POT_DI_PICCO_SEZ = row[26].replace(',', '.')
                            POT_APPARENTE_NOMINALE_SEZ = row[27]
                            PROD_ANNUA_LORDA_SEZ = row[28]
                            FATTORE_POTENZA_NOMINALE_SEZ = row[29]
                            POT_ATTIVA_NOMINALE_SEZ = row[30].replace(',', '.')
                            POT_ATTIVA_INVERTER_SEZ = row[31].replace(',', '.')
                            POT_EFF_LORDA = row[33].replace(',', '.')
                            POT_EFF_NETTA = row[34].replace(',', '.')
                            MARCA_UNITA_MCOGEN = row[35]
                            MODELLO_UNITA_MCOGEN = row[36]
                            POTENZA_TERMICA_MCOGEN = row[37]
                            POTENZA_IMMESSA_MCOGEN = row[38]
                            if row[16] == '2':
                                MODELLO_ACC = row[43]
                            else:
                                MODELLO_ACC = ''
                            if row[16] == '2':
                                COSTRUTTORE_ACC = row[44]
                            else:
                                COSTRUTTORE_ACC = ''
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
                                CAPACITA_NOMINALE_ACC = row[53].replace(',', '.')
                            except AttributeError:
                                CAPACITA_NOMINALE_ACC = ''
                            try:
                                CAPACITA_UTILIZZATA_MASSIMA_ACC = row[54].replace(',', '.')
                            except AttributeError:
                                CAPACITA_UTILIZZATA_MASSIMA_ACC = ''
                            doc = ET.SubElement(root, "UPNR")
                            ET.SubElement(doc, "CODICE_IMP").text = str(item[0])
                            ET.SubElement(doc, "CODICE_SEZ").text =  str(item[0].replace('IM', 'SZ')) + '_01'
                            ET.SubElement(doc, "POT_DI_PICCO_SEZ").text = str(POT_DI_PICCO_SEZ)
                            ET.SubElement(doc, "POT_APPARENTE_NOMINALE_SEZ").text = str(POT_APPARENTE_NOMINALE_SEZ)
                            ET.SubElement(doc, "PROD_ANNUA_LORDA_SEZ").text = str(PROD_ANNUA_LORDA_SEZ)
                            ET.SubElement(doc, "FATTORE_POTENZA_NOMINALE_SEZ").text = str(FATTORE_POTENZA_NOMINALE_SEZ)
                            ET.SubElement(doc, "POT_ATTIVA_NOMINALE_SEZ").text = str(POT_ATTIVA_NOMINALE_SEZ)
                            ET.SubElement(doc, "POT_ATTIVA_INVERTER_SEZ").text = str(POT_ATTIVA_INVERTER_SEZ)
                            ET.SubElement(doc, "POT_EFF_LORDA").text = str(POT_EFF_LORDA)
                            ET.SubElement(doc, "POT_EFF_NETTA").text = str(POT_EFF_NETTA)
                            ET.SubElement(doc, "MARCA_UNITA_MCOGEN").text = str(MARCA_UNITA_MCOGEN)
                            ET.SubElement(doc, "MODELLO_UNITA_MCOGEN").text = str(MODELLO_UNITA_MCOGEN)
                            ET.SubElement(doc, "POTENZA_TERMICA_MCOGEN").text = str(POTENZA_TERMICA_MCOGEN)
                            ET.SubElement(doc, "POTENZA_IMMESSA_MCOGEN").text = str(POTENZA_IMMESSA_MCOGEN)
                            ET.SubElement(doc, "MODELLO_ACC").text = str(MODELLO_ACC)
                            ET.SubElement(doc, "COSTRUTTORE_ACC").text = str(COSTRUTTORE_ACC)

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
                                ET.SubElement(doc, "CAPACITA_NOMINALE_ACC").text = str(CAPACITA_NOMINALE_ACC)
                            else:
                                ET.SubElement(doc, "CAPACITA_NOMINALE_ACC").text = None
                            if str(DICHIARAZIONE_ACC) == '2':
                                ET.SubElement(doc, "CAPACITA_UTILIZZATA_MASSIMA_ACC").text = str(CAPACITA_UTILIZZATA_MASSIMA_ACC)
                            else:
                                ET.SubElement(doc, "CAPACITA_UTILIZZATA_MASSIMA_ACC").text = None

                            # log(row[7], row)
                        else:
                            pass
                line_count += 1


        except Exception as e:
            print(e)
            traceback.print_exc()

    tree = ET.ElementTree(root)
    # tree.write(f"C:\\ImpiantiTerna\\G13\\G13_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
    #            short_empty_elements=False)
    tree.write(
        f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\G13_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
        short_empty_elements=False)
    Move_file.move_file('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Registrati')

# def log(preventivo, row):
#     line = f'{date.today()};{preventivo}'
#     file_uno = open(f"C:\\ImpiantiTerna\\G13\\log\\{preventivo}.csv", "w")
#     file_uno.write(line)
#     for data in row:
#         file_uno.write(f"\n {data};")
#     file_uno.close()

