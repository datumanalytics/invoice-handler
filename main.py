#SMPT
import imaplib
import email
import os
import json
import rename
import zipfile
import zextract

# Cargar datos de archivo json
with open('info.json') as f:
    data = json.load(f)

def disconnect(imap):
    imap.logout()

# Directorio donde se encuentran las facturas guardadas
ORIGINAL_PATH = '2019'
MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
SAVED_DIR = os.path.join(MAIN_DIR, ORIGINAL_PATH)

#Conectar al correo
server=imaplib.IMAP4(data['server'])
server.login(data['user'],data['pass'])
server.select('inbox', readonly = False)

#numero de correos
typ, msgs = server.search(None, 'ALL')
msgs = msgs[0].split()

#obtener contenido de cada correo
for emailid in msgs:
    resp, data = server.fetch(emailid, 'RFC822')
    email_body = data[0][1]
    mail = email.message_from_string(email_body)
    if mail.get_content_maintype() != 'multipart':
        continue
    #tiene adjunto?
    for part in mail.walk():
        if not mail.is_multipart():
            continue
        if mail.get('Content-Disposition'):
            continue
        file_name = part.get_filename()
        # guardar adjunto en directorio deseado
        if file_name:
            #sv_path = os.path.join(SAVED_DIR, file_name)
            sv_path = os.path.join(SAVED_DIR, file_name)
            file = open(sv_path,'wb')
            file.write(part.get_payload(decode=True))
            file.close()
            print ('downloaded '+file_name)

# Revisar archivos ya leidos
server.select('INBOX')
typ, [response] = server.search(None, 'SEEN')
if typ != 'OK':
    raise RuntimeError(response)

# Copiar los mensajes a 2019 y validar
typ, create_response = server.create('2019')
msg_ids = ','.join(response.split(' '))
if not msg_ids:
    print ('No hay facturas nuevas')
else:
    server.copy(msg_ids, '2019')
    server.select('2019')
    typ, [response] = server.search(None, 'ALL')
    print 'COPIED:', msg_ids, ' to folder 2019'

    # Correos a eliminar de Inbox?
    server.select('INBOX', readonly = False)
    typ, [msg_ids] = server.search(None, 'ALL')
    msg_ids = ','.join(msg_ids.split(' '))
    typ, response = server.store(msg_ids, '+FLAGS', r'(\Deleted)')
    typ, response = server.expunge()
    print 'Correos eliminados de Inbox:', response

zextract.zextract()
rename.rename(SAVED_DIR)
# TODO: extraccion de *.zip
# TODO: separar carpetas por mes en correo y hd
