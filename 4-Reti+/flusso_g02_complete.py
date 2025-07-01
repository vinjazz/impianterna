import traceback
import xml.etree.cElementTree as ET
import csv
from datetime import date, datetime
import xml.etree.ElementTree as Xet
import os
from Lancia_funzione import cerca_file_e_controlla_testo
from logger_manager import FlowLogger

# Inizializza logger globale
logger = None

def initialize_logger():
    """Inizializza il logger per G02"""
    global logger
    logger = FlowLogger("G02")
    logger.log_start("Elaborazione flusso G02 - Validazione Impianti")

def gestisci_file_g02():
    """Gestisce i file G02 mantenendo solo il più grande"""
    global logger
    
    try:
        directory = "\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+"
        
        # Trova tutti i file che iniziano con G02 e finiscono con .xml
        file_g02 = [f for f in os.listdir(directory) if f.startswith('G02') and f.endswith('.xml')]
        
        logger.log_info(f"Trovati {len(file_g02)} file G02: {file_g02}")

        # Se c'è solo un file, non fa nulla
        if len(file_g02) <= 1:
            logger.log_info("C'è solo un file (o nessun file) che inizia con G02. Nessuna azione necessaria.")
            return
            
        # Calcola le dimensioni di ogni file e trova il file con dimensioni maggiori
        file_g02_percorso = [os.path.join(directory, f) for f in file_g02]
        file_con_dimensioni = [(f, os.path.getsize(f)) for f in file_g02_percorso]

        # Log di tutti i file trovati
        for file_path, size in file_con_dimensioni:
            logger.log_file_processed(file_path, "G02 XML candidate", {'size_bytes': size})

        # Trova il file con le dimensioni maggiori
        file_maggiore = max(file_con_dimensioni, key=lambda x: x[1])

        # Mantiene solo il file più grande e cancella gli altri
        files_deleted = 0
        for file, dimensione in file_con_dimensioni:
            if file != file_maggiore[0]:
                os.remove(file)
                logger.log_info(f"Cancellato file {os.path.basename(file)} di dimensione {dimensione} byte.")
                files_deleted += 1

        logger.log_info(f"Il file {os.path.basename(file_maggiore[0])} con dimensione {file_maggiore[1]} byte è stato mantenuto.")
        logger.update_stats(files_deleted=files_deleted)
        
    except Exception as e:
        logger.log_error("Errore nella gestione file G02", e)
        raise

def g02_query():
    global logger
    csv_path = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\G12\\G12.csv'
    
    try:
        lista = []
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    lista.append(row[7])
                line_count += 1
            
            # Log analisi CSV
            logger.log_csv_analysis(csv_path, line_count - 1, ['codice_rintracciabilita'])
            
            result_string = "'" + "', '".join(map(str, lista)) + "'"
            query = f"""insert into voce_pratica
        select cod_pratica,
        (select 'CHLAV' from dual) as COD_STADIO,
        (select 'GAUI02' from dual) as COD_VOCE_ELEMENT,
        p.dat_decorrenza_pra as DAT_INO_VLI_VOCE, 
        to_date('31/12/2100', 'dd/mm/yyyy') as DAT_FIN_VLI_VOCE,
        (select '6110' from dual) as NUM_PGS_VOCE,
        (select 'V' from dual) as COD_FLG_ORIGINE,
        (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy') from dual) as DES_VAL_VOCE, 
        sysdate as DAT_CREAZIONE_REC,
        sysdate as DAT_ULT_AGG_REC,
        (select 'W70030' from dual) as COD_OPERATORE
        from pratica p  where cod_pratica in (
        {result_string}
        )
        and cod_pratica not in (select cod_pratica from voce_pratica where cod_pratica in (
        {result_string}
        ) and cod_voce_element like 'GAUI02');
        commit;
        quit;"""

            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\update_query\\G02_update_{timestamp}.txt"
            
            with open(filename, 'w') as file:
                file.write(query)
                file.close()
            
            # Log query generata
            logger.log_query_generated(filename, "G02_insert")
            logger.log_info(f"Query G02 generata per {len(lista)} record")
            
    except Exception as e:
        logger.log_error("Errore in g02_query", e)
        raise

def log_legacy(preventivo, row):
    """Mantieni la funzione di log legacy esistente"""
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\G02\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()

def flussoG02():
    global logger
    
    try:
        # Trova e processa il file XML più recente dalla cartella Registrati
        basepath = r'\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Reti+\4-Registrati'
        
        # Trova il file più recente
        input_xml_file = None
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                input_xml_file = entry
                break
        
        if not input_xml_file:
            logger.log_warning("Nessun file trovato nella cartella Registrati")
            return
            
        input_xml_path = os.path.join(basepath, input_xml_file)
        
        # Log del file XML di input con timestamp di creazione
        logger.log_file_processed(input_xml_path, "XML input Registrati")
        
        # Parse del file XML
        xmlparse = Xet.parse(input_xml_path)
        root = xmlparse.getroot()
        rows = []
        
        # Estrai dati dal XML
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
            xml_record_count += 1
        
        logger.log_info(f"Estratti {xml_record_count} record dal file XML Registrati")
        
        # Processa il CSV G12
        csv_path = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\G12\\G12.csv'
        
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            
            # Crea XML di output
            output_root = ET.Element("VALIDA_IMPIANTI", COD_SERVIZIO="G02", COD_FLUSSO="0050", 
                                   TERNA_PIVA="05779661007", GESTORE_PIVA="04152790962")

            logger.log_info("-------------------------------G02--------------------------------------")
            
            processed_matches = 0
            for row in csv_reader:
                print(row[7])
                if line_count == 0:
                    pass
                else:
                    for item in rows:
                        if item[2] == row[7]:  # Match CODICE_RINTRACCIABILITA
                            doc = ET.SubElement(output_root, "IMPIANTO", CODICE=item[0], TIPO_OPERAZIONE="V")
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
                            
                            log_legacy(row[7], row)  # Mantieni log legacy
                            processed_matches += 1

                line_count += 1

            # Salva XML di output
            tree = ET.ElementTree(output_root)
            output_xml_path = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\G02_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml"
            tree.write(output_xml_path, short_empty_elements=False)
            
            # Log XML generato
            logger.log_xml_generated(output_xml_path, processed_matches)
            logger.log_info(f"Processati {processed_matches} match tra XML e CSV")
            
            # Log analisi CSV
            logger.log_csv_analysis(csv_path, line_count, ['codice_rintracciabilita'])
            
            logger.update_stats(xml_records_input=xml_record_count, 
                              csv_records_processed=line_count,
                              matches_found=processed_matches)
            
    except Exception as e:
        logger.log_error("Errore in flussoG02", e)
        traceback.print_exc()
        raise

def main():
    """Funzione principale quando eseguito come script standalone"""
    global logger
    
    try:
        # Inizializza logger
        initialize_logger()
        
        # Esegui le funzioni principali
        logger.log_info("Inizio elaborazione flusso G02")
        
        flussoG02()
        gestisci_file_g02()
        
        cerca_file_e_controlla_testo(
            f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 
            'G02', 
            g02_query
        )
        
        logger.log_info("Elaborazione G02 completata con successo")
        
    except Exception as e:
        if logger:
            logger.log_error(f"Errore generale nell'esecuzione di G02", e)
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
    flussoG02()
    gestisci_file_g02()
    cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G02', g02_query)
    if logger:
        logger.log_end()