import traceback
import G04New_reti
import flussoG01_duereti
import flussoG02_reti
import flussoG13_duereti
import flussoG12_reti
import flussoG13_reti
import flussoG3New_reti
import flussoG3New_duereti
import g3_mu_reti
import g3_mu_duereti
import flussoG12_duereti
import flussoG02_duereti
from flussoG01 import flussoG01New
from flussoG12 import flussoG12New
from flussoG02 import flussoG02
from g3_mu import g03_MU
from flussoG3New import g03
from G04New import flussoG04
from G25 import flussoG25
from flussoG13 import flussoG13
from flussoG01_reti import flussoG01Reti
from write_query import write_files_starting_with_G03
from write_query import write_files_starting_with_G04
from write_query import g01_query
from write_query import g01_controllo_query
from write_query import g12_controllo_query
from write_query_reti import g01_query_reti
from write_query_duereti import g01_query_duereti
from write_query_reti import g01_controllo_query_reti
from write_query_duereti import g01_controllo_query_duereti
from write_query_duereti import g12_controllo_query_duereti
from write_query_reti import g12_controllo_query_reti
from write_query_reti import g12_query_reti
from write_query_duereti import g12_query_duereti
from write_query_reti import g02_query_reti
from write_query_duereti import g02_query_duereti
from write_query_reti import g13_query_reti
from write_query_duereti import g13_query_duereti
from write_query_reti import g03_MU_query_reti
from write_query_duereti import g03_MU_query_duereti
from write_query_reti import write_files_starting_with_G03_reti
from write_query_duereti import write_files_starting_with_G04_duereti
from write_query_duereti import write_files_starting_with_G03_duereti
from write_query_reti import write_files_starting_with_G04_reti
from write_query import g12_query
from write_query import g02_query
from write_query import g13_query
from write_query import g03_MU_query
import write_query
import write_query_reti
import write_query_duereti
import G04New_duereti
import csv
import os
import xml.etree.ElementTree as ET

def cerca_file_e_controlla_testo(cartella, prefisso, funzione_da_lanciare):

    # Scorre i file nella cartella
    for nome_file in os.listdir(cartella):
        # Controlla se il nome del file inizia con il prefisso e termina con .xml
        if nome_file.startswith(prefisso) and nome_file.endswith('.xml'):
            percorso_file = os.path.join(cartella, nome_file)
            try:
                # Tenta di fare il parsing del file XML
                tree = ET.parse(percorso_file)
                root = tree.getroot()

                # Controlla se il file contiene testo
                if any(elem.text.strip() for elem in root.iter() if elem.text):  # Controlla se c'è testo non vuoto
                    funzione_da_lanciare()
                else:
                    print(f"Il file {nome_file} non contiene testo.")
            except ET.ParseError:
                print(f"Errore nel parsing del file {nome_file}. Non è un file XML valido.")
def cerca_file_e_controlla_testo_csv(cartella, prefisso, funzione_da_lanciare):
    # Cerca file che inizia con il prefisso e termina con .csv
    trovato = False  # Flag per indicare se un file è stato trovato
    for nome_file in os.listdir(cartella):
        if nome_file.startswith(prefisso) and nome_file.endswith('.csv'):
            trovato = True
            percorso_file = os.path.join(cartella, nome_file)

            # Verifica se il file contiene testo
            with open(percorso_file, 'r', newline='', encoding='utf-8') as file_csv:
                lettore_csv = csv.reader(file_csv)
                try:
                    prima_riga = next(lettore_csv)  # Legge la prima riga
                    if any(prima_riga):  # Controlla se la prima riga contiene testo
                        print(f"Il file {nome_file} contiene testo. Lancio la funzione.")
                        funzione_da_lanciare()
                    else:
                        print(f"Il file {nome_file} non contiene testo.")
                except StopIteration:
                    # Se il file è vuoto o non contiene righe
                    print(f"Il file {nome_file} è vuoto.")
            break  # Esce dal ciclo dopo aver trovato il primo file che soddisfa i criteri

    if not trovato:
        print(f"Nessun file CSV che inizia con '{prefisso}' è stato trovato nella cartella {cartella}.")
def menu():
    try:
        flusso = input(""" Elenco flussi disponibili:
                       1- G01
                       2- scrivi query g03 MU
                       3- G12 
                       4- G02 
                       5- G13 
                       6- G03 PER MU 
                       7- G03
                       8- G04
                       9- G25
                       -------------------------------------------
                       10- G01 Reti+
                       11- G12 Reti+
                       12- G02 Reti+
                       13- G13 Reti+
                       14- G03 reti+
                       15- G03 MU reti+
                       16- G04 reti+
                       17- G25 reti+
                       18- scrivi query g03 MU reti+
                       -------------------------------------------
                       20- G01 Duereti
                       21- G12 Duereti
                       22- G02 Duereti
                       23- G13 Duereti
                       24- G03 Duereti
                       25- G03 MU Duereti
                       26- G04 Duereti
                       27- G25 Duereti
                       28- scrivi query g03 MU Duereti
                       -------------------------------------------
                       
                       91- Scrivi le query G03 e G04
                       92 Sposta query in old
                       -
                       94- Reti+ Scrivi le query G03 e G04
                       95- Reti+ Sposta query in old
                       
                       96- Duereti Scrivi le query G03 e G04
                       97- Duereti Sposta query in old
                       
                       -----------------------------------------------------
                       
                       seleziona il tipo di flusso da eseguire: """)
        flusso = int(flusso)
        if flusso == 1:
            flussoG01New()
            cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI", 'G01', g01_query)
            cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI", 'G01', g01_controllo_query)

        elif flusso == 2:
            write_query.write_G03_MU_query()
        elif flusso == 3:
            flussoG12New()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI", 'G12',g12_query)
            cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI", 'G12',g12_controllo_query)
        elif flusso == 4:
            print("ricordati di estrarre e inserire il file dei registrati nella cartella")
            input("premi invio una volta effettuata l'operazione")
            flussoG02()
            write_query.gestisci_file_g02()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI", 'G02',
                g02_query)
        elif flusso == 5:
            print("ricordati di estrarre e inserire il file dei registrati nella cartella")
            input("premi invio una volta effettuata l'operazione")
            flussoG13()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI", 'G13',
                g13_query)

        elif flusso == 6:
            print("ricordati di estrarre e inserire il file dei validati nella cartella")
            input("premi invio una volta effettuata l'operazione")
            g03_MU()

            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI", 'G03',
                g03_MU_query)

        elif flusso == 7:
            print("ricordati di estrarre e inserire il file dei Realizzati nella cartella")
            input("premi invio una volta effettuata l'operazione")
            g03()

        elif flusso == 8:
            print("ricordati di estrarre e inserire il file dei Esercibili nella cartella")
            input("premi invio una volta effettuata l'operazione")
            flussoG04()

        elif flusso == 9:
            flussoG25()
        #################################################################################################RETI+######################################################################################
        elif flusso == 10:
            flussoG01Reti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G01',
                g01_query_reti)

            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G01',
                g01_controllo_query_reti)
        elif flusso == 11:
            flussoG12_reti.flussoG12Reti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G12',
                g12_query_reti)

            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G12',
                g12_controllo_query_reti)
        elif flusso == 12:
            flussoG02_reti.flussoG02reti()
            write_query_reti.gestisci_file_g02_reti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G02',
                g02_query_reti)
        elif flusso == 13:
            flussoG13_reti.flussoG13reti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G13',
                g13_query_reti)
        elif flusso == 14:
            flussoG3New_reti.g03reti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G03',
                g03_MU_query_reti)
        elif flusso == 15:
            g3_mu_reti.g03_MU()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+", 'G03',
                g03_MU_query_reti)
        elif flusso == 16:
            G04New_reti.flussoG04()
        elif flusso == 18:
            write_query_reti.write_G03_MU_query_reti()
#################################################################################################DUERETI######################################################################################
        elif flusso == 20:
            flussoG01_duereti.flussoG01Duereti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G01',
                g01_query_duereti)
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G01',
                g01_controllo_query_duereti)
        elif flusso == 21:
            flussoG12_duereti.flussoG12Duereti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G12',
                g12_query_duereti)

            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G12',
                g12_controllo_query_duereti)
        elif flusso == 22:
            flussoG02_duereti.flussoG02duereti()
            write_query_duereti.gestisci_file_g02_duereti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G02',
                g02_query_duereti)
        elif flusso == 23:
            flussoG13_duereti.flussoG13duereti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G13',
                g13_query_duereti)
        elif flusso == 24:
            flussoG3New_duereti.g03duereti()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G03',
                g03_MU_query_duereti)
        elif flusso == 25:
            g3_mu_duereti.g03_MU()
            cerca_file_e_controlla_testo(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G03',
                g03_MU_query_duereti)
        elif flusso == 26:
            G04New_duereti.flussoG04()
        elif flusso == 27:
            G04New_duereti.flussoG04()
        elif flusso == 28:
            write_query_duereti.write_G03_MU_query_duereti()
        elif flusso == 90:
            pass
        elif flusso == 91:
            cerca_file_e_controlla_testo_csv("\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04", "G03", write_files_starting_with_G03)
            cerca_file_e_controlla_testo_csv("\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04", "G04", write_files_starting_with_G04)
            write_query.move_files()

        elif flusso == 92:
            write_query.move_queries()
        elif flusso == 93:
            pass
            #write_query_reti.write_query_reti()
        elif flusso == 94:
            cerca_file_e_controlla_testo_csv(
                "\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\LOG G03 E G04",
                "G03", write_files_starting_with_G03_reti)
            cerca_file_e_controlla_testo_csv(
                "\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\LOG G03 E G04",
                "G04", write_files_starting_with_G04_reti)
            write_query_reti.move_files_reti()
            #write_query_reti.write_files_starting_with_G03_reti()
        elif flusso == 95:
            write_query_reti.move_queries_reti()

        elif flusso == 96:
            cerca_file_e_controlla_testo_csv(
                "\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\LOG G03 E G04",
                "G03", write_files_starting_with_G03_duereti)
            cerca_file_e_controlla_testo_csv(
                "\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\LOG G03 E G04",
                "G04", write_files_starting_with_G04_duereti)
            write_query_duereti.move_files_duereti()
        # write_query_reti.write_files_starting_with_G03_reti()


    except Exception as e:
        print("........................................... Qualcosa è andato Storto................................................ "
              "\n verifica di aver inserito i file nelle cartelle esatte")
        print(e)
        print(traceback.print_exc())
    return menu()

menu()