import xml.etree.ElementTree as Xet
import sqlite3
import pandas as pd
import os
#import flussoG3

rows = []

def cleanDb():
    try:
        con = sqlite3.connect("C:\\ImpiantiTerna\\gaudi.db")
        cur = con.cursor()
        cur.execute("delete from GAUDI_impianti_esercibili")
        con.commit()
        cur.execute("delete from GAUDI_impianti_validati")
        con.commit()
        cur.execute("delete from GAUDI_impianti_realizzati")
        con.commit()
    except:
        pass
    finally:
        cur.close()
        con.close()

def generaFile(file):

    cols = ["IMPIANTO","CODICE_RICHIESTA", "CODICE_RINTRACCIABILITA",
            "CODICE_SAPR", "STATO_OPERATIVO","STATO_IMPIANTO","DATA_CONVALIDA","VERSIONE_ATTESTATO",
            "TIPO_TECNOLOGIA","NOMEIMP","COD_ISTAT_COMUNE",
            "LOCALITA","INDIRIZZO","CAP","PARTITA_IVA_PROD","CODICE_FISCALE_PROD",
            "CODICE_ISTAT_PROD","EMAIL_PROD","TENSIONE_COLL_RETE","POTENZA_ATTIVA_NOMINALE", "POTENZA_INVERTER","CODICE_POD","REGIME_COMMERCIALE"]


    xmlparse = Xet.parse(f'{file}')
    root = xmlparse.getroot()

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


        global rows
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

# def toCSV(rows,cols):
#     df = pd.DataFrame(rows, columns=cols)
#     df.to_csv(f'C:\\ImpiantiTerna\{file.replace(".xml","")}.csv')

def findFile(dir_path, type):
    for path in os.scandir(dir_path):
        if path.is_file():

            #generaFile(f'C:\\ImpiantiTerna\\esercibili\\{path.name}')
            generaFile(f'C:\\ImpiantiTerna\\{type}\\{path.name}')
            global rows
            try:
                con = sqlite3.connect("C:\\ImpiantiTerna\\gaudi.db")
                cur = con.cursor()
                def insert(type):
                    for item in rows:
                        print(item)
                        cur.execute(f"""insert into {type} (IMPIANTO,
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
                                        REGIME_COMMERCIALE) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (item[0],item[1],
                        item[2],
                        item[3],
                        item[4],
                        item[5],
                        item[6],
                        item[7],
                        item[8],
                        item[9],
                        item[10],
                        item[11],
                        item[12],
                        item[13],
                        item[14],
                        item[15],
                        item[16],
                        item[17],
                        item[18],
                        item[19],
                        item[20],
                        item[21],
                        item[22]))

                        con.commit()
                if type == "validati":
                    insert("GAUDI_impianti_validati")
                elif type == "esercibili":
                    insert("GAUDI_impianti_esercibili")
                elif type == "realizzati":
                    insert("GAUDI_impianti_realizzati")
                elif type == "eserciziomilano":
                    insert("GAUDI_impianti_esercizioMilano")
                elif type == "esercizioBrescia":
                    insert("GAUDI_impianti_esercizioBrescia")

            except Exception as e:
                print(e)
                pass
            finally:
                con.close()




def validati():
    dir_path = r'C:\\ImpiantiTerna\\validati'
    findFile(dir_path, type="validati")

def esercibili():
    dir_path = r'C:\\ImpiantiTerna\\esercibili'
    findFile(dir_path, type="esercibili")

def realizzati():
    dir_path = r'C:\\ImpiantiTerna\\realizzati'
    findFile(dir_path, type="realizzati")


def eserciziomilano():
    dir_path = r'C:\\ImpiantiTerna\\eserciziomilano'
    findFile(dir_path, type="eserciziomilano")

def esercizioBrescia():
    dir_path = r'C:\\ImpiantiTerna\\esercibilibrescia'
    findFile(dir_path, type="esercizioBrescia")


cleanDb()
#

#esercibili()

#realizzati()