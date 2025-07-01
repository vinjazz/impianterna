import sqlite3
import datetime
import xml.etree.cElementTree as ET
from datetime import date, datetime
from recupero_log import log_summary



def g03():
    try:
        con = sqlite3.connect("C:\\ImpiantiTerna\\gaudi.db")
        cur = con.cursor()
        sql = """select  a.impianto, B.data, a.CODICE_RINTRACCIABILITA, b.potenza  
                    from GAUDI_impianti_realizzati a 
                    join sides b 
                    on b.CODICE = a.CODICE_POD where  b.des_val_voce in (select max(c.des_val_voce) from sides c where b.codice = c.codice)
                    group by a.impianto, B.data, a.CODICE_RINTRACCIABILITA, b.potenza  """
        data = cur.execute(sql).fetchall()
        root = ET.Element("COMPLETAMENTO_IMPIANTO", COD_SERVIZIO="G03", COD_FLUSSO="0050", TERNA_PIVA="05779661007", GESTORE_PIVA="12883450152")
        contatore = 0
        for row in data:
            print(row[2])
            #upn = row[0].replace("IM", "UPN")
            doc = ET.SubElement(root, "IMPIANTO", CODICE = f"{row[0]}")
            data = datetime.strptime(row[1],'%d-%m-%Y').date()
            ET.SubElement(doc, "DATA_COMPLETAMENTO_CONNESSIONE").text = str(data)
            ET.SubElement(doc, "DATA_SOTTOSCRIZIONE_REGOLAMENTO_ESERCIZIO").text = ""
            ET.SubElement(doc, "POTENZA_EFFETTIVA").text = row[3].replace(",",".")
            ET.SubElement(doc, "DATA_FINE_REALIZZAZIONE_IMP").text = ""
            ET.SubElement(doc, "TIPOLOGIA_DICHIARATA").text = ""
            ET.SubElement(doc, "CODICE_RINTRACCIABILITA").text = row[2]
        tree = ET.ElementTree(root)
        #tree.write(f"C:\\ImpiantiTerna\\G03\\G03.xml")
        tree.write(
            f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\G03_{datetime.now().strftime('%d%m%Y%H%M%S')}.xml",
            short_empty_elements=False)


    except Exception as e:
        print(e)

    finally:
        con.close()


g03()
log_summary('G03')
