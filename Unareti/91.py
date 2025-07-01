import csv
import datetime
import os
import shutil
from Lancia_funzione import cerca_file_e_controlla_testo_csv
def write_files_starting_with_G03():
    # List all files in the directory
    folder_path = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04"
    files_in_folder = os.listdir(folder_path)
    # Filter files that start with 'G03'
    g03_files = [file for file in files_in_folder if file.startswith('G03')]
    query_total = ''
    for file in g03_files:
        lista = []

        with open(
                f'\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04\\{file}') as csv_file:
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
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\update_query\\G03_Update_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query_total)
        file.close()
    #webbrowser.open(filename)
def write_files_starting_with_G04():

    folder_path = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04"
    files_in_folder = os.listdir(folder_path)
    query_total = ''
    g04_files = [file for file in files_in_folder if file.startswith('G04')]
    for file in g04_files:
        lista = []

        with open(
                f'\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04\\{file}') as csv_file:
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
    filename = f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\update_query\\G04_Update_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write(query_total)
        file.close()

    #move_files()
def move_files():
    source_folder= f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04"
    destination_folder= f"\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04\\old"
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

cerca_file_e_controlla_testo_csv("\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04", "G03", write_files_starting_with_G03)
cerca_file_e_controlla_testo_csv("\\\\group.local\\SHAREDIR\\Brescia\\V002\\DIRCOM\\PREVENT\\PREVENTIVISTI\\FLUSSI_GAUDI\\LOG G03 E G04", "G04", write_files_starting_with_G04)
move_files()
