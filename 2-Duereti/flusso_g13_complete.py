import xml.etree.cElementTree as ET
import csv
import traceback
import os
from datetime import date, datetime
import xml.etree.ElementTree as Xet
from Lancia_funzione import move_files, cerca_file_e_controlla_testo
from logger_manager import FlowLogger

# Inizializza logger globale
logger = None

def initialize_logger():
    """Inizializza il logger per G13"""
    global logger
    logger = FlowLogger("G13")
    logger.log_start("Elaborazione flusso G13 - Carica UPNR")

def log_legacy(preventivo, row):
    """Mantieni la funzione di log legacy esistente"""
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G02\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()

def flussoG13():
    global logger
    
    try:
        basepath = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\4-Registrati'
        
        # Trova il file XML più recente nella cartella Registrati
        input_xml_file = None
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                input_xml_file = entry
                break
        
        if not input_xml_file:
            logger.log_warning("Nessun file XML trovato nella cartella Registrati")
            return
            
        input_xml_path = os.path.join(basepath, input_xml_file)
        
        # Log del file XML di input con timestamp di creazione
        logger.log_file_processed(input_xml_path, "XML input Registrati")
        
        xmlparse = Xet.parse(input_xml_path)
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

        logger.log_info(f"Processati {xml_record_count} record dal file XML Registrati")

        # Processa il CSV G12
        csv_path = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G12\\G12.csv'
        
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            output_root = ET.Element("CARICA_UPNR", COD_SERVIZIO="G13", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                              GESTORE_PIVA="13632560960")

            logger.log_info("-------------------------------G13--------------------------------------")
            
            processed_matches = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                else:
                    print(row[7])
                    for item in rows:
                        if item[2] == row[7]:  # Match CODICE_RINTRACCIABILITA
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
                                
                            doc = ET.SubElement(output_root, "UPNR")
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

                            log_legacy(row[7], row)
                            processed_matches += 1
                        else:
                            pass
                line_count += 1
        
        # Log analisi CSV
        logger.log_csv_analysis(csv_path, line_count - 1, ['codice_rintracciabilita'])

        # Salva XML di output
        tree = ET.ElementTree(output_root)
        output_xml_path = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G13_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml"
        tree.write(output_xml_path, short_empty_elements=False)
        
        # Log XML generato
        logger.log_xml_generated(output_xml_path, processed_matches)
        logger.update_stats(xml_records_input=xml_record_count, 
                          csv_records_processed=line_count - 1,
                          matches_found=processed_matches)

    except Exception as e:
        logger.log_error("Errore in flussoG13", e)
        traceback.print_exc()
        raise

def g13_query():
    global logger
    csv_path = '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G12\\G12.csv'
    
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
            query = f"""insert into voce_pratica
        select cod_pratica,
        (select 'CHLAV' from dual) as COD_STADIO,
        (select 'GAUI13' from dual) as COD_VOCE_ELEMENT,
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
        ) and cod_voce_element like 'GAUI13');
        commit;
    quit;"""

            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G13_update_{timestamp}.txt"
            with open(filename, 'w') as file:
                file.write(query)
                file.close()
            
            # Log query generata
            logger.log_query_generated(filename, "G13_insert")
            logger.log_info(f"Query G13 generata per {len(lista)} record")
            
    except Exception as e:
        logger.log_error("Errore in g13_query", e)
        raise

def main():
    """Funzione principale quando eseguito come script standalone"""
    global logger
    
    try:
        # Inizializza logger
        initialize_logger()
        
        # Esegui le funzioni principali
        logger.log_info("Inizio elaborazione flusso G13")
        
        flussoG13()
        
        cerca_file_e_controlla_testo(
            f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 
            'G13',
            g13_query
        )
        
        move_files(
            r'\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Duereti\4-Registrati', 
            r'\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Duereti\4-Registrati\old'
        )
        
        logger.log_info("Elaborazione G13 completata con successo")
        
    except Exception as e:
        if logger:
            logger.log_error(f"Errore generale nell'esecuzione di G13", e)
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
    flussoG13()
    cerca_file_e_controlla_testo(
                    f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G13',
                    g13_query)
    move_files(r'\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Duereti\4-Registrati', r'\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Duereti\4-Registrati\old')
    if logger:
        logger.log_end()