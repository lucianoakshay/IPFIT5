import os
import User_Interface
from tqdm import tqdm
import subprocess
import mime_dictionary2 as mime_dictionary
import magic

class gehakt:

    def main_def(self, input):
        # Image mount wordt aangeroepen om de meegegeven image te mounten
        mounting_dir = self.image_mount(input)

        # File list wordt aangeroepen om een dictionary te maken van alle files op de image
        file_dict = self.file_list(mounting_dir)

        # Magic function wordt aangeroepen om de file types te checken
        wrong_files = self.magic_test(file_dict)

        # Log checker function wordt aangeroepen om logs te doorlopen
        login_dict = self.log_checker()

        # Timeline function wordt aangeroepen om een timeline te maken


    #Function to mount e01 or dd images
    #E01 is not implemented yet
    def image_mount(self, given_dir):
        temporary_dir = input("Give a temporary mounting directory: ")
        # Checken of de directory bestaat. Indien dit niet het geval is wordt er gevraagd of deze aangemaakt moet worden.
        while os.path.isdir(temporary_dir) == False:
            create_dir = input("Directory does not exist. Do you want it to be created? Yes/No ")
            if create_dir == "Yes" or create_dir == "Y" or create_dir == "y":
                subprocess.call(["sudo", "mkdir", temporary_dir])
                print("Directory created")
            else:
                print("Please select another mounting directory.")
                temporary_dir = input("Give a temporary mounting directory: ")
        User_Interface.Main_program().Logging().info("User defined mounting directory: " + temporary_dir)
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

        print("Locating and saving all files locations in directory to memory")
        User_Interface.Main_program().Logging().info("Locating and saving all files locations in directory to memory")

        for filepath in tqdm(self.walkdir(mounting_dir), total=filecounter, unit="files"):
            hash_waarde = User_Interface.Main_program().bereken_hash(filepath)
            filename, file_extension = os.path.splitext(filepath)
            file_dict[filepath] = {"Extension": file_extension, "Hash value": hash_waarde}

        print("File search finished")
        User_Interface.Main_program().Logging().info("File search finished")

        return file_dict


    def magic_test(self, file_dict):
        #List of bad files
        bad_files = {}

        print("Searching for bad files")
        User_Interface.Main_program().Logging().info("Searching for bad files")

        for file in tqdm(file_dict, total=len(file_dict), unit="files checked"):
            if "~$" in file:
                User_Interface.Main_program().Logging().info("Not able to read file in '" + file + "'")
                continue
            curr_magic = magic.from_file(file, mime=True)
            if file_dict[file]["Extension"] in mime_dictionary.dic:
                if curr_magic in mime_dictionary.dic[file_dict[file]["Extension"]]:
                    continue
                else:
                    mod_time = os.path.getmtime(file)
                    bad_files[file] = mod_time
                    User_Interface.Main_program().Logging().info("Bad file found in '" + file + "'")
            else:
                User_Interface.Main_program().Logging().info("File with filepath: '" + file + "' not found in mime dictionary")

        print("Bad file search finished")
        User_Interface.Main_program().Logging().info("Bad file search finished")

        return bad_files


    def log_checker(self):
        failed_logins = {}
        return failed_logins


    def timeline_result(self):
        pass