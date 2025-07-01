import csv
from datetime import datetime

def g03_MU_query():
    lista = []
    with open(
            '\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\G12\\G12.csv') as csv_file:
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

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\Reti+\\update_query\\G03_MU_update_{timestamp}.txt"
        with open(filename, 'w') as file:
            file.write(query)
            file.close()


g03_MU_query()