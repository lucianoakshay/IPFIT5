# gezamenlijk deel Groep 1
#
import os
import sys
import hashlib as hash
import logging
import opdracht_IP
import opdracht_Gehakt
from datetime import date
from urllib.request import urlopen
from urllib.error import URLError
from virus_total_apis import PublicApi as virustotal
class NotPositiveError(UserWarning):
    pass


class Main_program:
    BUFFERSIZE = 65536
    p = None
    API_KEY = '5d26b492516bef5706b162488776b1ac507accd713f2d9a7bd53727b46ecf20e'

    def __init__(self):
        self.sha256hash = hash.sha256()

        self.IP = opdracht_IP.IP_filtering()
        temp_path =os.path.join(sys.path[0],"log")
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        self.log_location = os.path.join(sys.path[0],'log','Main.log')
        self.compare_file= None
        self.choices_main = {
                "1": self.IP_script,
                "2": self.Foto_script,
                "3": self.Gehakt_script,
                "4": self.quit
                }
        self.choices_ip = {
                "1": self.input_pcap_file,
                "2": self.back,
                "3": self.quit
        }
        if not self.internet_on():
            self.Logging().warning("No internet access, virus scaning is disabled. Also reduced functionality of the IP script")
            print("#"*48)
            print("# No internet access, virusscanner is disabled #")
            print("# IP_script will not be able to get WHOIS info #")
            print("#"*48)



    def internet_on(self):
        try:
            urlopen('http://google.com', timeout=2)
            return True
        except URLError as err:
            return False

    def back(self):
        Main_program().run()
    # This is the logging function that will be used to log the activity of this script.

    def Logging(self):
        logger = logging.getLogger(__name__)

        if not len(logger.handlers):
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(self.log_location)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    # this function will calculate the sha256 hash of a file
# misschien ff testen of de hash klopt

    def bereken_hash(self,bestand):
        if os.path.isfile(bestand) and os.access(bestand, os.R_OK):
            with open((bestand),'rb') as file:
                file_buffer = file.read(self.BUFFERSIZE)
                while len(file_buffer)>0:
                    self.sha256hash.update(file_buffer)
                    file_buffer= file.read(self.BUFFERSIZE)
        else:
            self.Logging().info(bestand+": File does not exist or is not accessible")

        return(str(self.sha256hash.hexdigest()))
    # function that will print out the menu to the screen, ( needs some minor changes)
    def display_main_menu(self):
        print("""
Menu
1. Run_IP_script
2. Run_Foto_script
3. Run_gehakt_script
4. Quit
""")

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
            self.Logging().info("User input: %s",choice)
            if action:
                action()
            else:
                self.Logging().info("Invalid input, restarting script")
                print("{0} is not a valid choice".format(choice))

    # will start the IP script
    def IP_script(self):
        self.Logging().info("Starting IP_script")
        # import opdracht_IP
        while True:
            self.display_IP_menu()
            choice = input("Enter an option: ")
            action = self.choices_ip.get(choice)
            self.Logging().info("User input: %s",choice)
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
        opdracht_Gehakt.gehakt.main_def(opdracht_Gehakt.gehakt(), input("Input the location of the image (.dd / .e01(not yet implemented)): "))
        print("This is the Gehakt_script that's now running")


    # will be used in the future to ask for input of the e01 file
    def input_e01_file(self):
        naam= "test"
        print("Please enter the filename of the e01:")
        filename =input()

        if self.exists(filename,naam):
            return filename



    # asks for pcap file, this file will be used as input for the IP_script
    def input_pcap_file(self):
        file_list = []
        dictionary = {}
        while True:
            amount = input('Input the ammount of .pcap files you want to filter: ')
            try:
                amount = int(amount)
                if amount<= 0 or amount>=11:
                    raise NotPositiveError
                break
            except ValueError:
                print("This is not a number please enter a valid number between 1 - 10")
            except NotPositiveError:
                if amount < 0:
                    print("Please enter a positive number, otherwise the whole application will cause total mayhem")
                elif amount >=11:
                    print( "The amount of PCAP files exceeds 10")

        for i in range(amount):
            while True:
                test = input('Input pcap file: ')
                if self.exists(test, 'PCAP'):
                    if test.endswith( '.pcap'):
                        if (os.path.abspath(test)) not in file_list:

                            file_list.append(os.path.abspath(test))
                            break
                        elif (os.path.abspath(test)) in file_list:
                            print("You added the same file twice, please add a different file:")

                    else:
                        print( "File isn't a .pcap file")
                elif test == 'C':
                    print("Cancel. Restarting script")
                    self.run()
                else:
                    print("File doesn't exist please enter a valid filename.")

        print("Do you want to compare these files against an other file?(Y/N/C)")
        while True:
            compare = input()
            if compare == "Y":
                print("Please enter the file where you want to compare against:")
                while True:
                    compare_file =input("")
                    if self.exists(compare_file, 'PCAP'):
                        self.Logging().info("Opening file: "+ compare_file)
                        print(compare_file)
                        self.compare_file = compare_file
                        print(self.compare_file)
                        break
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

        # self.IP.main()
        self.IP.main(file_list,self.compare_file)
        # output =self.IP.Filter_IP(file_list)
        # print(output)
        # dictionary.update(output)
        # # IP_script.write(dictionary)
        # output2=self.IP.compare(output)
        # self.IP.timeline(output2)
    def virustotal_scanner(self, file_hash):
        print("Uploading hash to virustotal")

    # will check if an file exists, but need to implement an option to re add the file if it doesn't exist
    def exists(self,file,naam):

        if os.path.exists(file):
            with open("Hashes_"+naam+str(date.today())+ ".txt", 'a+') as f:
                f.write(file+ ':'+self.bereken_hash(file)+  '\n')
            (self.bereken_hash(file))
            return True
        else:
            return False

    # will shutdown the script
    def quit(self):
        self.Logging().info("Exiting script")
        print("Exiting script the log files are written to: " + self.log_location )
        sys.exit(0)

#this function will run the main function when script is called
if __name__ == "__main__":
    Main_program().run()
# start menu here and call individual scripts
#do something with logging
#error handling
