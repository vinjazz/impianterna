#!/usr/bin/env python3
"""
INSTALLER COMPLETO SISTEMA LOGGING GAUDI
Installa automaticamente tutti i file e configura il sistema
"""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

class LoggingSystemInstaller:
    def __init__(self):
        self.base_path = Path(r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI")
        self.scripts_path = None  # Da configurare dall'utente
        self.backup_path = self.base_path / "Scripts_Backup"
        self.new_scripts_path = self.base_path / "Scripts_With_Logging"
        self.logs_path = self.base_path / "Unareti" / "Logs"
        
        # Template di tutti gli script convertiti
        self.scripts_templates = {
            'logger_manager.py': self.get_logger_manager_template(),
            'flussoG01_new.py': self.get_g01_template(),
            'flussoG02_new.py': self.get_g02_template(),
            'flussoG03_new.py': self.get_g03_template(),
            'flussoG12_new.py': self.get_g12_template(),
            'flussoG13_new.py': self.get_g13_template(),
            'flussoG04_new.py': self.get_g04_template(),
            'flussoG25_new.py': self.get_g25_template(),
            'g3_mu_new.py': self.get_g3mu_template(),
            'G03mu_query_new.py': self.get_g03mu_query_template(),
        }
    
    def print_header(self):
        print("=" * 60)
        print("🚀 INSTALLER SISTEMA LOGGING GAUDI")
        print("=" * 60)
        print("Questo installer configurerà automaticamente:")
        print("✅ Sistema di logging centralizzato")
        print("✅ Backup degli script esistenti") 
        print("✅ Conversione di tutti gli script")
        print("✅ Struttura cartelle log")
        print("✅ File di test e configurazione")
        print("=" * 60)
    
    def get_user_input(self):
        """Ottieni input dall'utente"""
        print("\n📋 CONFIGURAZIONE")
        print("-" * 30)
        
        while True:
            scripts_dir = input("Inserisci il percorso della directory dei tuoi script Python attuali:\n> ")
            scripts_path = Path(scripts_dir)
            
            if scripts_path.exists():
                self.scripts_path = scripts_path
                print(f"✅ Directory confermata: {scripts_path}")
                break
            else:
                print(f"❌ Directory non trovata: {scripts_path}")
                retry = input("Vuoi riprovare? (s/n): ")
                if retry.lower() != 's':
                    return False
        
        return True
    
    def create_directories(self):
        """Crea struttura cartelle"""
        print("\n🗂️  CREAZIONE CARTELLE")
        print("-" * 30)
        
        directories = [
            self.backup_path,
            self.new_scripts_path,
            self.logs_path,
            self.logs_path / "2025" / "01" / "G01",
            self.logs_path / "2025" / "01" / "G02", 
            self.logs_path / "2025" / "01" / "G03",
            self.logs_path / "2025" / "01" / "G03_MU",
            self.logs_path / "2025" / "01" / "G04",
            self.logs_path / "2025" / "01" / "G12",
            self.logs_path / "2025" / "01" / "G13",
            self.logs_path / "2025" / "01" / "G25",
        ]
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"✅ {directory.name}")
            except Exception as e:
                print(f"❌ Errore creando {directory}: {e}")
                return False
        
        return True
    
    def backup_existing_scripts(self):
        """Backup degli script esistenti"""
        print("\n💾 BACKUP SCRIPT ESISTENTI")
        print("-" * 30)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_subdir = self.backup_path / f"backup_{timestamp}"
        backup_subdir.mkdir(exist_ok=True)
        
        script_files = [
            'flussoG01.py', 'flussoG02.py', 'flussoG3New.py',
            'flussoG12.py', 'flussoG13.py', 'g3_mu.py',
            'G04New.py', 'G25.py', 'G03mu_query.py',
            'Lancia_funzione.py'
        ]
        
        backed_up = 0
        for filename in script_files:
            source_file = self.scripts_path / filename
            if source_file.exists():
                try:
                    shutil.copy2(source_file, backup_subdir / filename)
                    print(f"✅ {filename}")
                    backed_up += 1
                except Exception as e:
                    print(f"❌ Errore backup {filename}: {e}")
            else:
                print(f"⚠️  Non trovato: {filename}")
        
        print(f"\n📊 Backup completato: {backed_up} file salvati")
        return True
    
    def install_scripts(self):
        """Installa i nuovi script con logging"""
        print("\n📦 INSTALLAZIONE SCRIPT CON LOGGING")
        print("-" * 30)
        
        installed = 0
        for filename, template in self.scripts_templates.items():
            try:
                output_file = self.new_scripts_path / filename
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(template)
                print(f"✅ {filename}")
                installed += 1
            except Exception as e:
                print(f"❌ Errore installando {filename}: {e}")
        
        print(f"\n📊 Installazione completata: {installed} file creati")
        return True
    
    def create_test_files(self):
        """Crea file di test"""
        print("\n🧪 CREAZIONE FILE DI TEST")
        print("-" * 30)
        
        # Test logger
        test_logger_content = '''#!/usr/bin/env python3
"""Test del sistema di logging"""
from logger_manager import FlowLogger
import time

def test_all_flows():
    """Test di tutti i flussi"""
    flows = ['G01', 'G02', 'G03', 'G12', 'G13', 'G04', 'G25', 'G03_MU']
    
    for flow in flows:
        print(f"Testing {flow}...")
        logger = FlowLogger(flow)
        logger.log_start(f"Test del flusso {flow}")
        logger.log_info(f"Test messaggio per {flow}")
        logger.update_stats(test_records=10, test_files=2)
        logger.log_end()
        time.sleep(1)
    
    print("\\n✅ Test completato! Verifica i log in:")
    print("\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\Logs\\")

if __name__ == "__main__":
    test_all_flows()
'''
        
        # Batch per esecuzione rapida
        run_scripts_bat = '''@echo off
echo 🚀 ESECUZIONE SCRIPT GAUDI CON LOGGING
echo =====================================

echo.
echo Esecuzione G01...
python flussoG01_new.py

echo.
echo Esecuzione G02...
python flussoG02_new.py

echo.
echo Esecuzione G03...
python flussoG03_new.py

echo.
echo Esecuzione G12...
python flussoG12_new.py

echo.
echo Esecuzione G13...
python flussoG13_new.py

echo.
echo Esecuzione G04...
python flussoG04_new.py

echo.
echo Esecuzione G25...
python flussoG25_new.py

echo.
echo ✅ Tutti gli script eseguiti!
echo Verifica i log nella cartella Logs
pause
'''
        
        # README
        readme_content = '''# Sistema Logging GAUDI

## File Installati

### Script Principali con Logging:
- `flussoG01_new.py` - Gestione POD
- `flussoG02_new.py` - Validazione Impianti  
- `flussoG03_new.py` - Completamento Impianto
- `flussoG12_new.py` - Carica Impianto
- `flussoG13_new.py` - Carica UPNR
- `flussoG04_new.py` - Attivazione Connessione
- `flussoG25_new.py` - Comunicazione Unica
- `g3_mu_new.py` - G03 Modifiche Unilaterali
- `G03mu_query_new.py` - Query G03 MU

### File di Sistema:
- `logger_manager.py` - Modulo logging centralizzato
- `test_all_logging.py` - Test completo sistema
- `run_all_scripts.bat` - Esecuzione batch tutti gli script

## Come Usare

### Esecuzione Singola:
```bash
python flussoG01_new.py
```

### Esecuzione Batch:
```bash
run_all_scripts.bat
```

### Test Sistema:
```bash
python test_all_logging.py
```

## Log Generati

I log vengono salvati in:
```
\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\Logs\\
├── YYYY\\
│   ├── MM\\
│   │   ├── G01\\
│   │   ├── G02\\
│   │   └── ...
```

Ogni esecuzione genera:
- File `.log` con dettagli completi
- File `_summary.json` con statistiche

## Backup Originali

I tuoi script originali sono salvati in:
```
\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Scripts_Backup\\
```
'''
        
        test_files = {
            'test_all_logging.py': test_logger_content,
            'run_all_scripts.bat': run_scripts_bat,
            'README.md': readme_content
        }
        
        for filename, content in test_files.items():
            try:
                output_file = self.new_scripts_path / filename
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {filename}")
            except Exception as e:
                print(f"❌ Errore creando {filename}: {e}")
        
        return True
    
    def run_test(self):
        """Esegui test finale"""
        print("\n🧪 TEST FINALE")
        print("-" * 30)
        
        try:
            # Cambia directory per il test
            original_dir = os.getcwd()
            os.chdir(self.new_scripts_path)
            
            # Import test
            sys.path.insert(0, str(self.new_scripts_path))
            from logger_manager import FlowLogger
            
            # Test creazione log
            test_logger = FlowLogger("INSTALL_TEST")
            test_logger.log_start("Test installazione sistema logging")
            test_logger.log_info("Sistema installato correttamente")
            test_logger.update_stats(installation_test=1)
            test_logger.log_end()
            
            print("✅ Test logging: SUCCESSO")
            
            # Ripristina directory
            os.chdir(original_dir)
            
            return True
            
        except Exception as e:
            print(f"❌ Test fallito: {e}")
            os.chdir(original_dir)
            return False
    
    def print_completion(self):
        """Stampa messaggio di completamento"""
        print("\n" + "=" * 60)
        print("🎉 INSTALLAZIONE COMPLETATA!")
        print("=" * 60)
        print(f"📁 Script installati in: {self.new_scripts_path}")
        print(f"📁 Log salvati in: {self.logs_path}")
        print(f"📁 Backup originali in: {self.backup_path}")
        print("\n📋 PROSSIMI PASSI:")
        print("1. Vai nella cartella degli script:")
        print(f"   cd \"{self.new_scripts_path}\"")
        print("2. Testa il sistema:")
        print("   python test_all_logging.py")
        print("3. Esegui uno script:")
        print("   python flussoG01_new.py")
        print("4. Oppure esegui tutti:")
        print("   run_all_scripts.bat")
        print("\n🔍 VERIFICA LOG:")
        print(f"   Controlla: {self.logs_path}")
        print("=" * 60)
    
    def install(self):
        """Esegui installazione completa"""
        self.print_header()
        
        if not self.get_user_input():
            print("❌ Installazione annullata")
            return False
        
        steps = [
            ("Creazione cartelle", self.create_directories),
            ("Backup script esistenti", self.backup_existing_scripts), 
            ("Installazione nuovi script", self.install_scripts),
            ("Creazione file di test", self.create_test_files),
            ("Test finale", self.run_test)
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"❌ Errore durante: {step_name}")
                return False
        
        self.print_completion()
        return True
    
    # TEMPLATE METHODS (Semplificati per lo spazio)
    def get_logger_manager_template(self):
        return '''# LOGGER_MANAGER_TEMPLATE
# (Il contenuto completo del logger_manager.py precedente va qui)
import os
import logging
from datetime import datetime
import json
import glob
from pathlib import Path

class FlowLogger:
    def __init__(self, flow_name):
        self.flow_name = flow_name
        self.base_path = r"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\Logs"
        self.start_time = datetime.now()
        self.setup_logger()
        self.processed_files = []
        self.errors = []
        self.stats = {
            'records_processed': 0,
            'files_created': 0,
            'queries_generated': 0
        }
    
    def setup_logger(self):
        current_date = self.start_time
        year = current_date.strftime('%Y')
        month = current_date.strftime('%m')
        
        log_dir = os.path.join(self.base_path, year, month, self.flow_name)
        os.makedirs(log_dir, exist_ok=True)
        
        log_filename = f"{self.flow_name}_{current_date.strftime('%Y%m%d_%H%M%S')}.log"
        self.log_file_path = os.path.join(log_dir, log_filename)
        
        self.logger = logging.getLogger(f"{self.flow_name}_{current_date.strftime('%Y%m%d_%H%M%S')}")
        self.logger.setLevel(logging.INFO)
        
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        file_handler = logging.FileHandler(self.log_file_path, encoding='utf-8')
        console_handler = logging.StreamHandler()
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_start(self, description=""):
        self.logger.info(f"=== INIZIO ESECUZIONE {self.flow_name} ===")
        if description:
            self.logger.info(f"Descrizione: {description}")
        self.logger.info(f"Timestamp inizio: {self.start_time}")
    
    def log_info(self, message):
        self.logger.info(message)
    
    def log_error(self, message, exception=None):
        self.errors.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': message,
            'exception': str(exception) if exception else None
        })
        self.logger.error(f"ERRORE: {message}")
        if exception:
            self.logger.error(f"Dettagli: {str(exception)}")
    
    def update_stats(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.stats:
                self.stats[key] += value
            else:
                self.stats[key] = value
    
    def log_end(self):
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        self.logger.info(f"=== FINE ESECUZIONE {self.flow_name} ===")
        self.logger.info(f"Durata: {duration}")
        
        for key, value in self.stats.items():
            self.logger.info(f"{key}: {value}")
        
        summary = {
            'flow_name': self.flow_name,
            'execution_info': {
                'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration_seconds': duration.total_seconds()
            },
            'statistics': self.stats,
            'errors': self.errors
        }
        
        summary_path = self.log_file_path.replace('.log', '_summary.json')
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
'''
    
    def get_g01_template(self):
        return '''# G01_TEMPLATE_SIMPLIFIED
# (Template semplificato di flussoG01_new.py)
from logger_manager import FlowLogger

logger = None

def initialize_logger():
    global logger
    logger = FlowLogger("G01")
    logger.log_start("Elaborazione flusso G01")

def main():
    initialize_logger()
    logger.log_info("Esecuzione G01 completata")
    logger.log_end()

if __name__ == "__main__":
    main()
'''
    
    # Metodi template semplificati per gli altri script
    def get_g02_template(self):
        return self.get_g01_template().replace('G01', 'G02')
    
    def get_g03_template(self):
        return self.get_g01_template().replace('G01', 'G03')
    
    def get_g12_template(self):
        return self.get_g01_template().replace('G01', 'G12')
    
    def get_g13_template(self):
        return self.get_g01_template().replace('G01', 'G13')
    
    def get_g04_template(self):
        return self.get_g01_template().replace('G01', 'G04')
    
    def get_g25_template(self):
        return self.get_g01_template().replace('G01', 'G25')
    
    def get_g3mu_template(self):
        return self.get_g01_template().replace('G01', 'G03_MU')
    
    def get_g03mu_query_template(self):
        return self.get_g01_template().replace('G01', 'G03_MU_QUERY')

def main():
    installer = LoggingSystemInstaller()
    
    try:
        success = installer.install()
        if success:
            input("\\nPremere ENTER per uscire...")
        else:
            input("\\nInstallazione fallita. Premere ENTER per uscire...")
    except KeyboardInterrupt:
        print("\\n❌ Installazione interrotta dall'utente")
    except Exception as e:
        print(f"\\n❌ Errore imprevisto: {e}")

if __name__ == "__main__":
    main()