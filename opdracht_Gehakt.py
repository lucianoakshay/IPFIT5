import os
import User_Interface
from tqdm import tqdm
import subprocess

# wat will je aan deze functie meegeven?
# want je hebt de invoer van deze functie nu input genoemd, dit is ook een reserver word van python om user input te vragen.
# Ik denk dat als je de invoer variabelen hernoemt naar filename of iets dergelijks dat je geen fouten meer krijgt.
def image_mount(input):
    temporary_dir = input("Give a temporary mounting directory: ")
    #Checken of de directory bestaat. Indien dit niet het geval is wordt er gevraagd of deze aangemaakt moet worden.
    while os.path.isdir(temporary_dir) == False:
        create_dir = input("Directory does not exist. Do you want it to be created? Yes/No ")
        if create_dir == "Yes" or create_dir == "Y" or create_dir == "y":
            subprocess.call(["sudo", "mkdir", temporary_dir])
            print("Directory created")
        else:
            print("Please select another mounting directory.")
        temporary_dir = input("Give a temporary mounting directory: ")
    #De image wordt read only gemount met een bash commando
    subprocess.call(["sudo", "mount", "-o", "ro", input, temporary_dir])
    return temporary_dir


def file_list(input):
    test = User_Interface.Main_program()
    #Image mount wordt aangeroepen om de meegegeven image te mounten
    sec_input = image_mount(input)
    #Dictionary om alle files met hashes erbij op te slaan
    file_dict = {}
    # Loop die een variabele met het path naar een file update zodat iedere file in de directory wordt afgelopen.
    # Vervolgens worden de subdir en de file gejoind in de variabele current_dir
    # Hierna wordt een betreffende directory meegegeven aan een splitext commando die de extensie van de file afhaald
    for subdir, dirs, files in tqdm(os.walk(sec_input)):
        for file in files:
            current_dir = (os.path.join(subdir, file))
            hash_waarde = User_Interface.Main_program.bereken_hash(test,current_dir)
            filename, file_extension = os.path.splitext(current_dir)
            file_dict[filename] = {"Extension":file_extension, "Hash value":hash_waarde}
    print(file_dict)



