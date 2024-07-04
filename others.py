# from variables import *
import os
from datetime import datetime, timezone
import numpy
from variables import * 

import paramiko
from scp import SCPClient

from dateutil.relativedelta import relativedelta
 


def __gen_latest():

    if os.path.isdir(PATH_SERVER):
        #Directorio existe
        listdir = sorted(os.listdir(PATH_SERVER))

        latest_names = listdir[-3:]

        tmp_dt = []
        tmp_h = []
        tmp_f = []

        for name in latest_names :
            if  'txt' in name and 'latest.txt' != name:
                fpath = os.path.join(PATH_SERVER,name)
                with open(fpath,'r') as f:

                    buffer = numpy.array(f.read().splitlines(),dtype=object)[0:]

                    for line in buffer:
                
                       
                        date,h,f= line.split(',')
                        try:
                            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

                            tmp_dt.append(date)
                            tmp_h.append(float(h))
                            tmp_f.append(float(f))
                        except:
                            print(date)
                        

        tmp_dt = numpy.array(tmp_dt,dtype=object)
        tmp_h  = numpy.array(tmp_h,dtype=float)
        tmp_f  = numpy.array(tmp_f,dtype=float)

        dates = numpy.array(tmp_dt,dtype=object)

        #Obtenemos la hora utc
        now_utc = datetime.now(timezone.utc) 

        min_utc = datetime(now_utc.year,now_utc.month,now_utc.day) + relativedelta(days=-1)

        #dates = numpy.sort(dates[dates>=min_utc])
        mask = dates>=min_utc
        tmp_dt,tmp_h,tmp_f = tmp_dt[mask],tmp_h[mask],tmp_f[mask]

        fout = os.path.join(PATH_SERVER,'latest.txt')

        with open(fout,'w') as f:

            f.write("datetime,height,frequency\n")

        for dt,h,f in zip(tmp_dt,tmp_h,tmp_f):
       
            with open(fout,'a') as file:
                file.write(f"{dt.strftime('%Y-%m-%d %H:%M:%S')},{h},{f}\n")

            

# Crear una función para crear un cliente SCP
def create_scp_client(host, port, username, key_file):
    # Crear un cliente SSH
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username=username, key_filename=key_file)

    # Crear un cliente SCP
    scp = SCPClient(ssh.get_transport())
    return scp


def send_scp():
 
    host = '10.10.110.213'          # Dirección IP del host remoto
    port = 8122                      # Puerto SSH (por defecto es 22)
    username = 'idi-user'           # Nombre de usuario en el host remoto
    key_file = r'C:/Users/TuUsuario/.ssh/id_rsa'  # Ruta de tu clave privada
 
    local_file = os.path.join(PATH_SERVER,'latest.txt')
    remote_path = '/data/latest.txt'

    try:
        # Crear el cliente SCP y enviar el archivo
        scp = create_scp_client(host, port, username, key_file)
        scp.put(local_file, remote_path)
        scp.close()
    
    except:
        pass


 