import os
import logging
from datetime import datetime
import json
from pathlib import Path

class FlowLogger:
    def __init__(self, flow_name):
        self.flow_name = flow_name
        self.base_path = r"\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\LD_Reti\Logs"
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
        """Setup del logger con struttura cartelle Anno/Mese/Flusso"""
        current_date = self.start_time
        year = current_date.strftime('%Y')
        month = current_date.strftime('%m')
        
        # Crea struttura cartelle
        log_dir = os.path.join(self.base_path, year, month, self.flow_name)
        os.makedirs(log_dir, exist_ok=True)
        
        # Nome file log con timestamp
        log_filename = f"{self.flow_name}_{current_date.strftime('%Y%m%d_%H%M%S')}.log"
        self.log_file_path = os.path.join(log_dir, log_filename)
        
        # Configura logger
        self.logger = logging.getLogger(f"{self.flow_name}_{current_date.strftime('%Y%m%d_%H%M%S')}")
        self.logger.setLevel(logging.INFO)
        
        # Rimuovi handler esistenti per evitare duplicati
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_start(self, description=""):
        """Log inizio esecuzione"""
        self.logger.info(f"=== INIZIO ESECUZIONE {self.flow_name} ===")
        if description:
            self.logger.info(f"Descrizione: {description}")
        self.logger.info(f"Timestamp inizio: {self.start_time}")
    
    def log_file_processed(self, file_path, file_type="input", additional_info=None):
        """Log file processato con timestamp di creazione"""
        try:
            if os.path.exists(file_path):
                # Ottieni timestamp di creazione e modifica
                creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                file_size = os.path.getsize(file_path)
                
                file_info = {
                    'path': file_path,
                    'name': os.path.basename(file_path),
                    'type': file_type,
                    'creation_time': creation_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'modification_time': modification_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'size_bytes': file_size,
                    'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                if additional_info:
                    file_info.update(additional_info)
                
                self.processed_files.append(file_info)
                
                self.logger.info(f"File processato: {os.path.basename(file_path)}")
                self.logger.info(f"  - Tipo: {file_type}")
                self.logger.info(f"  - Data creazione: {file_info['creation_time']}")
                self.logger.info(f"  - Data modifica: {file_info['modification_time']}")
                self.logger.info(f"  - Dimensione: {file_size} bytes")
                
                if additional_info:
                    for key, value in additional_info.items():
                        self.logger.info(f"  - {key}: {value}")
            else:
                self.logger.warning(f"File non trovato: {file_path}")
        except Exception as e:
            self.log_error(f"Errore nel logging del file {file_path}: {str(e)}")
    
    def log_csv_analysis(self, csv_path, row_count, columns=None):
        """Log analisi file CSV"""
        additional_info = {
            'row_count': row_count,
            'columns': columns if columns else 'N/A'
        }
        self.log_file_processed(csv_path, "CSV input", additional_info)
        self.stats['records_processed'] += row_count
    
    def log_xml_generated(self, xml_path, element_count=None):
        """Log XML generato"""
        additional_info = {}
        if element_count:
            additional_info['element_count'] = element_count
        self.log_file_processed(xml_path, "XML output", additional_info)
        self.stats['files_created'] += 1
    
    def log_query_generated(self, query_path, query_type="update"):
        """Log query generata"""
        additional_info = {'query_type': query_type}
        self.log_file_processed(query_path, "SQL query", additional_info)
        self.stats['queries_generated'] += 1
    
    def log_error(self, error_message, exception=None):
        """Log errore"""
        error_info = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': error_message,
            'exception': str(exception) if exception else None
        }
        self.errors.append(error_info)
        
        self.logger.error(f"ERRORE: {error_message}")
        if exception:
            self.logger.error(f"Dettagli eccezione: {str(exception)}")
    
    def log_info(self, message):
        """Log messaggio informativo"""
        self.logger.info(message)
    
    def log_warning(self, message):
        """Log warning"""
        self.logger.warning(message)
    
    def update_stats(self, **kwargs):
        """Aggiorna statistiche"""
        for key, value in kwargs.items():
            if key in self.stats:
                self.stats[key] += value
            else:
                self.stats[key] = value
    
    def log_end(self):
        """Log fine esecuzione con statistiche"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        self.logger.info(f"=== FINE ESECUZIONE {self.flow_name} ===")
        self.logger.info(f"Timestamp fine: {end_time}")
        self.logger.info(f"Durata esecuzione: {duration}")
        
        # Statistiche
        self.logger.info("=== STATISTICHE ===")
        for key, value in self.stats.items():
            self.logger.info(f"{key}: {value}")
        
        # File processati
        self.logger.info(f"Totale file processati: {len(self.processed_files)}")
        
        # Errori
        if self.errors:
            self.logger.info(f"Errori riscontrati: {len(self.errors)}")
            for error in self.errors:
                self.logger.error(f"  - {error['timestamp']}: {error['message']}")
        else:
            self.logger.info("Nessun errore riscontrato")
        
        # Salva summary JSON
        self.save_summary()
    
    def save_summary(self):
        """Salva summary in formato JSON"""
        summary = {
            'flow_name': self.flow_name,
            'execution_info': {
                'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'duration_seconds': (datetime.now() - self.start_time).total_seconds()
            },
            'statistics': self.stats,
            'processed_files': self.processed_files,
            'errors': self.errors
        }
        
        summary_path = self.log_file_path.replace('.log', '_summary.json')
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Summary salvato in: {summary_path}")
        except Exception as e:
            self.logger.error(f"Errore nel salvataggio summary: {str(e)}")

def get_latest_file_in_directory(directory, pattern="*.xml"):
    """Ottiene il file più recente in una directory"""
    import glob
    try:
        files = glob.glob(os.path.join(directory, pattern))
        if not files:
            return None
        return max(files, key=os.path.getctime)
    except Exception:
        return None