import exifread, re


def gps_data(path_to_file):
    gps_coord = []
    with open(path_to_file, 'rb') as f:
        file_exifdata = exifread.process_file(f)
        if 'GPS GPSLatitude' and 'GPS GPSLongitude' in file_exifdata.keys():
            file_lati = str(file_exifdata['GPS GPSLatitude'])
            file_long = str(file_exifdata['GPS GPSLongitude'])
            posi_lati = re.search('/', file_lati)
            posi_long = re.search('/', file_long)
            file_lati2 = list((float(file_lati[1:3]),
                               float(file_lati[5:7]),
                               (float(file_lati[9:(posi_lati.start() - 1)]) / float(file_lati[(posi_lati.start() + 1):-1]))))
            file_long2 = list((float(file_long[1:3]),
                               float(file_long[5:7]),
                              (float(file_long[9:(posi_long.start() - 1)]) / float(file_long[(posi_long.start() + 1):-1]))))
            file_lati = (float(file_lati2[0]) + (float(file_lati2[1]) / 60) + (float(file_lati2[2]) / (60 * 60)))
            file_long = (float(file_long2[0]) + (float(file_long2[1]) / 60) + (float(file_long2[2]) / (60 * 60)))
            gps_coord = (file_lati, file_long)
            return gps_coord
