import os
import csv

def log_summary(flusso):
    directory = f'C:\ImpiantiTerna\{flusso}\log'
    os.remove(f'C:\ImpiantiTerna\{flusso}\log_summary_{flusso}.csv')
    for filename in os.scandir(directory):
        if filename.is_file():
                with open(filename.path, mode='r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    line_count = 0
                    for row in csv_reader:
                        if line_count == 0:
                            data = (row[0].split(';'))[0]
                            prev = (row[0].split(';'))[1]
                            #print(data + ' ' + prev + ' ' + flusso)

                            with open(f'C:\ImpiantiTerna\{flusso}\log_summary_{flusso}.csv', mode='a', newline='') as csv_file:


                                writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL )
                                writer.writerow([prev, data, flusso])

                                csv_file.close()
                            break






