# from variables import *
import os
import traceback 
import numpy
from variables import * 
from datetime import datetime, timezone 
import paramiko
from scp import SCPClient

from dateutil.relativedelta import relativedelta
from ftplib import FTP


def gen_latest():

    if os.path.isdir(PATH_SERVER):
        #Directorio existe
        listdir = sorted(os.listdir(PATH_SERVER))
        try:
            listdir.remove("latest.csv")
            listdir.remove("7days.csv")
        except:
            pass
        latest_names = listdir[-7:]

        tmp_dt = []
        tmp_h = []
        tmp_f = []

        for name in latest_names :
            if  'txt' in name and 'latest.csv' != name and '7days.csv' != name:
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
                        except Exception as e:
                            print(e,date)
                        

        tmp_dt = numpy.array(tmp_dt,dtype=object)
        tmp_h  = numpy.array(tmp_h,dtype=float)
        tmp_f  = numpy.array(tmp_f,dtype=float)

        dates = numpy.array(tmp_dt,dtype=object)

        #Obtenemos la hora utc
        now_utc = datetime.now() 

        min_utc = datetime(now_utc.year,now_utc.month,now_utc.day) + relativedelta(days=-1)
        min_utc_7d = datetime(now_utc.year,now_utc.month,now_utc.day) + relativedelta(days=-7)
        #dates = numpy.sort(dates[dates>=min_utc])
        mask = dates>=min_utc
        mask_7d = dates>=min_utc_7d

 
        tmp_dt_,tmp_h_,tmp_f_ = tmp_dt[mask],tmp_h[mask],tmp_f[mask]
        tmp_dt_7d,tmp_h_7d,tmp_f_7d = tmp_dt[mask_7d],tmp_h[mask_7d],tmp_f[mask_7d]
        
        fout = os.path.join(PATH_SERVER,'latest.csv')
        fout_7d = os.path.join(PATH_SERVER,'7days.csv')
        
        with open(fout,'w') as f:

            f.write("datetime,height,frequency\n")
            
        with open(fout_7d,'w') as fa:

            fa.write("datetime,height,frequency\n")
            
        for dt,h,f in zip(tmp_dt_,tmp_h_,tmp_f_):
       
            with open(fout,'a') as file:
                file.write(f"{dt.strftime('%Y-%m-%d %H:%M:%S')},{h},{f}\n")
        for dt,h,f in zip(tmp_dt_7d,tmp_h_7d,tmp_f_7d):
       
            with open(fout_7d,'a') as filea:
                filea.write(f"{dt.strftime('%Y-%m-%d %H:%M:%S')},{h},{f}\n")
            

# Crear una función para crear un cliente SCP
def create_scp_client(host, port, username, password):
    # Crear un cliente SSH
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(host, port, username=username, key_filename=key_file)
    ssh.connect(host, port, username, password)

    # Crear un cliente SCP
    scp = SCPClient(ssh.get_transport())
    return scp


def send_ftp_sao():

    SRC_FTP ='lisn.igp.gob.pe'
    USER_FTP = 'cesar'
    PWD_FTP ='cev2001gobpe'
    DIR_RMT = '/home/cesar/isr/datasao'

    try:
        files = os.listdir(PATH_SAO)

        files = sorted(files)

        ftp = FTP(SRC_FTP)
        ftp.login(user=USER_FTP, passwd=PWD_FTP)

        ftp.cwd(DIR_RMT)


        for file in files:

            if '.SAO' in file:
                try:
                    pfile = os.path.join(PATH_SAO,file)
                    with open(pfile, "rb") as p:
                        ftp.storbinary(f"STOR {file}", p)
                except:
                    print(f"Hubo un error al subir el archivo por FTP. {traceback.format_exc()}")

                else:
                    print(f"Archivo {file} subido por FTP a la ruta {DIR_RMT}.")

                    try:
                        os.remove(pfile)
                    except:
                        pass

        ftp.quit()
    except:
        print(f"Hubo un error en el servicio ftp. {traceback.format_exc()}")

def send_ftp():

    SRC_FTP ='lisn.igp.gob.pe'
    USER_FTP = 'cesar'
    PWD_FTP ='cev2001gobpe'
    DIR_RMT = '/home/cesar/isr/datadensity'

    try:
        files = os.listdir(PATH_SERVER)

        files.remove('7days.csv')
        files.remove('latest.csv')
        files = sorted(files)




        files = files[:]

        ftp = FTP(SRC_FTP)
        ftp.login(user=USER_FTP, passwd=PWD_FTP)

        ftp.cwd(DIR_RMT)


        for file in files:
            try:
                pfile = os.path.join(PATH_SERVER,file)
                with open(pfile, "rb") as p:
                    ftp.storbinary(f"STOR {file}", p)
            except:
                print(f"Hubo un error al subir el archivo por FTP. {traceback.format_exc()}")

            else:
                print(f"Archivo {file} subido por FTP a la ruta {DIR_RMT}.")

        ftp.quit()
    except:
        print(f"Hubo un error en el servicio ftp. {traceback.format_exc()}")


def send_scp():
 
    host = '10.10.110.213'          # Dirección IP del host remoto
    port = 8122                      # Puerto SSH (por defecto es 22)
    username = 'idi-user'           # Nombre de usuario en el host remoto
    key_file = r'C:/Users/escalado_user/.ssh/id_rsa.pub'  # Ruta de tu clave privada
    password='QyQdi4WmjBoMDUZTbJP4Z27Ex'
 
    local_file = os.path.join(PATH_SERVER,'latest.csv')
    local_file_7d = os.path.join(PATH_SERVER,'7days.csv')
    
    remote_path = '/data/latest.csv'
    remote_path_7d = '/data/7days.csv'
    
    try:
        # Crear el cliente SCP y enviar el archivo
        scp = create_scp_client(host, port, username, password)
        scp.put(local_file, remote_path)
        scp.put(local_file_7d, remote_path_7d)
        scp.close()
    
    except Exception as e:
        print(f"Error al enviar por scp. {e}")


 
