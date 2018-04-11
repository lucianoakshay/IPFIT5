# gezamenlijk deel Groep 1
#
import os
import sys
import hashlib as hash
import logging
import opdracht_IP
import opdracht_Gehakt
import opdracht_foto
from datetime import date
import User_Interface as ui
import tkinter as tk
from tkinter import filedialog


class Main_program:
    BUFFERSIZE = 65536
    p = None
    def __init__(self):
        self.log_location = None
        self.choices_main = {
                "1": self.lijstallebestanden,
                "2": self.allecamerabestanden,
                "3": self.showcameras,
                "4": self.fotosbijcamera,
                "5": self.exif_locatie,
                "9": self.quit
                }



    def back(self):
        Main_program().run()
    # This is the logging function that will be used to log the activity of this script.


    # function that will print out the menu to the screen, ( needs some minor changes)
    def display_main_menu(self):
        print("""
Menu
1. Lijst van alle bestanden
2. Lijst van alle camera bestanden
3. Lijst van alle camera's en modellen
4. Lijst van alle fotos horende bij de camera
5. Lijst en export met locatie gegevens
9. Quit
""")

    def main(self, log_location2):
        self.log_location = log_location2
        self.run()

    # will run the main program
    def run(self):
        ui.Main_program().Logging().info("Starting Foto_User_Interface")
        while True:
            self.display_main_menu()
            choice = input("Enter an option: ")
            action = self.choices_main.get(choice)
            ui.Main_program().Logging().info("User input: %s",choice)
            if action:
                action()
            else:
                ui.Main_program().Logging().info("Invalid input, restarting script")
                print("{0} is not a valid choice".format(choice))

    def openfile():
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        return file_path

    def lijstallebestanden(self):
        try:
            foto_image = Main_program.openfile()
            if foto_image.endswith('.E01') == False:
                print(foto_image + " is not an E01 Image file. Please try again")
                foto_image = Main_program.openfile()
        except Exception:
            Main_program()
        try:
            print("This is the List all files that's now running")
            opdracht_foto.allebestanden(foto_image)
            ui.Main_program().Logging().info("Starting List all files")
        except Exception:
            print("Unknown file")
            Main_program().run()
        sys.exit(0)

    def allecamerabestanden(self):
        ui.Main_program().Logging().info("Starting List all camera files")
        print("This is the allecamerabestanden that's now running")
        print("Ogenblik, dit kan even duren")
        opdracht_foto.allecamerabestanden()
        sys.exit(0)

    def showcameras(self):
        ui.Main_program().Logging().info("Starting showcameras")
        print("This is the showcameras that's now running")
        opdracht_foto.showcameras()
        sys.exit(0)

    def fotosbijcamera(self):
        ui.Main_program().Logging().info("Starting fotosbijcamera")
        print("This is the fotosbijcamera that's now running")
        opdracht_foto.fotosbijcamera()
        sys.exit(0)

    def exif_locatie(self):
        ui.Main_program().Logging().info("Starting exif_locatie")
        print("This is the exif_locatie that's now running")
        opdracht_foto.exif_locatie()
        sys.exit(0)

    # will shutdown the script
    def quit(self):
        ui.Main_program().Logging().info("Exiting script")
        print("Exiting script the log files are written to: " + self.log_location )
        sys.exit(0)

#this function will run the main function when script is called
if __name__ == "__main__":
    Main_program().run()
# start menu here and call individual scripts
#do something with logging
#error handling
