import sqlite3
import datetime
import xml.etree.cElementTree as ET

from dateutil.relativedelta import relativedelta
from datetime import date, datetime
import batch
from recupero_log import log_summary
def log(preventivo, row):
    line = f'{date.today()};{preventivo}'
    file_uno = open(f"C:\\ImpiantiTerna\\G04\\log\\{preventivo}.csv", "w")
    file_uno.write(line)
    for data in row:
        file_uno.write(f"\n {data};")
    file_uno.close()


def flussoG04(type):
    year = str(datetime.strptime(str(datetime.today().year), '%Y') - relativedelta(years=2))[0:4]

    try:
        con = sqlite3.connect("C:\\ImpiantiTerna\\gaudi.db")
        cur = con.cursor()
        if type == "post":
            sql = f"""select GAUDI_impianti_esercibili.impianto,
                    GAUDI_impianti_esercibili.CODICE_RINTRACCIABILITA, 
                    sides.data from
                    GAUDI_impianti_esercibili INNER JOIN sides  where
                    GAUDI_impianti_esercibili.CODICE_POD = sides.codice
                    and  sides.des_val_voce in (select max(c.des_val_voce) from sides c where sides.codice = c.codice)
                    and sides.ANNO >= {year}"""
        elif type == "pre":
            sql = f"""select GAUDI_impianti_esercibili.impianto,
                    GAUDI_impianti_esercibili.CODICE_RINTRACCIABILITA, 
                    sides.data from
                    GAUDI_impianti_esercibili INNER JOIN sides  where
                    GAUDI_impianti_esercibili.CODICE_POD = sides.codice
                    and  sides.des_val_voce in (select max(c.des_val_voce) from sides c where sides.codice = c.codice)
                    and sides.ANNO < {year}"""
        data = cur.execute(sql).fetchall()

        root = ET.Element("ATTIVAZIONE_CONNESSIONE", COD_SERVIZIO="G04", COD_FLUSSO="0050", TERNA_PIVA="05779661007", GESTORE_PIVA="12883450152")
        contatore = 0
        for row in data:
            print(row[1])
            upn = row[0].replace("IM", "UPN")
            doc = ET.SubElement(root, "UNITA", CODICE = f"{upn}_01")

            data = datetime.strptime(row[2],'%d-%m-%Y').date()

            ET.SubElement(doc, "DATA_ATTIVAZIONE_CONNESSIONE").text = str(data)
            ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = row[1]
            ET.SubElement(doc, "CODICE_SCARTO").text = "000"

        log(row[1], row)
        tree = ET.ElementTree(root)
        if type == "post":
            tree.write(f"C:\\ImpiantiTerna\\G04\\post\\recenti_G04_{date.today().strftime('%d%m%Y%H%M%S')}.xml")
            tree.write(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\G04_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
                short_empty_elements=False)

        else:
            tree.write(f"C:\\ImpiantiTerna\\G04\\pre\\vecchi_G04_{date.today().strftime('%d%m%Y%H%M%S')}.xml")
            tree.write(
                f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\G04_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
                short_empty_elements=False)

    except Exception as e:
        print(e)

    finally:
        con.close()


batch.esercibili()
#flussoG04('pre')
flussoG04('post')

log_summary('G04')
