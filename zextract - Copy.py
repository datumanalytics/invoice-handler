import os, glob
import zipfile

def zextract():
    ORIGINAL_PATH = '2019'
    os.chdir(ORIGINAL_PATH)
    files = glob.glob('*.zip')
    for file in files:
        zip = zipfile.ZipFile(file)
        zip.extractall()
        zip.close()
        os.remove(file)
    os.chdir('..')
