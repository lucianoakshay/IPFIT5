import os
import User_Interface
from tqdm import tqdm
import subprocess
import hashlib as hash

class gehakt:

    def main_def(self, input):
        # Image mount wordt aangeroepen om de meegegeven image te mounten
        mounting_dir = self.image_mount(input)

        # File list wordt aangeroepen om een dictionary te maken van alle files op de image
        file_dict = self.file_list(mounting_dir)

    def bereken_hash2(self, bestand):
        sha256hash = hash.sha256()
        BUFFERSIZE = 65536
        if os.path.isfile(bestand) and os.access(bestand, os.R_OK):
            with open((bestand),'rb') as file:
                file_buffer = file.read(BUFFERSIZE)
                while len(file_buffer)>0:
                    sha256hash.update(file_buffer)
                    file_buffer= file.read(BUFFERSIZE)
        else:
            User_Interface.Main_program().Logging().info(bestand+": File does not exist or is not accessible")

        return(str(sha256hash.hexdigest()))

    #Function to mount e01 or dd images
    #E01 is not implemented yet
    def image_mount(self, given_dir):
        temporary_dir = input("Give a temporary mounting directory: ")
        User_Interface.Main_program().Logging().info("User defined mounting directory: " + temporary_dir)
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

    def walkdir(self, folder):
        """Walk through each files in a directory"""
        for dirpath, dirs, files in os.walk(folder):
            for filename in files:
                yield os.path.abspath(os.path.join(dirpath, filename))

    def file_list(self, mounting_dir):
        # Dictionary om alle files met hashes erbij op te slaan
        file_dict = {}

        # File counter die aan het begin alle files telt voor de progress bar
        filecounter = 0
        for filepath in self.walkdir(mounting_dir):
            filecounter += 1

        for filepath in tqdm(self.walkdir(mounting_dir), total=filecounter, unit="files"):
            hash_waarde = User_Interface.Main_program().bereken_hash(filepath)
            filename, file_extension = os.path.splitext(filepath)
            file_dict[filename] = {"Extension": file_extension, "Hash value": hash_waarde}

        print(file_dict)
        print(len(file_dict))
        return file_dict



