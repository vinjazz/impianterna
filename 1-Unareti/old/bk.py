#!/usr/bin/env python3
"""
Test del sistema di logging per verificare che tutto funzioni
"""
from logger_manager import FlowLogger
import os
import time


def test_logger():
    print("🔄 Test del sistema di logging...")

    try:
        # Inizializza logger di test
        logger = FlowLogger("TEST")
        logger.log_start("Test del sistema di logging")

        # Test log base
        logger.log_info("Questo è un messaggio di test")
        logger.log_warning("Questo è un warning di test")

        # Test statistiche
        logger.update_stats(test_records=100, test_files=3)

        # Simula processamento file
        test_file = __file__  # Usa questo stesso file come test
        logger.log_file_processed(test_file, "Python script", {'test': True})

        # Test completamento
        logger.log_info("Test completato con successo")
        logger.log_end()

        print("✅ Test completato!")
        print(f"Verifica che sia stato creato il log in:")
        print(
            f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\Logs\\")

        return True

    except ImportError as e:
        print(f"❌ Errore di importazione: {e}")
        print("Verifica che logger_manager.py sia nella stessa directory")
        return False

    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        return False


def check_log_creation():
    """Verifica che i log siano stati creati"""
    import glob
    from datetime import datetime

    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')

    log_pattern = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\Logs\\{year}\\{month}\\TEST\\*.log"

    log_files = glob.glob(log_pattern)

    if log_files:
        print(f"✅ Trovati {len(log_files)} file di log:")
        for log_file in log_files:
            print(f"  - {os.path.basename(log_file)}")

        # Mostra contenuto del log più recente
        latest_log = max(log_files, key=os.path.getctime)
        print(f"\n📋 Contenuto del log più recente:")
        print("-" * 50)

        try:
            with open(latest_log, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"Errore nella lettura del log: {e}")

    else:
        print(f"⚠️  Nessun file di log trovato nel pattern: {log_pattern}")
        print("Verifica che le cartelle siano state create correttamente")


if __name__ == "__main__":
    print("🧪 Test Sistema Logging GAUDI")
    print("=" * 40)

    # Esegui test
    success = test_logger()

    if success:
        print("\n" + "=" * 40)
        time.sleep(2)  # Aspetta che i file vengano scritti
        check_log_creation()

    print("\n" + "=" * 40)
    input("Premi ENTER per continuare...")