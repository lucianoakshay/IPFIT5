from __future__ import print_function
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from gmplot import gmplot
from tqdm import tqdm
import sys, os
import tkinter as tk
from tkinter import filedialog
import texttable as tt
import table
import User_Interface as ui
import csv


def get_exif_data(image):
    """
    Returns a dictionary from the exif data of a PIL Image item. Also converts the GPS Tags.
    """
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data


def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format.
    """
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(exif_data):
    """
    Returns the latitude and longitude, if available,
    from the provided exif_data (obtained through get_exif_data above).
    """
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon

def get_lat(exif_data):
    """
    Returns the latitude and longitude, if available,
    from the provided exif_data (obtained through get_exif_data above).
    """
    lat = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')

        if gps_latitude and gps_latitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

    return lat

def get_lon(exif_data):
    """
    Returns the latitude and longitude, if available,
    from the provided exif_data (obtained through get_exif_data above).
    """
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]


        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_longitude and gps_longitude_ref:

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lon


def get_lat_lon_from_imagefile(filename):
    """
    Returns the latitude and longitude, if available, for a given image file.
    """
    image = Image.open(filename)
    exif_data = get_exif_data(image)

    return get_lat_lon(exif_data)

def get_lat_from_imagefile(filename):
    """
    Returns the LAT if available, for a given image file.
    """
    image = Image.open(filename)
    exif_data = get_exif_data(image)

    return get_lat(exif_data)

def get_lon_from_imagefile(filename):
    """
    Returns the LONGitude, if available, for a given image file.
    """
    image = Image.open(filename)
    exif_data = get_exif_data(image)

    return get_lon(exif_data)

def mapplotter(filename):
    gmap = gmplot.GoogleMapPlotter(52.370216, 4.895168, 5)
#    lat, lon = get_lat_lon_from_imagefile(filename)
#    gmap.marker(lat, lon, 'cornflowerblue')
#    gmap.draw("my_map_2.html")

    return None

def moremapplotter(foldername, myList):
        gmap = gmplot.GoogleMapPlotter(52.370216, 4.895168, 8)
#        file_lat, file_lon = get_lat_lon_from_imagefile(filename)
#        gmap.marker(lat, lon, 'cornflowerblue')
#        gmap.draw("my_map_2.html")

#        if os.path.isfile(filename):
#            for file in os.listdir("./fotos"):
#                print(os.path.join(file))
#        print(get_lat_lon_from_imagefile(filename))

#        myList = filesinmap(foldername)
        myextraList = []

        for x in myList:
            myextraList.append(get_lat_lon_from_imagefile(foldername + '/' + x))
#            myextraList.append(file_lat, file_lon = get_lat_lon_from_imagefile(x))
        for x in myextraList:
#            gmap.marker(x, 'cornflowerblue')
#            print(foldername + '/' + x)
#        myextraList.split(",")
#        print(myextraList)
            lats, lons = zip(*[x])
#            print(x)
            gmap.scatter(lats, lons, 'cornflowerblue', edge_width=100)
#            gmap.marker(51.904444444444444, 4.351388888888889, 'cornflowerblue')
        gmap.draw("my_map_2.html")

        return None

def filesinmap(foldername):
        myList = []
        for file in os.listdir(foldername):
    #        print(os.path.join(file))
            myList.append(file)
#            ui.bereken_hash(file)

        return myList
def file_list(mounting_dir):
    # Dictionary om alle files met hashes erbij op te slaan
    file_dict = {}

    # File counter die aan het begin alle files telt voor de progress bar
    filecounter = 0
    for filepath in self.walkdir(mounting_dir):
        filecounter += 1

    for filepath in tqdm(self.walkdir(mounting_dir), total=filecounter, unit="files"):
        hash_waarde = bereken_hash2(filepath)
        filename, file_extension = os.path.splitext(filepath)
        file_dict[filename] = {"Extension": file_extension, "Hash value": hash_waarde}

    print(file_dict)
    print(len(file_dict))
    return file_dict

def walkdir(folder):
    """Walk through each files in a directory"""
    for dirpath, dirs, files in os.walk(folder):
        for filename in files:
            yield os.path.abspath(os.path.join(dirpath, filename))

def file_lijst(mounting_dir):
    # Dictionary om alle files met hashes erbij op te slaan
    file_dict = {}

    # File counter die aan het begin alle files telt voor de progress bar
    filecounter = 0
    for filepath in walkdir(mounting_dir):
        filecounter += 1

    for filepath in tqdm(walkdir(mounting_dir), total=filecounter, unit="files"):
        hash_waarde = ui.Main_program().bereken_hash(filepath)
        filename, file_extension = os.path.splitext(filepath)
        file_dict[filename] = {"Extension": file_extension, "Hash value": hash_waarde}

    excel(file_dict)
    print(file_dict)
    print(len(file_dict))
    return file_dict

def excel(file_dict):
    with open("/home/ipfit5/Desktop/github/IPFIT5/14-maart/IPFIT5/test.csv", "w", newline ='') as outfile:
        fieldnames = ['FileName','Extension', 'Hash']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
#        for entries in file_dict:
        writer.writerows(file_dict)
#            outfile.write("\n")
#            print(file_dict)

#        for entries in file_dict:
#            outfile.write(entries)
#            outfile.write("\n")
#            print(file_dict)

def exifinformatie(image):
    # https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html
    # Datum + tijd = 36867
    exif_data = {}
    image = Image.open(image)
    info = image._getexif()
    model = "Model"
    make = "Make"
    datum = "DateTimeOriginal"
    datum1 ="DateTimeDigitized"
    datum2 = "DateTime"

    lijst = ['Make', 'Model']
    namelist = ['Merk', 'Model']
    if info:
        for x in lijst:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == x:
                    listindex = lijst.index(x)
                    print(namelist[listindex])
                    print(value)

            # if decoded == model:
            #     print("Model")
            #     print(value)
            # if decoded == make:
            #     print("Merk")
            #     print(value)
            #     gps_data = {}
            #     for t in value:
            #         sub_decoded = GPSTAGS.get(t, t)
            #         gps_data[sub_decoded] = value[t]
            #
            #     exif_data[decoded] = gps_data
            # else:
            #     exif_data[decoded] = value

    return None
#    return Image.open(filename)._getexif()[271][272]


def voorbeeld(image):
    """
    Returns a dictionary from the exif data of a PIL Image item. Also converts the GPS Tags.
    """
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data
if __name__ == "__main__":

#    root = tk.Tk()
#    root.withdraw()

#    filename = filedialog.askopenfilename()

#    filename = sys.argv[1]

#    if os.path.isfile(filename):
#        for file in os.listdir("./fotos"):
#            print(os.path.join(file))
#    print(get_lat_lon_from_imagefile(filename))
#    mapplotter(filename)

    foldername = "/home/ipfit5/Desktop/github/IPFIT5/14-maart/IPFIT5/fotos"
#    print(filesinmap(foldername))
#    file_lijst(foldername)
    moremapplotter(foldername, filesinmap(foldername))
    table.tabel(foldername)
#    print(ui.Main_program().bereken_hash("/home/ipfit5/Desktop/github/IPFIT5/14-maart/IPFIT5/fotos/20170115_183156.jpg"))
#    for file in os.listdir(foldername):
#        print(ui.Main_program().bereken_hash(foldername + "/" + file))
#        print(foldername + "/" + file)
#        exifinformatie(foldername + "/" + file)
