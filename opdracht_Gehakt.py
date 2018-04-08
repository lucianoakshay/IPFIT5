import os
import User_Interface
from tqdm import tqdm
import subprocess
import mime_dictionary2 as mime_dictionary
import magic
import datetime
import operator

class gehakt:

    def main_def(self, user_input):
        # Image mount wordt aangeroepen om de meegegeven image te mounten
        mounting_dir = self.image_mount(user_input)

        # File list wordt aangeroepen om een dictionary te maken van alle files op de image
        file_dict = self.file_list(mounting_dir)

        # Magic function wordt aangeroepen om de file types te checken
        bad_files = self.magic_test(file_dict)

        # Log checker function wordt aangeroepen om logs te doorlopen
        bad_logins = self.log_checker()

        # Timeline function wordt aangeroepen om een timeline te maken
        self.timeline_result(bad_files, bad_logins)

        # Last user input asked to quit or stay
        final_input = input("Script finished, Q to to go back to main menu: ")
        while final_input != "Q":
            final_input = input("Script finished, Q to to go back to main menu or N for next item: ")

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
        bad_files = []

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
                    raw_time = os.path.getmtime(file)
                    mod_time = datetime.datetime.fromtimestamp(raw_time).strftime('%Y-%m-%d %H:%M:%S')
                    bad_files.append([file, mod_time])
                    User_Interface.Main_program().Logging().info("Bad file found in '" + file + "'")
            else:
                User_Interface.Main_program().Logging().info("File with filepath: '" + file + "' not found in mime dictionary")

        print("Bad file search finished")
        User_Interface.Main_program().Logging().info("Bad file search finished")

        return bad_files


    def log_checker(self):
        bad_logins = []
        return bad_logins


    def timeline_result(self, bad_files, bad_logins):
        # Need to merge the two lists here
        merged_list = bad_files
        ordered_list = sorted(merged_list, key=operator.itemgetter(1))

        save_results = input("Do you want to save the results of the timeline to a file? (Yes/No)")
        if save_results == "Y" or save_results == "y" or save_results == "Yes" or save_results == "yes":
            print("Please specify some information")
            file_location = input("Please specify a saving location (without extension): ")
            case_nr = input("Case Number: ")
            evidence_id = input("Evidence ID: ")
            examiner = input("Examiner: ")
            curr_datetime = datetime.datetime.today()
            save = True

            # Creating the file and writing down header info
            file = open(file_location + ".txt", "w")
            file.write("Case Number: " + case_nr)
            file.write("\nEvidence ID: " + evidence_id)
            file.write("\nExaminer: " + examiner)
            file.write("\nRecorded date: " + str(curr_datetime))
        else:
            save = False

        # Looping through the list and printing everything
        for item in ordered_list:
            print(item[1], item[0])
            if save:
                file.write("\n" + item[1] + item[0])

        # Closing file if it was open
        if save:
            file.close()