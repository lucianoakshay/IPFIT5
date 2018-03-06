import os
import sys
import hashlib as hash
import logging
import opdracht_IP
class Main_program:
    BUFFERSIZE =65536

    p = None
    def __init__(self):
        self.p = opdracht_IP.IP_filtering()
        self.choices_main = {
                "1": self.IP_script,
                "2": self.Foto_script,
                "3": self.Gehakt_script,
                "4": self.Easy_hash_calc,
                "5": self.quit
                }
        self.e01=False

    # bestandsnaam toevoegen
    def Logging(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(sys.path[0],'Main.log'))
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def bereken_hash(self,bestand):
        sha256hash = hash.sha3_256()
        if os.path.isfile(bestand) and os.access(bestand, os.R_OK):
            with open((bestand),'rb') as file:
                file_buffer = file.read(self.BUFFERSIZE)
                while len(file_buffer)>0:
                    sha256hash.update(file_buffer)
                    file_buffer= file.read(self.BUFFERSIZE)
        else:
            self.Logging(bestand+": File does not exist or is not accessible")

        return(sha256hash.hexdigest())

    def display_main_menu(self):
        print("""
Menu
1. Run_IP_script
2. Run_Foto_script
3. Run_gehakt_script
4. Run_Easy_hash_script
5. Quit
""")



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

    def IP_script(self):


        # import opdracht_IP
        self.Logging().info("Starting IP_Script")
        self.p.convert_IP(self.Input_file())
        print("This is the IP_script that's now running")

    def Foto_script(self):
        self.e01=True
        self.Logging().info("Starting Foto_Script")

        print("THis is the Foto_script that's now running")

    def Gehakt_script(self):
        self.e01=True
        self.Logging().info("Starting Gehakt_Script")
        print("This is the Gehakt_script that's now running")

    def Easy_hash_calc(self):
        print("hash calculator")

    def Input_file(self):
        file_list=[]
        if self.e01:

            print("Please enter an file name:")
            filename =input()
            if self.exists(filename):

                return filename
            else:
                self.Logging().info("File: "+filename+"doesn't exists")
                print("File doesn't exists, restarting script...")
                self.run()

        else:
            aantal = int(input('Input the ammount of files'))
        #fout afhandeling
            for i in range(aantal):
                test = input('Input file: ')
                if(self.exists(test)):

                    file_list.append(os.path.abspath(test))
                else:
                    self.Logging().info("File: "+test+" doesn't exists")

                    print("File:"+test+ "doesn't exists, restarting script...")
                    # file_list.remove(test)
                    # maybe add option to continu after wrong file name
                    self.run()
            return test

    def exists(self,file):

        if os.path.exists(file):
            return True
        else:
            return False

    def quit(self):
        self.Logging().info("Exiting script")
        print("Exiting script the log files are written to: ")
        sys.exit(0)



if __name__ == "__main__":
    Main_program().run()
# start menu here and call individual scripts
#do something with logging
#error handling
