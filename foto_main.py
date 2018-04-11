import os,sys
import pyewf
import pytsk3
import texttable as tt
import User_Interface as ui
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from io import BytesIO
import fleep
from collections import defaultdict
import opdracht_foto

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


        def open_file(fs_object):

            offset = 0
            buff_size = 1024 * 1024
            size = getattr(fs_object.info.meta, "size", 0)
            naam = (fs_object.info.name.name.decode('UTF-8'))
            myNaam = []
            myData = []


            sha256_sum = hashlib.sha256()
            while offset < size:
        #        print(naam)
                size = getattr(fs_object.info.meta, "size", 0)
                available_to_read = min(buff_size, size - offset)
                data = fs_object.read_random(offset, available_to_read)
                return data

                if not data:
                    break
                offset += len(data)

        def exif_type(data):
                image = Image.open(BytesIO(data))
                info = image._getexif()
                if info:
                    for tag, value in info.items():
                        decoded = TAGS.get(tag, tag)
                        if decoded == "Model":
                            return value

        def exif_merk(data):
                image = Image.open(BytesIO(data))
                info = image._getexif()
                if info:
                    for tag, value in info.items():
                        decoded = TAGS.get(tag, tag)
                        if decoded == "Make":
                            return value

        def exif_datum(data):
                image = Image.open(BytesIO(data))
                info = image._getexif()
                if info:
                    for tag, value in info.items():
                        decoded = TAGS.get(tag, tag)
                        if decoded == "DateTimeOriginal":
                            return value

        def leaders(xs, top=10):
            counts = defaultdict(int)
            for x in xs:
                counts[x] += 1
            return sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]

        def checkcamera(bestand):
            info = fleep.get(bestand)
            return info.type_matches("raster-image")

        def remove_duplicates(values):
            output = []
            seen = set()
            for value in values:
                # If value has not been encountered yet,
                # ... add it to both list and set.
                if value not in seen:
                    output.append(value)
                    seen.add(value)
            return output

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

                        myListName = []
                        myListSize = []
                        hashwaarde = []
                        md5hashwaarde = []
                        count = []
                        cijfer = 0
                        myCijfer = []
                        for fs_object in root:
                                try:
                                    #EWFImgInfo.read_file(fs_object)
                            #        EWFImgInfo.read_file(fs_object)
                            #        EWFImgInfo.open_file(fs_object)
                            #        EWFImgInfo.exifinfo2(EWFImgInfo.open_file(fs_object))
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
                                    hashwaarde.append("-")
                                    md5hashwaarde.append("-")


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

            return None

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
                        count = []
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

            return None

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
                                        myType.append(EWFImgInfo.exif_type(EWFImgInfo.open_file(fs_object)))
                                        myMerk.append(EWFImgInfo.exif_merk(EWFImgInfo.open_file(fs_object)))

                                except Exception as ex:
                                    if str(ex) != "object type must be bytes":
                                        myType.append("Onbekend")
                                        myMerk.append("Onbekend")
                                    else:
                                        pass



            tab = tt.Texttable()
            tab.set_cols_dtype(['a', 'a'])

            headings = ['Merk', 'Model/type']
            tab.header(headings)
            merkcam = myMerk
            typecam = myType

            for row in zip(merkcam, typecam):
                tab.add_row(row)

            s = tab.draw()
            print(s + "\n")

            tab2 = tt.Texttable()
            tab2.set_cols_dtype(['a'])

            headings2 = ['Merk  |  Aantal']
            tab2.header(headings2)
            merkcam2 = EWFImgInfo.leaders(myMerk)

            for row in zip(merkcam2):
                tab2.add_row(row)

            s2 = tab2.draw()
            print(s2 + "\n")

            tab3 = tt.Texttable()
            tab3.set_cols_dtype(['a'])

            headings3 = ['Type  |  Aantal']
            tab3.header(headings3)
            typecam3 = EWFImgInfo.leaders(myType)

            for row in zip(typecam3):
                tab3.add_row(row)

            s3 = tab3.draw()
            print(s3)

            return None

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
                                    myFilenames.append(fs_object.info.name.name.decode('UTF-8'))
                                    myModellen.append(EWFImgInfo.exif_type(EWFImgInfo.open_file(fs_object)))
                                    myMerk.append(EWFImgInfo.exif_merk(EWFImgInfo.open_file(fs_object)))

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

            return None

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
            opdracht_foto.moremapplotter(files)

            for x in files:
                myLat.append(opdracht_foto.get_lat_from_imagefile(x))
                myLon.append(opdracht_foto.get_lon_from_imagefile(x))

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
            print("\n A world-map with all the locations is exported to: 'Export_Map.html'")

            return None

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
                                    myDatum.append(EWFImgInfo.exif_datum(EWFImgInfo.open_file(fs_object)))

                            except Exception as ex:
                                if str(ex) != "object type must be bytes":
                                    myDatum.append("Onbekend")
                                else:
                                    pass

            tab = tt.Texttable()
            tab.set_cols_dtype(['a', 'a', 'a'])

            headings = ['Bestandsnaam', 'Datum en Tijd', 'NR.']
            tab.header(headings)
            names = myFilenames
            datum = myDatum
            nummer = myCijfer


            for row in zip(names, datum, nummer):
                tab.add_row(row)

            s = tab.draw()
            print (s)

            return None
