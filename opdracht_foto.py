from __future__ import print_function
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from gmplot import gmplot
#import User_Interface
#from tqdm import tqdm
import sys, os
import tkinter as tk
from tkinter import filedialog

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


def get_lat_lon_from_imagefile(filename):
    """
    Returns the latitude and longitude, if available, for a given image file.
    """
    image = Image.open(filename)
    exif_data = get_exif_data(image)

    return get_lat_lon(exif_data)

def mapplotter(filename):
    gmap = gmplot.GoogleMapPlotter(52.370216, 4.895168, 5)
    lat, lon = get_lat_lon_from_imagefile(filename)
    gmap.marker(lat, lon, 'cornflowerblue')
    gmap.draw("my_map.html")

    return None

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    filename = filedialog.askopenfilename()

#    filename = sys.argv[1]

#    if os.path.isfile(filename):
#    for file in os.listdir("./fotos"):
#            print(os.path.join(file))
    print(get_lat_lon_from_imagefile(filename))
    mapplotter(filename)
