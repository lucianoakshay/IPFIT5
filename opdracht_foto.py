from __future__ import print_function
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from gmplot import gmplot
import sys, os
import tkinter as tk
from tkinter import filedialog
import texttable as tt
import User_Interface as ui
import foto_main as fotomain
import pyewf
import pytsk3
from io import BytesIO


def get_exif_data(image):
    """
    Returns a dictionary from the exif data of a PIL Image item. Also converts the GPS Tags.
    """
    try:
        exif_data = {}
        image = Image.open(BytesIO(image))
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
    except Exception as ex:
        pass
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


def get_lat_lon_from_imagefile(image):
    """
    Returns the latitude and longitude, if available, for a given image file.
    """
    #image = Image.open(BytesIO(image))
    exif_data = get_exif_data(image)

    return get_lat_lon(exif_data)

def get_lat_from_imagefile(image):
    """
    Returns the LAT if available, for a given image file.
    """
    #image = Image.open(BytesIO(image))
    exif_data = get_exif_data(image)

    return get_lat(exif_data)

def get_lon_from_imagefile(image):
    """
    Returns the LONGitude, if available, for a given image file.
    """
    #image = Image.open(BytesIO(image))
    exif_data = get_exif_data(image)

    return get_lon(exif_data)

def mapplotter(filename):
    gmap = gmplot.GoogleMapPlotter(52.370216, 4.895168, 5)
#    lat, lon = get_lat_lon_from_imagefile(filename)
#    gmap.marker(lat, lon, 'cornflowerblue')
#    gmap.draw("my_map_2.html")

    return None

def moremapplotter(image):
        gmap = gmplot.GoogleMapPlotter(52.370216, 4.895168, 8)

        myLat = []
        myLon = []

        for x in image:

            lon = (get_lon_from_imagefile(x))
            lat = (get_lat_from_imagefile(x))

            if type(lon) == int or type(lon) == float:
                myLon.append(lon)

            if type(lat) == int or type(lat) == float:
                myLat.append(lat)

        gmap.scatter(myLat, myLon, 'cornflowerblue', edge_width=100)

        gmap.draw("Export_Map.html")

        return None

def allebestanden(filepath):
    fotomain.EWFImgInfo.allfiles(filepath)

def allecamerabestanden(filepath):
    fotomain.EWFImgInfo.onlyphotofiles(filepath)

def showcameras(filepath):
    fotomain.EWFImgInfo.showcameras(filepath)

def fotosbijcamera(filepath):
    fotomain.EWFImgInfo.fotosbijcamera(filepath)

def exif_locatie(filepath):
    fotomain.EWFImgInfo.exif_locatie(filepath)

def exifinformatie(filepath):
    fotomain.EWFImgInfo.exifinformatie(filepath)
