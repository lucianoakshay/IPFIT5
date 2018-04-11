# User Interface opdracht foto
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
                "6": self.exif_informatie,
            #    "9": self.quit
                }



    def back(self):
        Main_program().run()
    # This is the logging function that will be used to log the activity of this script.


    # function that will print out the menu to the screen, ( needs some minor changes)
    def display_main_menu(self):
        print("""
Foto Menu
1. List all files
2. List all camera files
3. List all camera brands and model
4. List all files including brand and model
5. List of all location information and export world-map
6. List of all relevant EXIF information
9. Go back to Main menu
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
            elif choice == "9":
                break
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
            print("Select the image file (.E01): ")
            if foto_image.endswith('.E01') == False:
                print(foto_image + " is not an E01 Image file. Please try again")
                foto_image = Main_program.openfile()
        except Exception:
            self.run()
        try:
            print(foto_image + " is selected as E01 file")
            print("This is the List all files that's now running")
            opdracht_foto.allebestanden(foto_image)
            ui.Main_program().Logging().info("Starting List all files")
        except Exception:
            print("Unknown file")
            self.run()
        sys.exit(0)

    def allecamerabestanden(self):
        try:
            foto_image = Main_program.openfile()
            print("Select the image file (.E01): ")
            if foto_image.endswith('.E01') == False:
                print(foto_image + " is not an E01 Image file. Please try again")
                foto_image = Main_program.openfile()
        except Exception:
            self.run()
        try:
            print(foto_image + " is selected as E01 file")
            print("This is the List all photo files that's now running")
            print("Please wait, this can take some time")
            opdracht_foto.allecamerabestanden(foto_image)
            ui.Main_program().Logging().info("Starting List all camera files")
        except Exception:
            print("Unknown file")
            self.run()
        sys.exit(0)
    def showcameras(self):
        try:
            foto_image = Main_program.openfile()
            print("Select the image file (.E01): ")
            if foto_image.endswith('.E01') == False:
                print(foto_image + " is not an E01 Image file. Please try again")
                foto_image = Main_program.openfile()
        except Exception:
            self.run()
        try:
            print(foto_image + " is selected as E01 file")
            print("This is the List all found camera's that's now running")
            print("Please wait, this can take some time")
            opdracht_foto.showcameras(foto_image)
            ui.Main_program().Logging().info("Starting list all found camera's")
        except Exception:
            print("Unknown file")
            self.run()
        sys.exit(0)

    def fotosbijcamera(self):
        try:
            foto_image = Main_program.openfile()
            print("Select the image file (.E01): ")
            if foto_image.endswith('.E01') == False:
                print(foto_image + " is not an E01 Image file. Please try again")
                foto_image = Main_program.openfile()
        except Exception:
            self.run()
        try:
            print(foto_image + " is selected as E01 file")
            print("This is the List all photo files and camera's that's now running")
            print("Please wait, this can take some time")
            opdracht_foto.fotosbijcamera(foto_image)
            ui.Main_program().Logging().info("Starting List all photo files and camera's")
        except Exception:
            print("Unknown file")
            self.run()
        sys.exit(0)

        ui.Main_program().Logging().info("Starting fotosbijcamera")
        print("This is the fotosbijcamera that's now running")
        opdracht_foto.fotosbijcamera()
        sys.exit(0)

    def exif_locatie(self):
        try:
            foto_image = Main_program.openfile()
            print("Select the image file (.E01): ")
            if foto_image.endswith('.E01') == False:
                print(foto_image + " is not an E01 Image file. Please try again")
                foto_image = Main_program.openfile()
        except Exception:
            self.run()
        try:
            print(foto_image + " is selected as E01 file")
            print("This is the Show EXIF location information that's now running")
            print("Please wait, this can take some time")
            opdracht_foto.exif_locatie(foto_image)
            ui.Main_program().Logging().info("Starting Show EXIF location Info")
        except Exception:
            print("Unknown file")
            self.run()
        sys.exit(0)

    def exif_informatie(self):
        try:
            foto_image = Main_program.openfile()
            print("Select the image file (.E01): ")
            if foto_image.endswith('.E01') == False:
                print(foto_image + " is not an E01 Image file. Please try again")
                foto_image = Main_program.openfile()
        except Exception:
            self.run()
        try:
            print(foto_image + " is selected as E01 file")
            print("This is the Show EXIF information that's now running")
            print("Please wait, this can take some time")
            opdracht_foto.exifinformatie(foto_image)
            ui.Main_program().Logging().info("Starting Show EXIF Info")
        except Exception:
            print("Unknown file")
            self.run()
        sys.exit(0)

    # will shutdown the script
    def quit(self):
        try:
            ui.Main_program().Logging().info("Exiting script")
            print("Exiting script the log files are written to: " + self.log_location )
            sys.exit(0)
        except Exception:
            ui.Main_program().Logging().info("Exiting script")
            print("Exiting script the log files are written to: " + self.log_location )
            sys.exit(0)
            pass
#this function will run the main function when script is called
if __name__ == "__main__":
    Main_program().run()
# start menu here and call individual scripts
#do something with logging
#error handling
