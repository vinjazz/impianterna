import csv
import datetime
import webbrowser
import os
import shutil

def gestisci_file_g02_duereti():
    # Trova tutti i file che iniziano con G02 e finiscono con .xml
    file_g02 = [f for f in
                os.listdir("\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti") if
                f.startswith('G02') and f.endswith('.xml')]

    # Se c'è solo un file, non fa nulla
    if len(file_g02) <= 1:
        print("C'è solo un file (o nessun file) che inizia con G02. Nessuna azione necessaria.")
        return

    # Altrimenti, calcola le dimensioni di ogni file e trova il file con dimensioni maggiori
    file_g02_percorso = [
        os.path.join("\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti", f) for f
        in file_g02]
    file_con_dimensioni = [(f, os.path.getsize(f)) for f in file_g02_percorso]

    # Trova il file con le dimensioni maggiori
    file_maggiore = max(file_con_dimensioni, key=lambda x: x[1])

    # Mantiene solo il file più grande e cancella gli altri
    for file, dimensione in file_con_dimensioni:
        if file != file_maggiore[0]:
            os.remove(file)
            print(f"Cancellato file {file} di dimensione {dimensione} byte.")

    print(f"Il file {file_maggiore[0]} con dimensione {file_maggiore[1]} byte è stato mantenuto.")
def write_G03_MU_query_duereti():
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
   and pr.cod_azienda = 35
   and f.cod_voce_element like 'TIPCON'
   and t.cod_pratica in (
    {result_string}

);
    """

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G03_MU_Query_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query)
def move_files_duereti():
    source_folder = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\LOG G03 E G04"
    destination_folder = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\LOG G03 E G04\\old"
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

        # Ensure the destination folder exists; create it if not
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

        # Get a list of all files in the source folder
    files = os.listdir(source_folder)

    # Iterate through the files and move .txt files to the destination folder
    for file in files:
        if file.endswith(".csv"):
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)
            # Move the file
            shutil.move(source_path, destination_path)
            print(f"Moved: {file} from {source_folder} to {destination_folder}")
def write_query_duereti():
    lista = []
    G01_lista = []
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

    with open(
            '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G01\\G01.csv') as G01_csv_file:
        G01_csv_reader = csv.reader(G01_csv_file, delimiter=';')
        G01_line_count = 0
        for row in G01_csv_reader:
            if G01_line_count == 0:
                pass
            else:
                G01_lista.append(row[0])
            G01_line_count += 1
        G01_result_string = "'" + "', '".join(map(str, G01_lista)) + "'"

        query = f"""
    ############################################################################ G12 ########################################################################
    update voce_pratica 
    set des_val_voce = (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy')  from dual)
    where cod_pratica in (
    {result_string}
    ) and cod_voce_element like 'GAUI12';

    ############################################################################ G02 ########################################################################
    insert into voce_pratica
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
    ) and cod_voce_element like 'GAUI02' )

    ############################################################################ G13 ########################################################################

    insert into voce_pratica
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
    ) and cod_voce_element like 'GAUI13' )

    ############################################################################ G03 ########################################################################


    insert into voce_pratica
    select cod_pratica,
    (select 'CVAR' from dual) as COD_STADIO,
    (select 'GAUI03' from dual) as COD_VOCE_ELEMENT,
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
    ) and cod_voce_element like 'GAUI03' )

    ############################################################################ Controllo G12-13-03-02 ########################################################################
    select * from  voce_pratica 

    where cod_pratica in 
    (
    {result_string}
    ) and cod_voce_element in ('GAUI12','GAUI02','GAUI13','GAUI03')
    --for update

    ############################################################################ G01 ########################################################################

    insert into voce_pratica
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
    ) and cod_voce_element like 'GAUI01' )


    ############################################################################ Controllo G01 ########################################################################

    select * from  voce_pratica 

    where cod_pratica in 
    (
    {G01_result_string}
    ) and cod_voce_element = 'GAUI01'
    --for update

    ############################################################################ G03 Modello Unico ########################################################################
    select distinct t.cod_pratica,
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
)

    """

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\Update_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query)
    webbrowser.open(filename)
def write_files_starting_with_G03_duereti():
    # List all files in the directory
    folder_path = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\duereti\\LOG G03 E G04"
    files_in_folder = os.listdir(folder_path)
    # Filter files that start with 'G03'
    g03_files = [file for file in files_in_folder if file.startswith('G03')]
    query_total = ''
    for file in g03_files:
        lista = []

        with open(
                f'\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\duereti\\LOG G03 E G04\\{file}') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if line_count == 0 or line_count == 1:
                    pass
                else:
                    lista.append(row[4])
                line_count += 1
            g03_result_string = "'" + "', '".join(map(str, lista)) + "'"
            query = f"""update voce_pratica set des_val_voce = '{file.split('_')[2].replace('.csv', '')}'
where cod_pratica in (
{g03_result_string}) 
and cod_voce_element like 'GAUI03';
commit;
quit;

"""
            query_total += query
            csv_file.close()

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\duereti\\update_query\\G03_Update_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query_total)
        file.close()
    # webbrowser.open(filename)
def write_files_starting_with_G04_duereti():
    folder_path = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\duereti\\LOG G03 E G04"
    files_in_folder = os.listdir(folder_path)
    query_total = ''
    g04_files = [file for file in files_in_folder if file.startswith('G04')]
    for file in g04_files:
        lista = []

        with open(
                f'\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\duereti\\LOG G03 E G04\\{file}') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if line_count == 0 or line_count == 1:
                    pass
                else:
                    lista.append(row[2])
                line_count += 1
            g04_result_string = "'" + "', '".join(map(str, lista)) + "'"
            query = f"""update voce_pratica set des_val_voce = '{file.split('_')[2].replace('.csv', '')}'
where cod_pratica in (
{g04_result_string}) 
and cod_voce_element like 'GAUI04';
commit;
quit;


    """
            query_total += query
            csv_file.close()

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\duereti\\update_query\\G04_Update_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query_total)
        file.close()

    # move_files()

def move_queries_duereti():
    source_folder = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query"
    destination_folder = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\old"
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

        # Ensure the destination folder exists; create it if not
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

        # Get a list of all files in the source folder
    files = os.listdir(source_folder)

    # Iterate through the files and move .txt files to the destination folder
    for file in files:
        if file.endswith(".txt"):
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)

            # Move the file
            shutil.move(source_path, destination_path)
            print(f"Moved: {file} from {source_folder} to {destination_folder}")
def g01_query_duereti():
    with open(
            '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G01\\G01.csv') as G01_csv_file:
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
    ) and cod_voce_element like 'GAUI01' );
    commit;
quit;
"""

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G01_update_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query)
        file.close()
def g12_query_duereti():
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

        query = f"""update voce_pratica 
set des_val_voce = (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy')  from dual)
where cod_pratica in (
{result_string}
) and cod_voce_element like 'GAUI12';
commit;
quit;"""

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G12_update_{timestamp}.txt"
        with open(filename, 'w') as file:
            file.write(query)
            file.close()
def g02_query_duereti():
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
) and cod_voce_element like 'GAUI02' );
commit;
quit;
"""

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G02_update_{timestamp}.txt"
        with open(filename, 'w') as file:
            file.write(query)
            file.close()
def g13_query_duereti():
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
    ) and cod_voce_element like 'GAUI13' );
commit;
quit;
"""

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G13_update_{timestamp}.txt"
        with open(filename, 'w') as file:
            file.write(query)
            file.close()
def g03_query_duereti():
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
        query = f""" insert into voce_pratica
    select cod_pratica,
    (select 'CVAR' from dual) as COD_STADIO,
    (select 'GAUI03' from dual) as COD_VOCE_ELEMENT,
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
    ) and cod_voce_element like 'GAUI03');
commit;
quit;
"""

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G03_update_{timestamp}.txt"
        with open(filename, 'w') as file:
            file.write(query)
            file.close()
def g03_MU_query_duereti():
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
    (select 'CVAR' from dual) as COD_STADIO,
    (select 'GAUI03' from dual) as COD_VOCE_ELEMENT,
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
    ) and cod_voce_element like 'GAUI03');
commit;
quit;"""

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G03_MU_update_{timestamp}.txt"
        with open(filename, 'w') as file:
            file.write(query)
            file.close()
def g01_controllo_query_duereti():
    with open('\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\G01\\G01.csv') as G01_csv_file:
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

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G01_Controllo_update_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query)
        file.close()
def g12_controllo_query_duereti():
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

        query = f"""update voce_pratica 
                set des_val_voce = (select TO_CHAR(CURRENT_DATE, 'dd-mm-yyyy') from dual)
            where cod_pratica in (
            {result_string}
            ) and cod_voce_element in ('GAUI12','GAUI02','GAUI13', 'GAUI03') and des_val_voce is null;
            commit;
quit;

        """

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Duereti\\update_query\\G12_Controllo_update_{timestamp}.txt"
        with open(filename, 'w') as file:
            file.write(query)
            file.close()
