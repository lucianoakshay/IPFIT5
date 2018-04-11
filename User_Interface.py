# gezamenlijk deel Groep 1
#
import os
import sys
import hashlib as hash
import logging
import opdracht_IP
import opdracht_Gehakt
from datetime import date
import datetime
from urllib.request import urlopen
from urllib.error import URLError
from socket import timeout


class NotPositiveError(UserWarning):
    pass


class Main_program:
    # Is the buffersize for the hashing function.
    BUFFERSIZE = 65536
    p = None

    def __init__(self):
        # will be used for the hashing function
        self.sha256hash = hash.sha256()
        # will be used to check internet access
        self.internet_access = False
        # will be used to instantiate the IP script
        self.IP = opdracht_IP.IP_filtering()
        # This variable will be used to creat the log folder if it doesn't exist
        temp_path = os.path.join(sys.path[0], "log")
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        # This variable will be used to create the hash folder if it doesn't exist
        self.hash_location = os.path.join(sys.path[0], "hash")
        if not os.path.exists(self.hash_location):
            os.makedirs(self.hash_location)
        # This variable will be used to create the output folder if it doesn't exist
        self.output_location = os.path.join(sys.path[0], "output")
        if not os.path.exists(self.output_location):
            os.makedirs(self.output_location)
        # This variable will be used to set the log location
        self.log_location = os.path.join(sys.path[0], 'log', 'Main_log_' + str(date.today())+'.log')
        # This variable will be used to set the compare file for the opdracht_IP script
        self.compare_file = None
        self.ascii=False

        # will be used to set the choices in the main menu
        self.choices_main = {
                "1": self.IP_script,
                "2": self.Foto_script,
                "3": self.Gehakt_script,
                "4": self.quit
                }
        # will be used to set the choices in the menu of the IP-script
        self.choices_ip = {
                "1": self.input_pcap_file,
                "2": self.back,
                "3": self.quit
        }

    # function that will check if there's internet access
    def internet_on(self):
        try:
            # will contact google
            urlopen('http://google.com', timeout=1)
            self.internet_access = True
            return True
        except URLError as err:
            self.internet_access = False
            print(err)
            return False
        # if there is an timeout error set internet access to false
        except timeout:
            self.internet_access = False
            return False

    # function that will be used to go back to the main program
    def back(self):
        Main_program().run()

    # This is the logging function that will be used to log the activity of this script.
    def Logging(self):
        logger = logging.getLogger(__name__)

        # check if there already is a loggin handler, if not create one
        if not len(logger.handlers):
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(self.log_location)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    # this function will calculate the sha256 hash of a file
    def bereken_hash(self, file):
        if os.path.isfile(file) and os.access(file, os.R_OK):
            with open(file, 'rb') as file:
                file_buffer = file.read(self.BUFFERSIZE)
                while len(file_buffer) > 0:
                    self.sha256hash.update(file_buffer)
                    file_buffer = file.read(self.BUFFERSIZE)
        else:
            self.Logging().info(file + ": File does not exist or is not accessible")

        return str(self.sha256hash.hexdigest())
    # function that will print out the menu to the screen

    def display_main_menu(self):
        # Disabled for debugging purposes. Can be turned on again once development is finished.
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
Menu
1. Run_IP_script
2. Run_Foto_script
3. Run_gehakt_script
4. Quit
""")
        if not self.internet_on():
            self.Logging().warning("No internet access,functionality of the IP script will be reduced")
            print("#"*48)
            print("# Warning no internet access.                  #")
            print("# IP_script will not be able to get WHOIS info #")
            print("#"*48)

    def display_IP_menu(self):
                        print("""
Menu
1. Input_file
2. Go_back
3. Quit
""")

    # will run the main program
    def run(self):
        self.Logging().info("Starting Main_Script")

        while True:
            self.display_main_menu()
            choice = input("Enter an option: ")
            action = self.choices_main.get(choice)
            self.Logging().info("User input: %s", choice)
            if action:
                action()
            else:
                self.Logging().info("Invalid input, restarting script")
                print("{0} is not a valid choice".format(choice))

    # will start the IP script
    def IP_script(self):

        self.Logging().info("Starting IP_script")
        # loop to check if input is valid
        while True:
            self.display_IP_menu()
            choice = input("Enter an option: ")
            action = self.choices_ip.get(choice)
            self.Logging().info("User input: %s", choice)
            if action:
                action()
            else:
                self.Logging().info("Invalid input, restarting script")
                print("{0} is not a valid choice".format(choice))

    # Will start the foto script

    def Foto_script(self):
        self.Logging().info("Starting Foto_Script")
        print("This is the Foto_script that's now running")
    # WIll start gehakt script

    def Gehakt_script(self):
        self.Logging().info("Starting Gehakt_Script")
        gehakt_image = input("Input the location of the image (.dd / .e01(not yet implemented)): ")
        filename, file_extension = os.path.splitext(gehakt_image)
        while file_extension != ".dd":
            print(gehakt_image + " is of type: " + file_extension + ". Please try again")
            gehakt_image = input("Input the location of the image (.dd / .e01(not yet implemented)): ")
        opdracht_Gehakt.gehakt.main_def(opdracht_Gehakt.gehakt(), gehakt_image)

    # will be used in the future to ask for input of the e01 file
    def input_e01_file(self):
        naam = "test"
        print("Please enter the filename of the e01:")
        filename = input()

        if os.path.exists(filename):
            self.write_hash(filename, naam)
            return filename

    # asks for pcap file, this file will be used as input for the IP_script
    def input_pcap_file(self):
        file_list = []
        hash_filename = "IP_hashes_"+str(date.today()) + ".txt"
        # loop to check if the amount of the pcap's is between 1-10
        while True:
            amount = input('Input the amount of .pcap files you want to filter: ')
            try:
                amount = int(amount)
                # if amount is not between 1-10 raise error
                if amount <= 0 or amount >= 11:
                    raise NotPositiveError
                break
            except ValueError:
                print("This is not a number please enter a valid number between 1 - 10")
            except NotPositiveError:
                if amount < 0:
                    print("Please enter a positive number")
                elif amount >= 11:
                    print("The amount of PCAP files exceeds 10")
        # loop to
        for i in range(amount):
            while True:
                # will ask for the location of the pcap file
                user_input = input('Input pcap file or cancel C: ')
                # will check if the file exists
                if os.path.exists(user_input):
                    # will check if the file is an .pcap file
                    if user_input.endswith('.pcap'):
                        # will check if the file pcap file is not in the file_list
                        if (os.path.abspath(user_input)) not in file_list:
                            self.write_hash(user_input, hash_filename)
                            file_list.append(os.path.abspath(user_input))
                            break
                        elif (os.path.abspath(user_input)) in file_list:
                            print("You added the same file twice, please add a different file:")

                    else:
                        print("File isn't a .pcap file")
                elif user_input == 'C':
                    print("Cancel. Restarting script")
                    self.run()
                else:
                    print("File doesn't exist please enter a valid filename.")

        print("Do you want to compare these files against an IP_list?(Y/N/C)")
        # loop to check the input
        while True:
            compare = input()
            # if input is Y
            if compare == "Y":
                print("Please enter the .txt file where you want to compare against:")
                while True:
                    compare_file = input("")
                    if os.path.exists(compare_file):
                        if compare_file.endswith(".txt") or compare_file.endswith(".TXT"):

                            self.write_hash(compare_file, hash_filename)
                            self.Logging().info("Opening file: " + compare_file)
                            self.compare_file = compare_file
                            break
                        else:
                            print("File isn't a .txt file")
                            print("please enter a valid filename:")
                            continue

                    else:
                        print("File doesn't exist.. Please enter a valid filename")

                break
            if compare == "N":
                print("Will only filter out the IP adresses")
                self.compare_file = None
                break
            if compare == "C":
                print("Cancel. Restarting script")
                self.run()
            else:
                print("That's not a valid input please enter either N/Y or C to cancel")
        self.IP.main(file_list, self.compare_file, self.internet_access, self.output_location)

    # Will be used to write the hash of a file to .txt file
    def write_hash(self, file, name):
        path = os.path.join(sys.path[0], 'hash', str(name))
        print(path)
        with open(os.path.join(self.hash_location, name), 'a+') as f:
            f.write("{:20}{:20}{:20}\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file, self.bereken_hash(file)))

    # will shutdown the script
    def quit(self):
        self.Logging().info("Exiting script")
        print("Exiting script the log files are written to: " + self.log_location)
        sys.exit(0)


# this function will run the main function when script is called
if __name__ == "__main__":
    Main_program().run()
