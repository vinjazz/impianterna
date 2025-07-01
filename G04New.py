from Lancia_funzione import move_files
import datetime
import xml.etree.cElementTree as ET
import xml.etree.ElementTree as Xet
import glob
import os
from datetime import date, datetime
import csv


def get_most_recent_xml(directory ='\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Esercibili'):
    file_pattern = os.path.join(directory, '*.xml')
    files = glob.glob(file_pattern)

    if not files:
        print(f"No XML files found in directory: {directory}")
        return None

    latest_file = max(files, key=os.path.getctime)
    print(f"The most recent XML file is: {latest_file}")

    # dest_folder = os.path.join(directory, 'old')
    # os.makedirs(dest_folder, exist_ok=True)
    # dest_file = os.path.join(dest_folder, os.path.basename(latest_file))
    # shutil.move(latest_file, dest_file)

    return os.path.basename(latest_file)

def search_read_move_sides_csv(directory = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI'):
    file_pattern = os.path.join(directory, 'sides*.csv')
    files = glob.glob(file_pattern)

    if not files:
        print(f"No matching CSV files found in directory: {directory}")
        return None

    latest_file = max(files, key=os.path.getctime)
    print(f"Reading the most recent CSV file: {latest_file}")

    data = []

    with open(latest_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # Skip the first row
        for row in reader:
            print(row)
            data.append(row)

    """dest_folder = os.path.join(directory, 'old')
    os.makedirs(dest_folder, exist_ok=True)
    dest_file = os.path.join(dest_folder, os.path.basename(latest_file))
    shutil.move(latest_file, dest_file)"""
    print(data)
    return data

def log(preventivo, row):
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\G04\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()

def flussoG04():
    xmlparse = Xet.parse(
        '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Esercibili\\' + str(get_most_recent_xml()))
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

        (k, v), = i.attrib.items()
        rows.append((v,
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
    try:
        list = (search_read_move_sides_csv())

        root = ET.Element("ATTIVAZIONE_CONNESSIONE", COD_SERVIZIO="G04", COD_FLUSSO="0050", TERNA_PIVA="05779661007", GESTORE_PIVA="12883450152")

        for row in list:
            for datas in rows:
                if row[0] == datas[2]:
                    upn = datas[0].replace("IM", "UPN")
                    doc = ET.SubElement(root, "UNITA", CODICE=f"{upn}_01")
                    data = datetime.strptime(row[5],'%d-%m-%Y').date()
                    ET.SubElement(doc, "DATA_ATTIVAZIONE_CONNESSIONE").text = str(data)
                    ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = row[0]
                    ET.SubElement(doc, "CODICE_SCARTO").text = "000"
                    log(row[0], row)
                else:
                    pass
        tree = ET.ElementTree(root)
        tree.write(
            f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\G04_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
            short_empty_elements=False)
        Move_file.move_file(
            '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Esercibili')
    except Exception as e:
        print(e)


