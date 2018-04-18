# Individuele opdracht: Foto
# Auteur: Luciano Chanchal
# Student nr: s1103554
# Groep: 1
# Main applicatie opdracht foto
import os,sys
import pyewf
import pytsk3
import texttable as tt
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from io import BytesIO
import fleep
from collections import defaultdict
import exifmap_export
import datetime
from datetime import date

class EWFImgInfo(pytsk3.Img_Info):
        def __init__(self, ewf_handle):
            self._ewf_handle = ewf_handle
            super(EWFImgInfo, self).__init__(
                url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

        def close(self):
            self._ewf_handle.close()

        def read(self, offset, size):
            self._ewf_handle.seek(offset)
            return self._ewf_handle.read(size)

        def get_size(self):
            return self._ewf_handle.get_media_size()

        # Open the files inside the E01 image and return the opened data
        def open_file(fs_object):
            offset = 0
            buff_size = 1024 * 1024
            size = getattr(fs_object.info.meta, "size", 0)
            naam = (fs_object.info.name.name.decode('UTF-8'))

            sha256_sum = hashlib.sha256()
            while offset < size:
                size = getattr(fs_object.info.meta, "size", 0)
                available_to_read = min(buff_size, size - offset)
                data = fs_object.read_random(offset, available_to_read)
                return data

                if not data:
                    break
                offset += len(data)

        # Get the camera Type of the EXIF tags
        def exif_type(data):
                image = Image.open(BytesIO(data))
                info = image._getexif()
                if info:
                    for tag, value in info.items():
                        decoded = TAGS.get(tag, tag)
                        if decoded == "Model":
                            return value

        # Get the camera Brand of the EXIF tags
        def exif_merk(data):
                image = Image.open(BytesIO(data))
                info = image._getexif()
                if info:
                    for tag, value in info.items():
                        decoded = TAGS.get(tag, tag)
                        if decoded == "Make":
                            return value

        # Get the photo Taken Date from the EXIF tags
        def exif_datum(data):
                image = Image.open(BytesIO(data))
                info = image._getexif()
                if info:
                    for tag, value in info.items():
                        decoded = TAGS.get(tag, tag)
                        if decoded == "DateTimeOriginal":
                            return value

        # Delete and filter double rows in a list
        def deldouble(xs, top=10):
            counts = defaultdict(int)
            for x in xs:
                counts[x] += 1
            return sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]

        # Check if real photo file
        # This function take some time..
        # But is accurate
        def checkcamera(bestand):
            info = fleep.get(bestand)
            return info.type_matches("raster-image")

        # This function write the output of the terminal
        # To the file with the fuctionname and date
        # output = the text / table
        # option = number 1-6 of the Menu
        # name = name of the fuction that calls this fuction
        # filepath = the filepath of the e01
        def printoutput(output, option, name, filepath):
            try:
                datum = str(date.today())
                datumentijd = str(datetime.datetime.today())

                path = os.path.join(sys.path[0], 'output', str(name) + '_' + datum + '.txt')
                f = open(path, 'w')
                f.write("\nRecorded date and time: " + datumentijd + "\n")
                f.write("\nInput file: " + str(filepath) + "\n")
                f.write("\nFoto Menu Choice : " + option + "\n")
                f.write("\nChoice name: " + name + "\n \n")

                f.write(output)  # write the real output
                f.close()  # Close the writer
                print("\nOutput of option " + option + " is exported to: " + path )
            except Exception as ex:
                print(ex)
                pass

# Choice 1 of Foto Menu
        # print all files of the E01 in table
        # filename, size, sha256, md5, count
        def allfiles(filepath):

            filenames = pyewf.glob(filepath)

            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            img_info = EWFImgInfo(ewf_handle)
            vol = pytsk3.Volume_Info(img_info)
            for part in vol:
                    if part.len > 2048:

                        fs = pytsk3.FS_Info(img_info, offset=part.start * vol.info.block_size)
                        root = fs.open_dir(path="/")

                        myListName = [] # List for filenames
                        myListSize = [] # List for sizes
                        hashwaarde = [] # List for SHA256 hash
                        md5hashwaarde = [] # List for MD5 hash
                        cijfer = 0 # Start for count in myCijfer
                        myCijfer = [] # List for counting the number of files
                        for fs_object in root: # For every file in root
                                try:
                                    realfile = (EWFImgInfo.open_file(fs_object))
                                    file_size = getattr(fs_object.info.meta, "size", 0)
                                    file_name = fs_object.info.name.name.decode('UTF-8')

                                    myListName.append(file_name)
                                    myListSize.append(file_size)
                                    cijfer = cijfer + 1
                                    myCijfer.append(cijfer)
                                    sha256 = (hashlib.sha256(realfile).hexdigest())
                                    md5 = (hashlib.md5(realfile).hexdigest())

                                    if sha256 is "Error":
                                        hashwaarde.append("-")
                                        md5hashwaarde.append("-")
                                    else:
                                        hashwaarde.append(sha256)
                                        md5hashwaarde.append(md5)

                                except Exception as ex:
                                    hashwaarde.append("-")
                                    md5hashwaarde.append("-")

            tab = tt.Texttable() # tab = name of the texttable
            tab.set_cols_dtype(['a', 'a', 'a', 'a', 'a']) # Set colum type
            tab.set_cols_width([25,15,65,40,4]) # Set colum width

            headings = ['Bestandsnaam', 'Bestandsgrootte','SHA256', "MD5", 'Nr.']

            # Assign to new variable for the table
            tab.header(headings)
            names = myListName
            size = myListSize
            hashw = hashwaarde
            md5hashw = md5hashwaarde
            nummer = myCijfer

            # Add every list to the table
            for row in zip(names, size, hashw, md5hashw, nummer):
                tab.add_row(row)

            s = tab.draw() # Create the table
            print (s) # Print the table
            EWFImgInfo.printoutput(s, "1", "allfiles", filepath)

            return None

# Choice 2 of Foto Menu
        def onlyphotofiles(filepath):

            filenames = pyewf.glob(filepath)

            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            img_info = EWFImgInfo(ewf_handle)
            vol = pytsk3.Volume_Info(img_info)
            for part in vol:
                    if part.len > 2048:

                        fs = pytsk3.FS_Info(img_info, offset=part.start * vol.info.block_size)

                        root = fs.open_dir(path="/")

                        myListName = []
                        myListSize = []
                        hashwaarde = []
                        md5hashwaarde = []
                        cijfer = 0
                        myCijfer = []
                        for fs_object in root:
                                try:
                                    if EWFImgInfo.checkcamera(EWFImgInfo.open_file(fs_object)):
                                        file_size = getattr(fs_object.info.meta, "size", 0)
                                        file_name = fs_object.info.name.name.decode('UTF-8')

                                        myListName.append(file_name)
                                        myListSize.append(file_size)
                                        cijfer = cijfer + 1
                                        myCijfer.append(cijfer)

                                        hash_obj_sha256 = hashlib.sha256()
                                        hash_obj_md5 = hashlib.md5()
                                        if hash_obj_sha256 is "Error":
                                            hashwaarde.append("-")
                                            md5hashwaarde.append("-")

                                        else:
                                            hash_obj_md5.update(fs_object.read_random(0, file_size))
                                            hash_obj_sha256.update(fs_object.read_random(0, file_size))

                                            hash_w = hash_obj_sha256.hexdigest()
                                            hashwaarde.append(hash_w)

                                            hash_w_md5 = hash_obj_md5.hexdigest()
                                            md5hashwaarde.append(hash_w_md5)

                                except Exception as ex:
                                    pass


            tab = tt.Texttable()
            tab.set_cols_dtype(['a', 'a', 'a', 'a', 'a'])
            tab.set_cols_width([25,15,65,40,4])

            headings = ['Bestandsnaam', 'Bestandsgrootte','SHA256', "MD5", 'Nr.']
            tab.header(headings)
            names = myListName
            size = myListSize
            hashw = hashwaarde
            md5hashw = md5hashwaarde
            nummer = myCijfer


            for row in zip(names, size, hashw, md5hashw, nummer):
                tab.add_row(row)

            s = tab.draw()
            print (s)
            EWFImgInfo.printoutput(s, "2", "onlyphotofiles", filepath)

            return None

# Choice 3 of Foto Menu
        def showcameras(filepath):

            filenames = pyewf.glob(filepath)

            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            img_info = EWFImgInfo(ewf_handle)
            vol = pytsk3.Volume_Info(img_info)
            for part in vol:
                    if part.len > 2048:

                        fs = pytsk3.FS_Info(img_info, offset=part.start * vol.info.block_size)

                        root = fs.open_dir(path="/")


                        myType = []
                        myMerk = []

                        for fs_object in root:
                                try:
                                    #print(fs_object.info.name.name.decode('UTF-8'))
                                    if EWFImgInfo.checkcamera(EWFImgInfo.open_file(fs_object)):
                                        merk = EWFImgInfo.exif_type(EWFImgInfo.open_file(fs_object))
                                        typec = EWFImgInfo.exif_merk(EWFImgInfo.open_file(fs_object))
                                        if merk is None:
                                            myType.append("Onbekend")
                                            myMerk.append("Onbekend")
                                        else:
                                            myType.append(typec)
                                            myMerk.append(merk)

                                except Exception as ex:
                                    if str(ex) != "object type must be bytes":
                                        myType.append("Onbekend")
                                        myMerk.append("Onbekend")
                                    else:
                                        pass



            tab = tt.Texttable()
            tab.set_cols_dtype(['t', 't'])
            tab.set_cols_width(['30', '30'])


            headings = ['Merk', 'Model/type']
            tab.header(headings)
            merkcam = myMerk
            typecam = myType

            for row in zip(merkcam, typecam):
                tab.add_row(row)

            s1 = tab.draw()
            print(s1 + "\n")

            tab2 = tt.Texttable()
            tab2.set_cols_dtype(['a'])

            headings2 = ['Merk  |  Aantal']
            tab2.header(headings2)
            merkcam2 = EWFImgInfo.deldouble(myMerk)

            for row in zip(merkcam2):
                tab2.add_row(row)

            s2 = tab2.draw()
            print(s2 + "\n")

            tab3 = tt.Texttable()
            tab3.set_cols_dtype(['a'])

            headings3 = ['Type  |  Aantal']
            tab3.header(headings3)
            typecam3 = EWFImgInfo.deldouble(myType)

            for row in zip(typecam3):
                tab3.add_row(row)

            s3 = tab3.draw()
            print(s3)

            s = s1 + "\n" + "\n" + s2 + "\n" + s3
            EWFImgInfo.printoutput(s, "3", "showcameras", filepath)

            return None

# Choice 4 of Foto Menu
        def fotosbijcamera(filepath):

            filenames = pyewf.glob(filepath)

            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            img_info = EWFImgInfo(ewf_handle)
            vol = pytsk3.Volume_Info(img_info)
            for part in vol:
                    if part.len > 2048:

                        fs = pytsk3.FS_Info(img_info, offset=part.start * vol.info.block_size)

                        root = fs.open_dir(path="/")

                        cijfer = 0
                        myCijfer = []
                        myModellen = []
                        myFilenames = []
                        myMerk = []


                        for fs_object in root:
                            try:
                                cijfer = cijfer + 1
                                myCijfer.append(cijfer)
                                if EWFImgInfo.checkcamera(EWFImgInfo.open_file(fs_object)):
                                    typec = EWFImgInfo.exif_type(EWFImgInfo.open_file(fs_object))
                                    merk = EWFImgInfo.exif_merk(EWFImgInfo.open_file(fs_object))
                                    myFilenames.append(fs_object.info.name.name.decode('UTF-8'))
                                    if merk is None:
                                        myModellen.append("Onbekend")
                                        myMerk.append("Onbekend")
                                    else:
                                        myModellen.append(typec)
                                        myMerk.append(merk)

                            except Exception as ex:
                                if str(ex) != "object type must be bytes":
                                    myModellen.append("Onbekend")
                                    myMerk.append("Onbekend")
                                else:
                                    pass

            myMerk, myModellen, myFilenames = zip(*sorted(zip(myMerk, myModellen, myFilenames)))

            tab = tt.Texttable()
            tab.set_cols_dtype(['a', 'a', 'a', 'a'])

            headings = ['Bestandsnaam', 'Merk', 'Type', 'NR.']
            tab.header(headings)
            names = myFilenames
            merkcam = myMerk
            typecam = myModellen
            nummer = myCijfer


            for row in zip(names, merkcam, typecam, nummer):
                tab.add_row(row)

            s = tab.draw()
            print (s)
            EWFImgInfo.printoutput(s, "4", "fotosbijcamera", filepath)
            return None

# Choice 5 of Foto Menu
        def exif_locatie(filepath):

            filenames = pyewf.glob(filepath)

            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            img_info = EWFImgInfo(ewf_handle)
            vol = pytsk3.Volume_Info(img_info)
            for part in vol:
                    if part.len > 2048:

                        fs = pytsk3.FS_Info(img_info, offset=part.start * vol.info.block_size)

                        root = fs.open_dir(path="/")

                        myFilenames = []
                        files = []
                        myLat = []
                        myLon = []

                        for fs_object in root:
                            try:
                                if EWFImgInfo.checkcamera(EWFImgInfo.open_file(fs_object)):
                                    files.append(EWFImgInfo.open_file(fs_object))
                                    myFilenames.append(fs_object.info.name.name.decode('UTF-8'))
                            except Exception as ex:
                                pass
            exifmap_export.moremapplotter(files)

            for x in files:
                myLat.append(exifmap_export.get_lat_from_imagefile(x))
                myLon.append(exifmap_export.get_lon_from_imagefile(x))

            tab = tt.Texttable()
            tab.set_cols_dtype(['a', 'f', 'f'])
            #
            headings = ['Bestandsnaam', 'Latitude', 'Longitude']
            tab.header(headings)
            names = myFilenames
            latitude = myLat
            longitude = myLon

            for row in zip(names, latitude, longitude):
                tab.add_row(row)
            #
            s = tab.draw()
            print (s)
            EWFImgInfo.printoutput(s, "5", "exif_locatie", filepath)
            return None

# Choice 6 of Foto Menu
        def exifinformatie(filepath):

            filenames = pyewf.glob(filepath)

            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            img_info = EWFImgInfo(ewf_handle)
            vol = pytsk3.Volume_Info(img_info)
            for part in vol:
                    if part.len > 2048:

                        fs = pytsk3.FS_Info(img_info, offset=part.start * vol.info.block_size)

                        root = fs.open_dir(path="/")

                        cijfer = 0
                        myCijfer = []
                        myFilenames = []
                        myDatum = []

                        for fs_object in root:
                            try:
                                cijfer = cijfer + 1
                                myCijfer.append(cijfer)
                                if EWFImgInfo.checkcamera(EWFImgInfo.open_file(fs_object)):
                                    myFilenames.append(fs_object.info.name.name.decode('UTF-8'))
                                    datum = EWFImgInfo.exif_datum(EWFImgInfo.open_file(fs_object))

                                    if datum is None:
                                        myDatum.append("Onbekend")
                                    else:
                                        myDatum.append(datum)

                            except Exception as ex:
                                if str(ex) != "object type must be bytes":
                                    myDatum.append("Onbekend")
                                else:
                                    pass

            tab = tt.Texttable()
            tab.set_cols_dtype(['a', 'a', 'a'])

            headings = ['Bestandsnaam', 'Datum en Tijd opname', 'NR.']
            tab.header(headings)
            names = myFilenames
            datum = myDatum
            nummer = myCijfer


            for row in zip(names, datum, nummer):
                tab.add_row(row)

            s = tab.draw()
            print (s)
            EWFImgInfo.printoutput(s, "6", "exifinformatie", filepath)

            return None
