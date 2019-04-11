import xml.etree.ElementTree as ET
from datetime import datetime
import os, glob

def rename(SAVED_DIR):
    ORIGINAL_PATH = '2019'
    os.chdir(ORIGINAL_PATH)
    files = glob.glob('*.xml')
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        Total = root.attrib['Total']
        Emisor = root[0].attrib['Rfc']
        Fecha1 = root.attrib['Fecha']
        Fecha2 = datetime.strptime(Fecha1,'%Y-%m-%dT%H:%M:%S')
        Fecha = datetime.strftime(Fecha2,'%Y_%m_%d')
        Mes = datetime.strftime(Fecha2,'%b')
        Nombre='{} {} {}'.format(Emisor,Fecha,Total)
        try:
            os.makedirs(Mes)
            print ('Carpeta para facturas de '+Mes+' creada')
        except:
            print ('Moviendo a carpeta de '+Mes)
        file = file.replace('.xml','')
        MONTH_DIR=os.path.join(SAVED_DIR,Mes,Nombre)
        try:
            os.rename(file+'.xml',MONTH_DIR+'.xml')
        except:
            print('Factura '+file+' repetida')
        try:
            os.rename(file+'.pdf',MONTH_DIR+'.pdf')
        except:
            print ('Archivo '+file+'.pdf no encontrado')
            continue
        print('Archivo renombrado: '+Nombre)

    os.chdir('..')
