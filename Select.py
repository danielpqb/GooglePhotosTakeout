'''
This script searches all .JPG files with GPS location inside a directory and moves the files to another directory.
'''

from GPSPhoto import gpsphoto
import os
import shutil

def lffiles(path, f_type=None):
    global files
    global unknwfiles
    global delfiles
    global delfolders
    global ignore_coord
    global unzip

    with os.scandir(path) as folder:
        for file in folder:
            if file.is_dir():  # If the file isn't a folder
                if not os.listdir(file.path): #If it is an empty directory
                    os.rmdir(file.path)
                    delfolders += 1
                    continue
                else:
                    folders.append(file.path)
                    continue

            if file.name.endswith('.json'):
                try:
                    os.remove(file.path)
                    delfiles += 1
                    continue
                except:
                    continue

            if '-editada' in file.name:
                try:
                    os.remove(path + '\\' + file.name.replace('-editada', ''))
                except:
                    pass

            if unzip == True:
                try:
                    shutil.move(file.path, except_path + '#Adicionar' + '\\' + file.name)
                    files += 1
                    continue
                except:
                    continue

            if file.name.endswith(f_type):
                if ignore_coord == True:
                    try:
                        shutil.move(file.path, final_path + '\\' + file.name)
                        files += 1
                        continue
                    except:
                        continue
                else:
                    photo_coords = askcoord(file.path)
                    if photo_coords == None:
                        try:
                            shutil.move(file.path, except_path + '#UnknownLocation' + '\\' + file.name)
                            unknwfiles += 1
                            continue
                        except:
                            continue
                    elif lat_min < photo_coords[0] < lat_max and long_min < photo_coords[1] < long_max:
                        try:
                            shutil.move(file.path, final_path + '\\' + file.name)
                            files += 1
                            continue
                        except:
                            continue
        folders.pop(0)


def askcoord(filepath):
    try:
        data = gpsphoto.getGPSData(filepath)
        return [data['Latitude'], data['Longitude']]
    except:
        return None

#file_types = ['.jpg', '.JPG', '.jpeg', '.png', '.PNG', '.tif', '.TIF', '.mp4', '.MP4', '.mov', '.MOV', '.3gp', '.3GP']
file_types = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.tif', '.TIF', '.gif', '.GIF']
#file_types = ['.mp4', '.MP4', '.mov', '.MOV', '.3gp', '.3GP']

unzip = True
initial_path = r'D:\Users\Daniel\BACKUPs\Fotos\Separando\04\Takeout\Google Fotos'
final_path = r'D:\Users\Daniel\BACKUPs\Fotos\Separando\04\Takeout\Google Fotos'
except_path = r'D:\Users\Daniel\BACKUPs\Fotos\Separando\\'
ignore_coord = True
lat = -22.805
long = -43.2
dist = 54500

# lat_min = -23.349545
# lat_max = -22.260923
# long_min = -44.716189
# long_max = -41.690416

dist /= 100000
lat_min = lat - dist
lat_max = lat + dist
long_min = long - dist
long_max = long + dist

unknwfiles = 0  # Count number of files moved to #UnknownLocation folder
delfiles = 0  # Count number of .json files that were removed
delfolders = 0  # Count number of folders that were removed
files = 0  # Count number of files moved
folders = [initial_path]

print('----------- Files Moved -----------')

if unzip != True:
    for f_type in file_types:
        folders = [initial_path]
        files = 0

        while folders != []:
            lffiles(folders[0], f_type)

        print(f'\'{f_type}\': {files}')
else:
    while folders != []:
        lffiles(folders[0])
    print(f'Files moved to #Adicionar: {files}')

print(f'-----------------------------------\nFiles moved to #UnknownLocation: {unknwfiles}')
print(f'\'.json\' files deleted: {delfiles}')
print(f'Folders deleted: {delfolders}')
