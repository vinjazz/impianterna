import xml.etree.cElementTree as ET
import csv
import traceback
from datetime import date, datetime
from Lancia_funzione import cerca_file_e_controlla_testo
from logger_manager import FlowLogger

# Inizializza logger globale
logger = None

def initialize_logger():
    """Inizializza il logger per G12"""
    global logger
    logger = FlowLogger("G12")
    logger.log_start("Elaborazione flusso G12 - Carica Impianto")

def g12_query():
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
                
            result_string = "'" + "', '".join(map(str, lista)) + "'"

            query = f"""update voce_pratica 
        set des_val_voce = (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy')  from dual)
        where cod_pratica in (
        {result_string}
        ) and cod_voce_element like 'GAUI12';
        commit;
        quit;"""

            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\update_query\\G12_update_{timestamp}.txt"
            with open(filename, 'w') as file:
                file.write(query)
                file.close()
            
            # Log query generata
            logger.log_query_generated(filename, "G12_update")
            logger.log_info(f"Query G12 generata per {len(lista)} record")
            
    except Exception as e:
        logger.log_error("Errore in g12_query", e)
        raise

def g12_controllo_query():
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
                
            result_string = "'" + "', '".join(map(str, lista)) + "'"

            query = f"""update voce_pratica 
                    set des_val_voce = (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy') from dual)
                where cod_pratica in (
                {result_string}
                ) and cod_voce_element in ('GAUI12','GAUI02','GAUI13', 'GAUI03') and des_val_voce is null;
                commit;
                quit;
            """

            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\update_query\\G12_Controllo_update_{timestamp}.txt"
            with open(filename, 'w') as file:
                file.write(query)
                file.close()
            
            # Log query generata
            logger.log_query_generated(filename, "G12_controllo_update")
            logger.log_info(f"Query G12 controllo generata per {len(lista)} record")
            
    except Exception as e:
        logger.log_error("Errore in g12_controllo_query", e)
        raise

def flussoG12New():
    global logger
    csv_path = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\G12\\G12.csv'
    
    try:
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            root = ET.Element("CARICA_IMPIANTO", COD_SERVIZIO="G12", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                              GESTORE_PIVA="04152790962")
            
            processed_records = 0
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
                    
                    log_legacy(row[7], row)
                    processed_records += 1

                line_count += 1

        # Log analisi CSV
        logger.log_csv_analysis(csv_path, processed_records, ['NOME_IMP', 'CODICE_RINTRACCIABILITA', 'DICHIARAZIONE_ACC'])

        # Salva XML
        tree = ET.ElementTree(root)
        xml_filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\G12_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml"
        tree.write(xml_filename, short_empty_elements=False)
        
        # Log XML generato
        logger.log_xml_generated(xml_filename, processed_records)

    except Exception as e:
        logger.log_error("Errore in flussoG12New", e)
        traceback.print_exc()
        raise

def log_legacy(preventivo, row):
    """Mantieni la funzione di log legacy esistente"""
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\G12\\log\\{preventivo}.csv", "w")
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
        logger.log_info("Inizio elaborazione flusso G12")
        
        flussoG12New()
        
        cerca_file_e_controlla_testo(
            f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 
            'G12',
            g12_query
        )
        cerca_file_e_controlla_testo(
            f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 
            'G12',
            g12_controllo_query
        )
        
        logger.log_info("Elaborazione G12 completata con successo")
        
    except Exception as e:
        if logger:
            logger.log_error(f"Errore generale nell'esecuzione di G12", e)
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
    flussoG12New()
    cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G12',g12_query)
    cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G12',g12_controllo_query)
    if logger:
        logger.log_end()