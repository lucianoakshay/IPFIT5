import os
import sys
class Main_program:
    BUFFERSIZE =65536
    def __init__(self):
        self.choices = {
                "1": self.IP_script,
                "2": self.Foto_script,
                "3": self.Gehakt_script,
                "4": self.Easy_hash_calc,
                "5": self.quit
                }

    def bereken_hash(self,bestand):
        sha256hash = hash.sha3_256()
        if os.path.isfile(bestand) and os.access(bestand, os.R_OK):
            with open((bestand),'rb') as file:
                file_buffer = file.read(self.BUFFERSIZE)
                while len(file_buffer)>0:
                    sha256hash.update(file_buffer)
                    file_buffer= file.read(self.BUFFERSIZE)
        else:
            print("File does not exist or is not accessible")
        return(sha256hash.hexdigest())
    def display_menu(self):
        print("""
Menu
1. Run_IP_script
2. Run_Foto_script
3. Run_gehakt_script
4. Run_Easy_hash_script
5. Quit
""")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def IP_script(self):
        print("This is the IP_script that's now running")

    def Foto_script(self):
        print("THis is the Foto_script that's now running")

    def Gehakt_script(self):
        print("This is the Gehakt_script that's now running")

    def Easy_hash_calc(self):
        print("hash calculator")

    def quit(self):
        print("Exiting script the log files are written to: ")
        sys.exit(0)

if __name__ == "__main__":
    Main_program().run()
# start menu here and call individual scripts
#do something with logging
#error handling
