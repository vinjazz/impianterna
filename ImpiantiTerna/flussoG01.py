import xml.etree.cElementTree as ET
import csv
from datetime import date, datetime
from Lancia_funzione import cerca_file_e_controlla_testo

def g01_controllo_query():
    with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\G01\\G01.csv') as G01_csv_file:
        G01_lista = []
        G01_csv_reader = csv.reader(G01_csv_file, delimiter=';')
        G01_line_count = 0
        for row in G01_csv_reader:
            if G01_line_count == 0:
                pass
            else:
                G01_lista.append(row[0])
            G01_line_count += 1
        G01_result_string = "'" + "', '".join(map(str, G01_lista)) + "'"
        query = f"""update voce_pratica 
        set des_val_voce = (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy') from dual)
where cod_pratica in (
{G01_result_string}
) and cod_voce_element like 'GAUI01' and des_val_voce is null;
commit;
quit;
"""

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\update_query\\G01_Controllo_update_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query)
        file.close()
def g01_query():
    with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\G01\\G01.csv') as G01_csv_file:
        G01_lista = []
        G01_csv_reader = csv.reader(G01_csv_file, delimiter=';')
        G01_line_count = 0
        for row in G01_csv_reader:
            if G01_line_count == 0:
                pass
            else:
                G01_lista.append(row[0])
            G01_line_count += 1
        G01_result_string = "'" + "', '".join(map(str, G01_lista)) + "'"

        query = f""" insert into voce_pratica
    select cod_pratica,
    (select 'VLAV' from dual) as COD_STADIO,
    (select 'GAUI01' from dual) as COD_VOCE_ELEMENT,
    p.dat_decorrenza_pra as DAT_INO_VLI_VOCE, 
    to_date('31/12/2100', 'dd/mm/yyyy') as DAT_FIN_VLI_VOCE,
    (select '6110' from dual) as NUM_PGS_VOCE,
    (select 'V' from dual) as COD_FLG_ORIGINE,
    (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy') from dual) as DES_VAL_VOCE, 
    sysdate as DAT_CREAZIONE_REC,
    sysdate as DAT_ULT_AGG_REC,
    (select 'W70030' from dual) as COD_OPERATORE
    from pratica p  where cod_pratica in (
    {G01_result_string}
    )
    and cod_pratica not in (select cod_pratica from voce_pratica where cod_pratica in (
    {G01_result_string}
    ) and cod_voce_element like 'GAUI01');
    commit;
quit;"""

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\update_query\\G01_update_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query)
        file.close()
def flussoG01New():
    try:
        with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\G01\\G01.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            root = ET.Element("GESTIONE_POD", COD_SERVIZIO="G01", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                              GESTORE_PIVA="12883450152")

            for row in csv_reader:

                if line_count == 0:

                    pass
                else:

                    CODICE_RINTACCIABILITA = row[0]
                    POD = row[1]
                    POTENZA_IMMISSIONE_KW = row[2].replace(',', '.')
                    POTENZA_PRELIEVO_KW = row[3].replace(',', '.')
                    PUNTO_DI_SOLA_IMMISSIONE = row[4]
                    SSPC_TIPOLOGIA_DICHIARATA = row[5]
                    TIPO_CONNESSIONE = row[6]
                    LIVELLO_TENSIONE = row[7]
                    TIPO_ITER = row[8]

                    doc = ET.SubElement(root, "POD", CODICE= POD, TIPO_OPERAZIONE= "U")
                    ET.SubElement(doc, "POTENZA_IMMISSIONE_KW").text = str(POTENZA_IMMISSIONE_KW)
                    ET.SubElement(doc, "POTENZA_PRELIEVO_KW").text = str(POTENZA_PRELIEVO_KW)
                    ET.SubElement(doc, "LIVELLO_TENSIONE_V").text = str(LIVELLO_TENSIONE)
                    ET.SubElement(doc, "PUNTO_DI_SOLA_IMMISSIONE").text = str(PUNTO_DI_SOLA_IMMISSIONE)
                    ET.SubElement(doc, "TIPO_IMMISSIONE").text = str(TIPO_CONNESSIONE)
                    ET.SubElement(doc, "CABINA_PRIMARIA").text = None
                    ET.SubElement(doc, "SSPC_TIPOLOGIA_RICHIESTA").text = str(SSPC_TIPOLOGIA_DICHIARATA)
                    ET.SubElement(doc, "SSPC_TIPOLOGIA_POD").text = "P"
                    ET.SubElement(doc, "SSPC_POD_ASSOCIATO")
                    ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = str(CODICE_RINTACCIABILITA)
                    ET.SubElement(doc, "TIPO_ITER").text = str(TIPO_ITER)
                    # tree = ET.ElementTree(root)

                    log(row[0], row)
                    print(row[0])
                line_count += 1
    except Exception as e:
        print(e)
    tree = ET.ElementTree(root)
    tree.write(
        f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\G01_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
        short_empty_elements=False)

def log(preventivo, row):
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\\\Unareti\\G01\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()

flussoG01New()
cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\", 'G01', g01_query)
cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Unareti\\", 'G01', g01_controllo_query)
