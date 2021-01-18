import os, shutil, re, exifread, argparse, click, myfunctions, sys

argParse = argparse.ArgumentParser(description='Photosorting program', )
argParse.add_argument('input_dir', type=str, help='Input directory')
argParse.add_argument('output_dir', type=str, help='Output directory')
argParse.add_argument('-x', '--deletesource', action='store_true', help='Delete source files')
argParse.add_argument('-m', '--generatemap', action='store_true', help='Generate Map Locations')
arguments = argParse.parse_args()

input_dir = arguments.input_dir
output_dir = arguments.output_dir
delete_source = arguments.deletesource
generate_map = arguments.generatemap
map_dict = dict()
placeholder = ''
Backslash = '\ '
if not input_dir.endswith(Backslash[0:1]):
    input_dir = input_dir+Backslash[0:1]
if not output_dir.endswith(Backslash[0:1]):
    output_dir = output_dir+Backslash[0:1]
date_list = set(())
i = 0
if delete_source:
    delete_source = click.confirm('Do you really want to destroy the original pictures?', default=True)
for file in os.listdir(input_dir):
    if file.lower().endswith('.jpeg') or file.lower().endswith('.jpg'):
        with open(input_dir+file, 'rb') as f:
            file_exifdata = exifread.process_file(f)
            exifdata_keys = file_exifdata.keys()
            if 'EXIF DateTimeOriginal' in exifdata_keys:
                file_date = file_exifdata['EXIF DateTimeOriginal']
                file_year = str(file_date)[0:4]
                file_name_beforesort = str(file_date).replace(':', '-')
                date_list.add(file_name_beforesort[0:10])
                if not os.path.isdir(output_dir + file_year):
                    os.makedirs(output_dir + file_year)
                shutil.copyfile(input_dir+file, output_dir + file_year + '\\' + file_name_beforesort + '.jpg', follow_symlinks=True)
            else:
                i += 1
                if not os.path.isdir(output_dir + 'Unknown_date\\'):
                    os.mkdir(output_dir + 'Unknown_date\\')
                try:
                    shutil.copyfile(input_dir+file, output_dir + 'Unknown_date\\' + str(i).zfill(3) + '.jpg')
                except:
                    print('file' + file + 'already exists')
            f.close()
            if delete_source:
                os.remove(input_dir+file)
if delete_source:
    os.removedirs(input_dir)
for item in date_list:
    i = 1
    for file in os.listdir(output_dir+item[0:4]+'\\'):
        if re.match(item, file):
            os.rename(output_dir+item[0:4]+'\\'+file, output_dir+item[0:4]+'\\'+file[0:10]+'-'+str(i).zfill(3)+'.jpg')
            if generate_map:
                Long_Lati = myfunctions.gps_data(output_dir+item[0:4]+'\\'+file[0:10]+'-'+str(i).zfill(3)+'.jpg')
                if Long_Lati:
                    map_dict.update({output_dir+item[0:4]+'\\'+file[0:10]+'-'+str(i).zfill(3)+'.jpg': Long_Lati})
            i += 1
for key in map_dict:
    lati=str(map_dict[key][0])
    long=str(map_dict[key][1])
    placeholder += 'L.marker(['+lati+ ', '+long+''']).addTo(map).bindPopup('<img src="'''+str(key)+'''" class="popup-img">',{minWidth:100}).openPopup();'''
with open(sys.path[0]+'\\'+"map_template.html", "r") as template:
    with open(output_dir+'\\'+"image_map.html", "w") as generated_html:
        generated_html.write(template.read().replace('PLACEHOLDER;', placeholder))
