import xml.etree.cElementTree as ET
import csv
from datetime import date, datetime
from Lancia_funzione import cerca_file_e_controlla_testo
from logger_manager import FlowLogger

# Inizializza logger globale
logger = None

def initialize_logger():
    """Inizializza il logger per G01"""
    global logger
    logger = FlowLogger("G01")
    logger.log_start("Elaborazione flusso G01 - Gestione POD")

def g01_controllo_query():
    global logger
    csv_path = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G01\\G01.csv'
    
    try:
        with open(csv_path) as G01_csv_file:
            G01_lista = []
            G01_csv_reader = csv.reader(G01_csv_file, delimiter=';')
            G01_line_count = 0
            
            for row in G01_csv_reader:
                if G01_line_count == 0:
                    pass
                else:
                    G01_lista.append(row[0])
                G01_line_count += 1
            
            # Log analisi CSV
            logger.log_csv_analysis(csv_path, G01_line_count - 1, ['cod_pratica'])
            
            G01_result_string = "'" + "', '".join(map(str, G01_lista)) + "'"
            query = f"""update voce_pratica 
            set des_val_voce = (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy') from dual)
        where cod_pratica in (
        {G01_result_string}
        ) and cod_voce_element like 'GAUI01' and des_val_voce is null;
        commit;
        quit;
        """

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G01_Controllo_update_{timestamp}.txt"
        
        with open(filename, 'w') as file:
            file.write(query)
            file.close()
        
        # Log query generata
        logger.log_query_generated(filename, "controllo_update")
        logger.log_info(f"Query di controllo generata per {len(G01_lista)} record")
        
    except Exception as e:
        logger.log_error(f"Errore in g01_controllo_query", e)
        raise

def g01_query():
    global logger
    csv_path = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G01\\G01.csv'
    
    try:
        with open(csv_path) as G01_csv_file:
            G01_lista = []
            G01_csv_reader = csv.reader(G01_csv_file, delimiter=';')
            G01_line_count = 0
            
            for row in G01_csv_reader:
                if G01_line_count == 0:
                    pass
                else:
                    G01_lista.append(row[0])
                G01_line_count += 1
            
            G01_result_string = "'" + "', '".join(map(str, G01_lista)) + "'"

            query = f""" insert into voce_pratica
        select cod_pratica,
        (select 'VLAV' from dual) as COD_STADIO,
        (select 'GAUI01' from dual) as COD_VOCE_ELEMENT,
        p.dat_decorrenza_pra as DAT_INO_VLI_VOCE, 
        to_date('31/12/2100', 'dd/mm/yyyy') as DAT_FIN_VLI_VOCE,
        (select '6110' from dual) as NUM_PGS_VOCE,
        (select 'V' from dual) as COD_FLG_ORIGINE,
        (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy') from dual) as DES_VAL_VOCE, 
        sysdate as DAT_CREAZIONE_REC,
        sysdate as DAT_ULT_AGG_REC,
        (select 'W70030' from dual) as COD_OPERATORE
        from pratica p  where cod_pratica in (
        {G01_result_string}
        )
        and cod_pratica not in (select cod_pratica from voce_pratica where cod_pratica in (
        {G01_result_string}
        ) and cod_voce_element like 'GAUI01');
        commit;
    quit;"""

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G01_update_{timestamp}.txt"
        
        with open(filename, 'w') as file:
            file.write(query)
            file.close()
        
        # Log query generata
        logger.log_query_generated(filename, "insert_update")
        logger.log_info(f"Query di inserimento generata per {len(G01_lista)} record")
        
    except Exception as e:
        logger.log_error(f"Errore in g01_query", e)
        raise

def flussoG01New():
    global logger
    csv_path = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G01\\G01.csv'
    
    try:
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            
            root = ET.Element("GESTIONE_POD", COD_SERVIZIO="G01", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                              GESTORE_PIVA="13632560960")

            processed_records = 0
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

                    doc = ET.SubElement(root, "POD", CODICE=POD, TIPO_OPERAZIONE="U")
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

                    log_legacy(row[0], row)  # Mantieni il log legacy
                    processed_records += 1
                    print(row[0])
                    
                line_count += 1
            
            # Log analisi CSV
            logger.log_csv_analysis(csv_path, processed_records, 
                                  ['CODICE_RINTACCIABILITA', 'POD', 'POTENZA_IMMISSIONE_KW', 
                                   'POTENZA_PRELIEVO_KW', 'PUNTO_DI_SOLA_IMMISSIONE', 
                                   'SSPC_TIPOLOGIA_DICHIARATA', 'TIPO_CONNESSIONE', 
                                   'LIVELLO_TENSIONE', 'TIPO_ITER'])
        
        # Genera XML
        tree = ET.ElementTree(root)
        xml_filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G01_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml"
        tree.write(xml_filename, short_empty_elements=False)
        
        # Log XML generato
        logger.log_xml_generated(xml_filename, processed_records)
        logger.update_stats(records_processed=processed_records)
        
    except Exception as e:
        logger.log_error(f"Errore in flussoG01New", e)
        raise

def log_legacy(preventivo, row):
    """Mantieni la funzione di log legacy esistente"""
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\\\Duereti\\G01\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()

def main():
    """Funzione principale quando eseguito come script standalone"""
    global logger
    
    try:
        # Inizializza logger
        initialize_logger()
        
        # Esegui le funzioni principali
        logger.log_info("Inizio elaborazione flusso G01")
        
        flussoG01New()
        
        cerca_file_e_controlla_testo(
            f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\", 
            'G01', 
            g01_query
        )
        
        cerca_file_e_controlla_testo(
            f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\", 
            'G01', 
            g01_controllo_query
        )
        
        logger.log_info("Elaborazione G01 completata con successo")
        
    except Exception as e:
        if logger:
            logger.log_error(f"Errore generale nell'esecuzione di G01", e)
        print(f"Errore: {e}")
        raise
    finally:
        if logger:
            logger.log_end()

# Esecuzione quando chiamato direttamente (per compatibilità con versione attuale)
if __name__ == "__main__":
    main()
else:
    # Se importato, esegui comunque le funzioni (compatibilità esistente)
    initialize_logger()
    flussoG01New()
    cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\", 'G01', g01_query)
    cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\", 'G01', g01_controllo_query)
    if logger:
        logger.log_end()