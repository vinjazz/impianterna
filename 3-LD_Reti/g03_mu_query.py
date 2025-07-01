#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G03 MU QUERY GENERATOR CON FLOWLOGGER
=====================================

Genera query SELECT per G03 Misura Unica basata su dati G12.csv
Estrae informazioni complete per pratiche con misura unica

Versione aggiornata con sistema logging FlowLogger
"""

import csv
import datetime
import os
from logger_manager import FlowLogger

# Inizializza logger per G03 MU Query
logger = FlowLogger("G03_MU_QUERY")


def write_G03_MU_query():
    """Genera query SELECT per G03 Misura Unica"""
    logger.log_start("Generazione query G03 MU - Estrazione dati misura unica")

    try:
        csv_path = r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\LD_Reti\G12\G12.csv"

        # Log e analizza file CSV G12
        logger.log_file_processed(csv_path, "CSV G12 input per G03 MU")

        if not os.path.exists(csv_path):
            logger.log_error(f"File CSV non trovato: {csv_path}")
            return False

        lista = []
        headers = None

        try:
            with open(csv_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                line_count = 0

                for row in csv_reader:
                    if line_count == 0:
                        headers = row
                        logger.log_info(f"Headers CSV G12: {row[:8]}...")  # Mostra primi 8 header
                    else:
                        if len(row) > 7:
                            lista.append(row[7])  # Colonna 7 contiene CODICE_RINTRACCIABILITA
                        else:
                            logger.log_warning(f"Riga {line_count} ha meno di 8 colonne")
                    line_count += 1

                # Log analisi CSV
                logger.log_csv_analysis(csv_path, len(lista), headers)
                logger.log_info(f"Pratiche estratte dalla colonna 7: {len(lista)}")

                if len(lista) > 0:
                    # Mostra alcuni esempi di codici estratti
                    sample_codes = lista[:5]
                    logger.log_info(f"Esempi codici: {sample_codes}")

        except Exception as e:
            logger.log_error("Errore lettura file CSV G12", e)
            return False

        if not lista:
            logger.log_warning("Nessun codice pratica estratto dal CSV G12")
            return False

        # Crea stringa SQL con tutti i codici
        result_string = "'" + "', '".join(map(str, lista)) + "'"
        logger.log_info(f"Stringa SQL generata con {len(lista)} codici")

        # Query complessa per G03 MU
        query = f"""select distinct t.cod_pratica,
                    r.cod_voce_element,
                    r.des_val_voce,
                    t.des_val_voce     as pod,
                    a.des_val_voce     as codice,
                    v2.des_val_voce     as data,
                    p.des_val_voce     as potenza,
                    to_char(to_date(v2.des_val_voce, 'dd-mm-yyyy'), 'YYYY') as anno,
                    v1.des_val_voce     as moduni, --1 si 2 no
                    v2.des_val_voce     as dtfinc,
                    CASE
             WHEN value1.des_voce_predef = 'RITIRO DEDICATO (280-07)' THEN
              1
             WHEN value1.des_voce_predef = 'SCAMBIO SUL POSTO' and
                  to_number(replace(p.des_val_voce, ',', '.')) <= 20 THEN
              13
             WHEN value1.des_voce_predef = 'SCAMBIO SUL POSTO' and
                  to_number(replace(p.des_val_voce, ',', '.')) > 20 THEN
              14
           END as SSPC_TIPOLOGIA_DICHIARATA
      from voce_pratica r
           left join voce_pratica t on t.cod_pratica = r.cod_pratica
           left join voce_pratica a on t.cod_pratica = a.cod_pratica
           left join voce_pratica p on t.cod_pratica = p.cod_pratica
           left join voce_pratica v1 on v1.cod_pratica = a.cod_pratica
           left join voce_pratica v2 on v2.cod_pratica = a.cod_pratica
           left join pratica pr on pr.cod_pratica = t.cod_pratica
           left join voce_pratica f on f.cod_pratica = a.cod_pratica
           left join val_predef_voce value1 on f.des_val_voce = value1.cod_voce_predef    
     where 
       --and t.dat_creazione_rec > to_date('01-01-2016', 'dd-mm-yyyy')
       t.cod_voce_element in ('PODCON', 'POD51')
       and r.cod_voce_element = 'RICPO2'
       and t.des_val_voce is not null
       and a.cod_voce_element = 'MODUNI'
       --and a.des_val_voce != 'IM_'
       --and a.des_val_voce like 'IM%'
       --and v.des_val_voce is not null
       --and to_date(v.des_val_voce, 'dd-mm-yyyy') >
       --to_date('01-01-2016', 'dd-mm-yyyy')
       and p.cod_voce_element = 'YOTD12'
       --and p.cod_stadio = 'CVAR'
       and v1.cod_voce_element = 'MODUNI'
       and v2.cod_voce_element = 'DTFINC'
       and pr.cod_azienda = 1
       and f.cod_voce_element like 'TIPCON'
       and t.cod_pratica in (
    {result_string}
    );

        """

        # Salva query nel file
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LD_Reti\\update_query\\G03_MU_Query_{timestamp}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(query)

            # Log query generata
            logger.log_query_generated(filename, "SELECT G03 MU")

            # Log dettagli query
            logger.log_info("Query G03 MU generata con successo")
            logger.log_info("Tabelle coinvolte: voce_pratica (multiple joins), pratica, val_predef_voce")
            logger.log_info("Campi estratti: cod_pratica, pod, codice, data, potenza, anno, moduni, tipologia")
            logger.log_info(f"Filtro pratiche: {len(lista)} codici da G12.csv colonna 7")
            logger.log_info(f"Query salvata in: {os.path.basename(filename)}")

            # Analizza query generata
            query_lines = query.count('\n')
            query_size = len(query.encode('utf-8'))

            logger.log_info(f"Dimensioni query: {query_lines} righe, {query_size} bytes")

            # Log file query con dettagli aggiuntivi
            additional_info = {
                'query_type': 'SELECT con JOIN multipli',
                'tables_involved': ['voce_pratica', 'pratica', 'val_predef_voce'],
                'input_records': len(lista),
                'query_lines': query_lines,
                'query_complexity': 'HIGH - Multiple LEFT JOINs con CASE logic'
            }
            logger.log_file_processed(filename, "SQL Query G03 MU", additional_info)

            # Aggiorna statistiche
            logger.update_stats(
                records_processed=len(lista),
                queries_generated=1,
                files_created=1,
                query_complexity_score=8  # Alto per via dei JOIN multipli
            )

            logger.log_info(f"G03 MU Query completato: query per {len(lista)} pratiche generata")
            return True

        except Exception as e:
            logger.log_error(f"Errore scrittura query file {filename}", e)
            return False

    except Exception as e:
        logger.log_error("Errore write_G03_MU_query", e)
        return False
    finally:
        logger.log_end()


def analyze_g12_structure():
    """Analizza struttura del file G12 per debugging"""
    logger.log_start("Analisi struttura file G12 per G03 MU")

    try:
        csv_path = r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\LD_Reti\G12\G12.csv"

        if not os.path.exists(csv_path):
            logger.log_error(f"File G12 non trovato: {csv_path}")
            return False

        logger.log_file_processed(csv_path, "CSV G12 analysis")

        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            # Analizza header
            headers = next(csv_reader, [])
            logger.log_info(f"Totale colonne in G12: {len(headers)}")

            if len(headers) > 7:
                logger.log_info(f"Colonna 7 (indice 7): '{headers[7]}'")
                logger.log_info(f"Colonne 5-10: {headers[5:11]}")
            else:
                logger.log_warning("File G12 ha meno di 8 colonne!")

            # Analizza prime righe
            sample_rows = []
            for i, row in enumerate(csv_reader):
                if i < 3:  # Prime 3 righe di dati
                    if len(row) > 7:
                        sample_rows.append(row[7])
                    else:
                        sample_rows.append("MISSING")
                else:
                    break

            logger.log_info(f"Esempi valori colonna 7: {sample_rows}")

            logger.log_info("Analisi G12 completata")
            return True

    except Exception as e:
        logger.log_error("Errore analyze_g12_structure", e)
        return False
    finally:
        logger.log_end()


def main():
    """Funzione principale"""
    try:
        print("🚀 Avvio G03 MU Query Generator")
        print("=" * 60)
        print("📋 Generazione query SELECT per misura unica")
        print("📁 Input: G12.csv colonna 7 (CODICE_RINTRACCIABILITA)")
        print("📄 Output: Query SQL complessa con JOIN multipli")
        print("=" * 60)

        # Opzione per analizzare struttura G12 prima di generare query
        if len(os.sys.argv) > 1 and os.sys.argv[1] == "--analyze":
            print("🔍 Modalità analisi struttura G12...")
            success = analyze_g12_structure()
        else:
            print("🔄 Generazione query G03 MU...")
            success = write_G03_MU_query()

        if success:
            print("\n✅ G03 MU Query completato con successo!")
            print("📊 Controlla i log per dettagli completi")
            print("📄 Query salvata in update_query/")
        else:
            print("\n❌ Errore durante generazione G03 MU Query")

    except KeyboardInterrupt:
        print("\n⏹️  Esecuzione interrotta dall'utente")
        logger.log_error("Esecuzione interrotta dall'utente")
        logger.log_end()
    except Exception as e:
        print(f"\n❌ Errore durante esecuzione G03 MU Query: {e}")
        logger.log_error("Errore critico durante esecuzione", e)
        logger.log_end()
        import traceback
        traceback.print_exc()


# Esecuzione principale
if __name__ == "__main__":
    main()