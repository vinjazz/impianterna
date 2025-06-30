import os
import xml.etree.ElementTree as ET
import csv

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