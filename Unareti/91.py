#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLUSSO 91 - GESTIONE LOG G03 E G04 CON FLOWLOGGER
==================================================

Elabora file CSV G03 e G04 dalla directory LOG G03 E G04
Genera query UPDATE per database e sposta file elaborati

Versione aggiornata per FlowLogger esistente
"""

import csv
import datetime
import os
import shutil
from Lancia_funzione import cerca_file_e_controlla_testo_csv
from logger_manager import FlowLogger

# Inizializza logger per flusso 91
logger = FlowLogger("F91")


def write_files_starting_with_G03():
    """Elabora file CSV che iniziano con G03 e genera query UPDATE"""
    logger.log_start("Elaborazione file G03 - Aggiornamento voce_pratica GAUI03")

    try:
        folder_path = r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Unareti\LOG G03 E G04"

        # Lista file G03
        try:
            files_in_folder = os.listdir(folder_path)
            g03_files = [file for file in files_in_folder if file.startswith('G03') and file.endswith('.csv')]

            logger.log_info(f"File G03 trovati: {len(g03_files)}")
            if g03_files:
                for file in g03_files:
                    logger.log_info(f"  - {file}")
        except Exception as e:
            logger.log_error(f"Errore lettura directory: {e}")
            return

        if not g03_files:
            logger.log_info("Nessun file G03 trovato")
            return

        query_total = ''
        processed_files = 0
        total_records = 0

        for file in g03_files:
            file_path = os.path.join(folder_path, file)

            try:
                # Log file prima di elaborarlo
                logger.log_file_processed(file_path, "CSV G03 input")

                lista = []
                with open(file_path) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    line_count = 0
                    headers = None

                    for row in csv_reader:
                        if line_count == 0:
                            headers = row
                        elif line_count == 1:
                            pass  # Salta seconda riga se necessario
                        else:
                            if len(row) > 4:
                                lista.append(row[4])
                            else:
                                logger.log_warning(f"Riga {line_count} in {file} ha meno di 5 colonne")
                        line_count += 1

                    # Log analisi CSV con dettagli
                    logger.log_csv_analysis(file_path, len(lista), headers)

                    # Estrae data dal nome file
                    try:
                        date_part = file.split('_')[2].replace('.csv', '')
                        logger.log_info(f"Data estratta da {file}: {date_part}")
                    except IndexError:
                        date_part = datetime.datetime.now().strftime('%Y%m%d')
                        logger.log_warning(f"Impossibile estrarre data da {file}, uso data corrente: {date_part}")

                    if lista:
                        g03_result_string = "'" + "', '".join(map(str, lista)) + "'"
                        query = f"""update voce_pratica set des_val_voce = '{date_part}'
where cod_pratica in (
{g03_result_string}) 
and cod_voce_element like 'GAUI03';
commit;
quit;

"""
                        query_total += query
                        total_records += len(lista)
                        processed_files += 1

                        logger.log_info(f"File {file} elaborato: {len(lista)} record, data: {date_part}")
                        logger.update_stats(records_processed=len(lista))
                    else:
                        logger.log_warning(f"Nessun record valido trovato in {file}")

            except Exception as e:
                logger.log_error(f"Errore elaborazione {file}", e)
                continue

        if query_total:
            # Salva query nel file
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\update_query\\G03_Update_{timestamp}.txt"

            with open(filename, 'w') as file:
                file.write(query_total)

            # Log query generata
            logger.log_query_generated(filename, "UPDATE G03")
            logger.update_stats(queries_generated=1, files_created=1)

            logger.log_info(
                f"G03 completato: {processed_files}/{len(g03_files)} file elaborati, {total_records} record totali")
        else:
            logger.log_warning("Nessuna query generata per G03")

    except Exception as e:
        logger.log_error("Errore write_files_starting_with_G03", e)
        raise


def write_files_starting_with_G04():
    """Elabora file CSV che iniziano con G04 e genera query UPDATE"""
    logger.log_start("Elaborazione file G04 - Aggiornamento voce_pratica GAUI04")

    try:
        folder_path = r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Unareti\LOG G03 E G04"

        # Lista file G04
        try:
            files_in_folder = os.listdir(folder_path)
            g04_files = [file for file in files_in_folder if file.startswith('G04') and file.endswith('.csv')]

            logger.log_info(f"File G04 trovati: {len(g04_files)}")
            if g04_files:
                for file in g04_files:
                    logger.log_info(f"  - {file}")
        except Exception as e:
            logger.log_error(f"Errore lettura directory: {e}")
            return

        if not g04_files:
            logger.log_info("Nessun file G04 trovato")
            return

        query_total = ''
        processed_files = 0
        total_records = 0

        for file in g04_files:
            file_path = os.path.join(folder_path, file)

            try:
                # Log file prima di elaborarlo
                logger.log_file_processed(file_path, "CSV G04 input")

                lista = []
                with open(file_path) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    line_count = 0
                    headers = None

                    for row in csv_reader:
                        if line_count == 0:
                            headers = row
                        elif line_count == 1:
                            pass  # Salta seconda riga se necessario
                        else:
                            if len(row) > 2:
                                lista.append(row[2])  # G04 usa colonna 2
                            else:
                                logger.log_warning(f"Riga {line_count} in {file} ha meno di 3 colonne")
                        line_count += 1

                    # Log analisi CSV con dettagli
                    logger.log_csv_analysis(file_path, len(lista), headers)

                    # Estrae data dal nome file
                    try:
                        date_part = file.split('_')[2].replace('.csv', '')
                        logger.log_info(f"Data estratta da {file}: {date_part}")
                    except IndexError:
                        date_part = datetime.datetime.now().strftime('%Y%m%d')
                        logger.log_warning(f"Impossibile estrarre data da {file}, uso data corrente: {date_part}")

                    if lista:
                        g04_result_string = "'" + "', '".join(map(str, lista)) + "'"
                        query = f"""update voce_pratica set des_val_voce = '{date_part}'
where cod_pratica in (
{g04_result_string}) 
and cod_voce_element like 'GAUI04';
commit;
quit;

"""
                        query_total += query
                        total_records += len(lista)
                        processed_files += 1

                        logger.log_info(f"File {file} elaborato: {len(lista)} record, data: {date_part}")
                        logger.update_stats(records_processed=len(lista))
                    else:
                        logger.log_warning(f"Nessun record valido trovato in {file}")

            except Exception as e:
                logger.log_error(f"Errore elaborazione {file}", e)
                continue

        if query_total:
            # Salva query nel file
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\update_query\\G04_Update_{timestamp}.txt"

            with open(filename, 'w') as file:
                file.write(query_total)

            # Log query generata
            logger.log_query_generated(filename, "UPDATE G04")
            logger.update_stats(queries_generated=1, files_created=1)

            logger.log_info(
                f"G04 completato: {processed_files}/{len(g04_files)} file elaborati, {total_records} record totali")
        else:
            logger.log_warning("Nessuna query generata per G04")

    except Exception as e:
        logger.log_error("Errore write_files_starting_with_G04", e)
        raise


def move_files():
    """Sposta file CSV elaborati nella cartella old"""
    logger.log_start("Spostamento file CSV elaborati in cartella archivio")

    try:
        source_folder = r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Unareti\LOG G03 E G04"
        destination_folder = r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Unareti\LOG G03 E G04\old"

        # Verifica cartella source
        if not os.path.exists(source_folder):
            logger.log_error(f"Cartella source non trovata: {source_folder}")
            return

        # Crea cartella destination se non esiste
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            logger.log_info(f"Cartella destination creata: {destination_folder}")

        # Lista file da spostare
        files = os.listdir(source_folder)
        csv_files = [f for f in files if f.endswith(".csv")]

        if not csv_files:
            logger.log_info("Nessun file CSV da spostare")
            return

        logger.log_info(f"File CSV da spostare: {len(csv_files)}")

        moved_files = 0
        errors = 0

        for file in csv_files:
            try:
                source_path = os.path.join(source_folder, file)
                destination_path = os.path.join(destination_folder, file)

                # Log file prima di spostarlo
                logger.log_file_processed(source_path, "file to move")

                # Sposta il file
                shutil.move(source_path, destination_path)

                # Log file spostato
                logger.log_file_processed(destination_path, "file moved", {"moved_from": source_path})

                moved_files += 1
                logger.log_info(f"Spostato: {file}")

            except Exception as e:
                errors += 1
                logger.log_error(f"Errore spostamento {file}", e)

        logger.log_info(f"File spostati: {moved_files}, Errori: {errors}")
        logger.update_stats(files_moved=moved_files, move_errors=errors)

        if errors == 0:
            logger.log_info("Tutti i file CSV spostati con successo")
        else:
            logger.log_warning(f"{errors} errori durante lo spostamento")

    except Exception as e:
        logger.log_error("Errore move_files", e)
        raise


def main_execution():
    """Esecuzione principale del flusso 91"""
    logger.log_start("Esecuzione completa Flusso 91 - Gestione log G03 e G04")

    try:
        steps_completed = 0
        total_steps = 3

        # Step 1: Elaborazione G03
        logger.log_info("STEP 1/3: Controllo ed elaborazione file G03...")
        try:
            cerca_file_e_controlla_testo_csv(
                r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Unareti\LOG G03 E G04",
                "G03",
                write_files_starting_with_G03
            )
            steps_completed += 1
            logger.log_info("✅ Step 1 completato")
        except Exception as e:
            logger.log_error("❌ Errore Step 1 (G03)", e)

        # Step 2: Elaborazione G04
        logger.log_info("STEP 2/3: Controllo ed elaborazione file G04...")
        try:
            cerca_file_e_controlla_testo_csv(
                r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Unareti\LOG G03 E G04",
                "G04",
                write_files_starting_with_G04
            )
            steps_completed += 1
            logger.log_info("✅ Step 2 completato")
        except Exception as e:
            logger.log_error("❌ Errore Step 2 (G04)", e)

        # Step 3: Spostamento file
        logger.log_info("STEP 3/3: Spostamento file elaborati...")
        try:
            move_files()
            steps_completed += 1
            logger.log_info("✅ Step 3 completato")
        except Exception as e:
            logger.log_error("❌ Errore Step 3 (spostamento)", e)

        # Riepilogo finale
        logger.update_stats(steps_completed=steps_completed, total_steps=total_steps)

        if steps_completed == total_steps:
            logger.log_info(f"🎉 Flusso 91 completato con successo: {steps_completed}/{total_steps} step eseguiti")
        else:
            logger.log_warning(f"⚠️ Flusso 91 parzialmente completato: {steps_completed}/{total_steps} step eseguiti")

    except Exception as e:
        logger.log_error("Errore esecuzione principale Flusso 91", e)
        raise
    finally:
        # Il log_end() salva automaticamente il summary JSON
        logger.log_end()


# Esecuzione principale
if __name__ == "__main__":
    try:
        print("🚀 Avvio Flusso 91 - Gestione Log G03 e G04")
        print("=" * 60)
        print("📁 Log salvati in: \\\\group.local\\...\\Unareti\\Logs\\YYYY\\MM\\F91\\")
        print("=" * 60)
        
        main_execution()

        print("\n✅ Flusso 91 completato!")
        print("📊 Controlla i log per i dettagli completi")
        print("📄 Summary JSON generato automaticamente")

    except KeyboardInterrupt:
        print("\n⏹️  Esecuzione interrotta dall'utente")
        logger.log_error("Esecuzione interrotta dall'utente")
        logger.log_end()
    except Exception as e:
        print(f"\n❌ Errore durante esecuzione Flusso 91: {e}")
        logger.log_error("Errore critico durante esecuzione", e)
        logger.log_end()
        import traceback

        traceback.print_exc()
        raise