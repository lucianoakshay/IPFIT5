import os
import User_Interface
from tqdm import tqdm
import subprocess

class gehakt:

    def main_def(self, input):
        # Image mount wordt aangeroepen om de meegegeven image te mounten
        mounting_dir = self.image_mount(input)

        # File list wordt aangeroepen om een dictionary te maken van alle files op de image
        file_dict = self.file_list(mounting_dir)

    #Function to mount e01 or dd images
    #E01 is not implemented yet
    def image_mount(self, given_dir):
        temporary_dir = input("Give a temporary mounting directory: ")
        User_Interface.Main_program.Logging(User_Interface.Main_program()).info("User defined mounting directory: " + temporary_dir)
        # Checken of de directory bestaat. Indien dit niet het geval is wordt er gevraagd of deze aangemaakt moet worden.
        while os.path.isdir(temporary_dir) == False:
            create_dir = input("Directory does not exist. Do you want it to be created? Yes/No ")
            if create_dir == "Yes" or create_dir == "Y" or create_dir == "y":
                subprocess.call(["sudo", "mkdir", temporary_dir])
                print("Directory created")
            else:
                print("Please select another mounting directory.")
                temporary_dir = input("Give a temporary mounting directory: ")
        # De image wordt read only gemount met een bash commando
        subprocess.call(["sudo", "mount", "-o", "ro", given_dir, temporary_dir])
        return temporary_dir

    def file_list(self, mounting_dir):
        # Dictionary om alle files met hashes erbij op te slaan
        file_dict = {}

        # File counter die aan het begin alle files telt voor de progress bar
        filecounter = 0
        for filepath in os.walk(mounting_dir):
            filecounter += 1

        # Loop die een variabele met het path naar een file update zodat iedere file in de directory wordt afgelopen.
        # Vervolgens worden de subdir en de file gejoind in de variabele current_dir
        # Hierna wordt een betreffende directory meegegeven aan een splitext commando die de extensie van de file afhaald
        for subdir, dirs, files in tqdm(os.walk(mounting_dir), total=filecounter, unit="files"):
            for file in files:
                current_dir = (os.path.join(subdir, file))
                hash_waarde = User_Interface.Main_program.bereken_hash(User_Interface.Main_program(), current_dir)
                filename, file_extension = os.path.splitext(current_dir)
                file_dict[filename] = {"Extension": file_extension, "Hash value": hash_waarde}
        print(file_dict)




