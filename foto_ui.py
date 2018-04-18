# Individuele opdracht: Foto
# Auteur: Luciano Chanchal
# Student nr: s1103554
# Groep: 1
# User Interface opdracht foto
import os
import sys
import hashlib as hash
import logging
from datetime import date
import User_Interface as ui
import tkinter as tk
from tkinter import filedialog
import foto_main


class Main_program:
    BUFFERSIZE = 65536
    p = None

    # function that contain the foto menu choices
    def __init__(self):
        self.log_location = None
        self.choices_main = {
                "1": self.lijstallebestanden,
                "2": self.allecamerabestanden,
                "3": self.showcameras,
                "4": self.fotosbijcamera,
                "5": self.exif_locatie,
                "6": self.exif_informatie,
                "9": self.quit
                }

    # function that will print out the menu to the screen
    def display_main_menu(self):
        print("""
Foto Menu
1. List all files
2. List all camera files
3. List all camera brands and model
4. List all files including brand and model
5. List of all location information and export world-map
6. List of all relevant EXIF information
9. Quit
""")

    # function that start the script from User_Interface
    def main(self, log_location2):
        self.log_location = log_location2
        self.run()

    # will run the main program and ask for user input
    def run(self):
        ui.Main_program().Logging().info("Starting Foto_User_Interface")
        while True:
            self.display_main_menu()
            choice = input("Enter an option: ")
            action = self.choices_main.get(choice)
            ui.Main_program().Logging().info("User input: %s",choice)
            if action:
                action()
        #    elif choice == "9":
        #        break
            else:
                ui.Main_program().Logging().info("Invalid input, restarting script")
                print("{0} is not a valid choice".format(choice))

    # function that will open a file dialog for selecting the (E01) image
    def openfile():
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        return file_path

        """
        Explanation of functions:
        lijstallebestanden
        allecamerabestanden
        showcameras
        fotosbijcamera
        exif_locatie
        exif_informatie

        try:
** Open dialog and get filename **
            foto_image = Main_program.openfile()

** Check if E01 extension**
            if foto_image.endswith('.E01') == False:

** After 2 try's return to foto menu  **
        except Exception:
            self.run()


        try:
** Start selection with selected file **
            foto_main.allebestanden(foto_image)
** Do the logging **
            ui.Main_program().Logging().info("File: " + foto_image + " is selected")
            ui.Main_program().Logging().info("Starting List all files")
        except Exception:
** Error while running **
            print("Unknown file")
            ui.Main_program().Logging().info("Unknown error")
            self.run()
        sys.exit(0)

        """

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
            print(foto_image + " is selected as E01 file\n")
            print("This is the List all files that's now running")
            foto_main.EWFImgInfo.allfiles(foto_image)
            ui.Main_program().Logging().info("File: " + foto_image + " is selected")
            ui.Main_program().Logging().info("Starting List all files")
        except Exception:
            print("Unknown file")
            ui.Main_program().Logging().info("Unknown error")
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
            print(foto_image + " is selected as E01 file\n")
            print("This is the List all photo files that's now running")
            print("Please wait, this can take some time")
            foto_main.EWFImgInfo.onlyphotofiles(foto_image)
            ui.Main_program().Logging().info("File: " + foto_image + " is selected")
            ui.Main_program().Logging().info("Starting List all camera files")
        except Exception:
            print("Unknown file")
            ui.Main_program().Logging().info("Unknown error")
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
            print(foto_image + " is selected as E01 file\n")
            print("This is the List all found camera's that's now running")
            print("Please wait, this can take some time")
            foto_main.EWFImgInfo.showcameras(foto_image)
            ui.Main_program().Logging().info("File: " + foto_image + " is selected")
            ui.Main_program().Logging().info("Starting list all found camera's")
        except Exception:
            print("Unknown file")
            ui.Main_program().Logging().info("Unknown error")
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
            print(foto_image + " is selected as E01 file\n")
            print("This is the List all photo files and camera's that's now running")
            print("Please wait, this can take some time")
            foto_main.EWFImgInfo.fotosbijcamera(foto_image)
            ui.Main_program().Logging().info("File: " + foto_image + " is selected")
            ui.Main_program().Logging().info("Starting List all photo files and camera's")
        except Exception as ex:
            print(ex)
            print("Unknown file")
            ui.Main_program().Logging().info("Unknown error")
            self.run()
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
            print(foto_image + " is selected as E01 file\n")
            print("This is the Show EXIF location information that's now running")
            print("Please wait, this can take some time")
            foto_main.EWFImgInfo.exif_locatie(foto_image)
            ui.Main_program().Logging().info("File: " + foto_image + " is selected")
            ui.Main_program().Logging().info("Starting Show EXIF location Info")
        except Exception:
            print("Unknown file")
            ui.Main_program().Logging().info("Unknown error")
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
            print(foto_image + " is selected as E01 file\n")
            print("This is the Show EXIF information that's now running")
            print("Please wait, this can take some time")
            foto_main.EWFImgInfo.exifinformatie(foto_image)
            ui.Main_program().Logging().info("File: " + foto_image + " is selected")
            ui.Main_program().Logging().info("Starting Show EXIF Info")
        except Exception as ex:
            print(ex)
            print("Unknown file")
            ui.Main_program().Logging().info("Unknown error")
            self.run()
        sys.exit(0)

    # will shutdown the script and print to log file
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
# this function will run the main function when script is called
if __name__ == "__main__":
    Main_program().run()
