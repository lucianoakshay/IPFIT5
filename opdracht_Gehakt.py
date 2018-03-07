import os
import User_Interface
from tqdm import tqdm

def file_list(input):
    test = User_Interface.Main_program()
    #Dictionary om alle files met hashes erbij op te slaan
    file_dict = {}
    # Loop die een variabele met het path naar een file update zodat iedere file in de directory wordt afgelopen.
    # Vervolgens worden de subdir en de file gejoind in de variabele current_dir
    # Hierna wordt een betreffende directory meegegeven aan een splitext commando die de extensie van de file afhaald
    for subdir, dirs, files in tqdm(os.walk(input)):
        for file in files:
            current_dir = (os.path.join(subdir, file))
            hash_waarde = User_Interface.Main_program.bereken_hash(test,current_dir)
            filename, file_extension = os.path.splitext(current_dir)
            file_dict[filename] = {"Extension":file_extension, "Hash value":hash_waarde}
    print(file_dict)



