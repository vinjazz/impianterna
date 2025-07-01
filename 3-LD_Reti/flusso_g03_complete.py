import datetime
import xml.etree.cElementTree as ET
from datetime import date, datetime
import csv
import glob
import os
import xml.etree.ElementTree as Xet
from Lancia_funzione import move_files
from logger_manager import FlowLogger, get_latest_filename_in_directory

# Inizializza logger globale
logger = None

def initialize_logger():
    """Inizializza il logger per G03"""
    global logger
    logger = FlowLogger("G03")
    logger.log_start("Elaborazione flusso G03 - Completamento Impianto")

def get_most_recent_xml(directory ='\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LD_Reti\\2-Realizzati'):
    global logger
    
    try:
        file_pattern = os.path.join(directory, '*.xml')
        files = glob.glob(file_pattern)

        if not files:
            logger.log_warning(f"No XML files found in directory: {directory}")
            return None

        latest_file = max(files, key=os.path.getctime)
        latest_filename = os.path.basename(latest_file)
        
        logger.log_info(f"The most recent XML file is: {latest_filename}")
        
        # Log del file XML trovato con timestamp di creazione
        logger.log_file_processed(latest_file, "XML input Realizzati")
        
        return latest_filename
        
    except Exception as e:
        logger.log_error(f"Errore in get_most_recent_xml: {str(e)}")
        return None

def search_read_move_sides_csv(directory = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI'):
    global logger
    
    try:
        file_pattern = os.path.join(directory, 'Sides*.csv')
        files = glob.glob(file_pattern)

        if not files:
            logger.log_warning(f"No matching CSV files found in directory: {directory}")
            return None

        latest_file = max(files, key=os.path.getctime)
        logger.log_info(f"Reading the most recent CSV file: {latest_file}")
        
        # Log del file CSV con timestamp di creazione
        logger.log_file_processed(latest_file, "CSV input Sides")

        data = []
        with open(latest_file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Skip the first row
            for row in reader:
                print(row)
                data.append(row)

        logger.log_csv_analysis(latest_file, len(data), ['codice_rintracciabilita', 'data_completamento', 'potenza_effettiva'])
        print(data)
        return data
        
    except Exception as e:
        logger.log_error(f"Errore in search_read_move_sides_csv: {str(e)}")
        return None

def log_legacy(preventivo, row):
    """Mantieni la funzione di log legacy esistente"""
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LD_Reti\\G03\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()

def g03():
    global logger
    
    try:
        logger.log_info('Begin G03 processing')
        
        realizzati_dir = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LD_Reti\\2-Realizzati'
        latest_xml_name = get_most_recent_xml(realizzati_dir)
        
        if not latest_xml_name:
            logger.log_error("Nessun file XML trovato nella cartella Realizzati")
            return
            
        xml_full_path = os.path.join(realizzati_dir, latest_xml_name)
        
        xmlparse = Xet.parse(xml_full_path)
        root = xmlparse.getroot()
        rows = []
        
        xml_record_count = 0
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
            xml_record_count += 1
        
        logger.log_info(f"Processati {xml_record_count} record dal file XML Realizzati")

        csv_data = search_read_move_sides_csv()
        if not csv_data:
            logger.log_error("Nessun dato CSV trovato")
            return
            
        output_root = ET.Element("COMPLETAMENTO_IMPIANTO", COD_SERVIZIO="G03", COD_FLUSSO="0050", TERNA_PIVA="05779661007", GESTORE_PIVA="01341400198")
        
        processed_matches = 0
        for row in csv_data:
            for datas in rows:
                if row[0] == datas[2]:  # Match CODICE_RINTRACCIABILITA
                    doc = ET.SubElement(output_root, "IMPIANTO", CODICE = f"{datas[0]}")
                    data = datetime.strptime(row[5],'%d-%m-%Y').date()
                    ET.SubElement(doc, "DATA_COMPLETAMENTO_CONNESSIONE").text = str(data)
                    ET.SubElement(doc, "DATA_SOTTOSCRIZIONE_REGOLAMENTO_ESERCIZIO").text = ""
                    ET.SubElement(doc, "POTENZA_EFFETTIVA").text = row[6].replace(",",".")
                    ET.SubElement(doc, "DATA_FINE_REALIZZAZIONE_IMP").text = ""
                    ET.SubElement(doc, "TIPOLOGIA_DICHIARATA").text = ""
                    ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = row[0]
                    
                    log_legacy(row[0], row)
                    processed_matches += 1
                else:
                    pass
                    
        # Salva XML di output
        tree = ET.ElementTree(output_root)
        output_xml_path = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LD_Reti\\G03_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml"
        tree.write(output_xml_path, short_empty_elements=False)
        
        # Log XML generato
        logger.log_xml_generated(output_xml_path, processed_matches)
        logger.update_stats(xml_records_input=xml_record_count, 
                          csv_records_processed=len(csv_data),
                          matches_found=processed_matches)
        
    except Exception as e:
        logger.log_error(f"Errore in g03: {str(e)}")
        raise

def main():
    """Funzione principale quando eseguito come script standalone"""
    global logger
    
    try:
        # Inizializza logger
        initialize_logger()
        
        # Esegui le funzioni principali
        logger.log_info("Inizio elaborazione flusso G03")
        
        g03()
        
        # Move files dopo il processing
        move_files('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LD_Reti\\2-Realizzati',
                   '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LD_Reti\\2-Realizzati\\old')
        
        logger.log_info("Elaborazione G03 completata con successo")
        
    except Exception as e:
        if logger:
            logger.log_error(f"Errore generale nell'esecuzione di G03", e)
        print(f"Errore: {e}")
        raise
    finally:
        if logger:
            logger.log_end()

# Esecuzione
if __name__ == "__main__":
    main()
else:
    # Compatibilità con esecuzione diretta esistente
    initialize_logger()
    g03()
    move_files('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LD_Reti\\2-Realizzati','\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LD_Reti\\2-Realizzati\\old')
    if logger:
        logger.log_end()