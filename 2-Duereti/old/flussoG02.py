import traceback
import xml.etree.cElementTree as ET
import csv
from datetime import date, datetime
import xml.etree.ElementTree as Xet
import os
from Lancia_funzione import cerca_file_e_controlla_testo
def gestisci_file_g02():
    # Trova tutti i file che iniziano con G02 e finiscono con .xml
    file_g02 = [f for f in os.listdir("\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti") if f.startswith('G02') and f.endswith('.xml')]

    # Se c'è solo un file, non fa nulla
    if len(file_g02) <= 1:
        print("C'è solo un file (o nessun file) che inizia con G02. Nessuna azione necessaria.")
        return
    # Altrimenti, calcola le dimensioni di ogni file e trova il file con dimensioni maggiori
    file_g02_percorso = [os.path.join("\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", f) for f in file_g02]
    file_con_dimensioni = [(f, os.path.getsize(f)) for f in file_g02_percorso]

    # Trova il file con le dimensioni maggiori
    file_maggiore = max(file_con_dimensioni, key=lambda x: x[1])

    # Mantiene solo il file più grande e cancella gli altri
    for file, dimensione in file_con_dimensioni:
        if file != file_maggiore[0]:
            os.remove(file)
            print(f"Cancellato file {file} di dimensione {dimensione} byte.")

    print(f"Il file {file_maggiore[0]} con dimensione {file_maggiore[1]} byte è stato mantenuto.")

def g02_query():
    lista = []
    with open(
            '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G12\\G12.csv') as csv_file:
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
(select 'GAUI02' from dual) as COD_VOCE_ELEMENT,
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
) and cod_voce_element like 'GAUI02');
commit;
quit;"""

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G02_update_{timestamp}.txt"
        with open(filename, 'w') as file:
            file.write(query)
            file.close()

def log(preventivo, row):
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G02\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()
def flussoG02():
    try:
        basepath = r'\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Duereti\Registrati'
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                name = entry
        xmlparse = Xet.parse(r'\\group.local\SHAREDIR\Brescia\V002\DIRCOM\PREVENT\PREVENTIVISTI\FLUSSI_GAUDI\Duereti\Registrati\\' + name)
        root = xmlparse.getroot()
        rows = []
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
        with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G12\\G12.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            root = ET.Element("VALIDA_IMPIANTI", COD_SERVIZIO="G02", COD_FLUSSO="0050", TERNA_PIVA="05779661007",
                              GESTORE_PIVA="13632560960")

            print("-------------------------------G02--------------------------------------")

            for row in csv_reader:

                print(row[7])
                if line_count == 0:
                    pass
                else:
                    for item in rows:
                        if item[2] == row[7]:
                            doc = ET.SubElement(root, "IMPIANTO", CODICE=item[0], TIPO_OPERAZIONE="V")
                            VERSIONE_ATTESTATO = '1'
                            FLAG_CONNESSIONE_CONDIVISA = 'N'
                            MOTIVAZIONE_RIGETTO = ''
                            CODICE_RINTRACCIABILITA = item[2]
                            CODICE_SCARTO = '000'

                            ET.SubElement(doc, "VERSIONE_ATTESTATO").text = str(VERSIONE_ATTESTATO)
                            ET.SubElement(doc, "FLAG_CONNESSIONE_CONDIVISA").text = str(FLAG_CONNESSIONE_CONDIVISA)
                            ET.SubElement(doc, "MOTIVAZIONE_RIGETTO").text = str(MOTIVAZIONE_RIGETTO)
                            ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = str(CODICE_RINTRACCIABILITA)
                            ET.SubElement(doc, "CODICE_SCARTO").text = str(CODICE_SCARTO)
                            log(row[7], row)


                tree = ET.ElementTree(root)

                tree.write(
                    f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G02_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
                    short_empty_elements=False)
                line_count += 1

    except Exception as e:
        print(e)
        traceback.print_exc()



flussoG02()
gestisci_file_g02()
cerca_file_e_controlla_testo(f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", 'G02', g02_query)
