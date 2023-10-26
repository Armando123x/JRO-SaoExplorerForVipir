 
import os
import struct
import multiprocessing
from scipy import *
from scipy.interpolate import griddata
from scipy.interpolate import interp1d
import numpy
from matplotlib.pylab import *
import netCDF4 as nc
import pickle
import time
# paquetes para main
import glob
#---------------------------------------------------------
#---------------------------------------------------------
#---------------------------------------------------------
#----------- Direcciones de imagenes ---------------------


BUTON_ALL   = "buton_all.png"
MENU        = "file.png"
CARPETA     = 'files.png'
MAXIMIZAR   = 'minmaxclose.png'
DESKTOP     = 'desktop.png'
SELECT_MENU = 'select_menu.png'
HOME        = 'home.png'
IONOGRAMA   = 'Ionograma.png'
SAVE_SAO_RECORDS = 'save_sao.png'
GRM_FILE         = 'grm.png'
ATEMP   = 'atemp.png'
ERROR = 'error.png'
CLOSE = 'cerrar.png'
ESCRITORIO = 'escritorio.png'
DB_SNR  = 'set_frequency.png'
LAYERS = 'layers.png'
FREQ = 'freq.png'

SRC_FTP ='lisn.igp.gob.pe'
USER_FTP = 'acastro'
PWD_FTP ='UhmqBB0yLz4f5vLu1HvC'
# PATH_FTP = '/data1/ionosonde/JM91J/'
PATH_FTP = '/JM91J'
PATH_EXPLORER = r"C:\Users\soporte\Desktop\JRO-SaoExplorerForVipir-main\SAOExplorer_3.6"
PATH_DESKTOP = os.path.expanduser("~/Desktop")
PATH_SAO = os.path.join(PATH_DESKTOP,'SAOs')
SRC_TEMP = os.path.join(PATH_DESKTOP,'atemp')
TIME_SLEEP_BY_ADJUST = 8

DAYS = [31,28,31,30,31,30,31,31,30,31,30,31]

#Parameter para guardar el SAO:
# -------------------------------
# diariamente: daily
# mensualmente : monthly
# anualmente : annually
# --------------------------
# Es preferible guardarlo anualmente, para tener una cantidad
# menor de archivos.

# Por el momento, está deshabilitado la opción daily.

SAVE_SAO = 'daily'
TH_DB = 24

MIN_CONFIDENCE = 0.43


########################################################################
# timeout for ftp file download in seconds

ftp_timeout = 180 

#______________________________________________________________________
#______________________________________________________________________
#______________________________________________________________________
#______________________________________________________________________
#______________________________________________________________________
#______________________________________________________________________
#______________________________________________________________________
#______________________________________________________________________
#______________________________________________________________________


import multiprocessing
 
import multiprocessing.pool


# class NoDaemonProcess(multiprocessing.Process):
#     # make 'daemon' attribute always return False
#     def _get_daemon(self):
#         return False
#     def _set_daemon(self, value):
#         pass
#     daemon = property(_get_daemon, _set_daemon)

# # We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# # because the latter is only a wrapper function, not a proper class.
# class MyPool(multiprocessing.pool.Pool):
#     Process = NoDaemonProcess



class MyPool(multiprocessing.pool.Pool):
    def Process(self, *args, **kwds):
        proc = super(MyPool, self).Process(*args, **kwds)

        class NonDaemonProcess(proc.__class__):
            """Monkey-patch process to ensure it is never daemonized"""
            @property
            def daemon(self):
                return False

            @daemon.setter
            def daemon(self, val):
                pass

        proc.__class__ = NonDaemonProcess
        return proc
    
def es_bisiesto(año):
    if año % 4 == 0:
        if año % 100 == 0:
            if año % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False
    
    
def search_files_ngi(path):

    name = "*.ngi"

    src = os.path.join(path,name)

    list = glob.glob(src)


    return list

from multiprocessing import Pool

def ngi2grm(path1,path2=None):
 
    if path2 is None: path2=path1

    list = sort(search_files_ngi(path1))
  
    
    buff =[[x,path2] for x in list]
     
    pool = Pool(4,maxtasksperchild=500)
    
    result =pool.map(processto,buff)
    
    pool.close()
    pool.join()

    result = numpy.count_nonzero(~numpy.array(result))
    return result



def processto(array):
        file,path2 = array[0],array[1]
        namegrm = "{}.GRM".format(os.path.basename(file).split(".")[0])

        filegrm = os.path.join(path2,namegrm)
        try:

            ds = nc.Dataset(file)



            range1= ds['Range'][:]
            year = int(ds['year'][:])
            doy = int(ds['daynumber'][:])
            month = int(ds['month'][:])
            day = int(ds['day'][:])
            hour = int(ds['hour'][:])
            minu = int(ds['minute'][:])
            sec = int(ds['second'][:])
            fstart = int(ds['freq_start'][:]*10)
            fend = int(ds['freq_end'][:]*10)
            rangei = int(range1[0])
            powerO = ds['O-mode_power'][:]
            powerX = ds['X-mode_power'][:]
            

            frec = numpy.array(ds['Frequency'][:],dtype=numpy.int_)


            range2 = numpy.linspace(0, 255, num=256)*2.5+80
            
            powerOi=powerO[:,0:256].copy()
            powerXi=powerX[:,0:256].copy()


            for i in range(frec.shape[0]):

                powerOf=interp1d(range1, powerO[i], kind='cubic')
                powerXi[i] = powerOf(range2)

                powerXf=interp1d(range1, powerX[i], kind='cubic')
                powerOi[i] = powerXf(range2)
            
        


            year1 = int(str(year-2000),16)
            doy1= int(str(int(doy/100)),16)
            doy2= int(str(doy % 100),16)
            monthx = int(str(month),16)
            dayx = int(str(day),16)
            hourx = int(str(hour),16)
            minux = int(str(minu),16)
            secx = int(str(sec),16)
            fs1= int(fstart/10000)
            fs1x = int(str(int(fstart/10000)),16)
            fs2 = int((fstart-fs1*10000)/100)
            fs2x = int(str(int((fstart-fs1*10000)/100)),16)
            fs3 = int((fstart-fs1*10000)-fs2*100)
            fs3x = int(str(int((fstart-fs1*10000)-fs2*100)),16)
            fe1 = int(fend/10000)
            fe1x = int(str(int(fend/10000)),16)
            fe2 = int((fend-fe1*10000)/100)
            fe2x = int(str(int((fend-fe1*10000)/100)),16)
            fe3 = int((fend-fe1*10000)-fe2*100)
            fe3x = int(str(int((fend-fe1*10000)-fe2*100)),16)
            fint1=int('0',16)
            fint2=int(str(75),16)
            h37 = int(str(80),16)
            h40 = int(str(56),16)
            h53 = int(str(41),16)
            h56 = int(str(90),16)
            h58 = int(str(40),16)
            
            fd4 = int(frec.shape[0]/4)
            saltof = 0

            with open(filegrm, "wb") as grmf:
                ibloque=7

                for k in range(fd4):
                    if k>0: ibloque=6
                    grmf.seek(4096*k)
                    grmf.write(struct.pack('11B',ibloque,60,254,year1,doy1,doy2,monthx,dayx,hourx,minux,secx))
                    grmf.write(struct.pack('20B',48,49,50,48,49,50,6,1,fs1x,fs2x,fs3x,fint1,fint2,fe1x,fe2x,fe3x,0,0,1,1))
                    grmf.write(struct.pack('29B',7,3,1,0,0,h37,2,2,h40,0,0,8,2,0,4,0,0,0,14,0,0,h53,6,0,h56,6,h58,0,8))
                    
                    for j in range(4):
                        fi = int(frec[k*4+j*1+saltof]/10)
                        fi1 = int(fi/100)
                        fi1x = int(str(fi1),16)
                        fi2 = fi % 100
                        fi2x = int(str(fi2),16)
                    #print(fi, fi1, fi2,fi1x,fi2x)
                        ampmp=int(max(powerOi[k*4+j*1+saltof])/3)
                        ampmpx=int(str(ampmp),16)
                #print(ds['Has_Azimuth'])
                #prelude O
                        PolNh=51
                        OfsGa=56
                        grmf.write(struct.pack('6B',PolNh,fi1x,fi2x,OfsGa,secx,ampmpx))
                #      print(PolNh,fi1x,fi2x,OfsGa,secx,ampmpx)
                #group F-O
                        for i in range(249):
                            amp=int(powerOi[k*4+j*1+saltof,i]/3)
                            dop=3
                            ampdpo = amp*8+dop
                            fas = 10
                            az = 0
                            faazo = fas*8+az
                            try:
                                grmf.write(struct.pack('2B',ampdpo,faazo))
                            except:
                                print("Existe un problema con los datos NGI del archivo {}. No será guardado.".format(file))
                                grmf.close()
                                ds.close()  
                                try:
                                    os.remove(filegrm)
                                except:
                                    pass
                                try:
                                    os.remove(file)
                                except:
                                    pass
                                return False
                        #print(ampdpo,faazo)
                        ampmp=int(max(powerXi[k*4+j*1+saltof])/3)
                        ampmpx=int(str(ampmp),16)
                #print(ds['Has_Azimuth'])
                #prelude X
                        PolNh=35
                        OfsGa=56
                        grmf.write(struct.pack('6B',PolNh,fi1x,fi2x,OfsGa,secx,ampmpx))
                    #print(PolNh,fi1x,fi2x,OfsGa,secx,ampmpx)
                #group F-X
                        for i in range(249):
                            amp=int(powerXi[k*4+j*1+saltof,i]/3)
                            dop=3
                            ampdpo = amp*8+dop
                            fas = 10
                            az = 0
                            faazo = fas*8+az
                            grmf.write(struct.pack('2B',ampdpo,faazo))        
                grmf.close()
            ds.close()    
            try:
                os.remove(file)
                print("Se borró el archivo {}".format(file))
            except:
                print("No se pudo borrar el archivo {}".format(file))
            else:    
                return True
            
        except:
            print("Existe un problema con los datos NGI del archivo {}. No será guardado.".format(file))
            try:
                ds.close()
                
                os.remove(filegrm)
                os.remove(file)
            except:
                pass
            
            return False             
 
