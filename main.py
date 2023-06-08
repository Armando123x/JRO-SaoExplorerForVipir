import pyautogui
import os
import subprocess
from variables import *
import platform
import ftplib, tarfile, os
from ftplib import FTP
import pandas as pd 
from multiprocessing import Pool
from datetime import datetime
import numpy
from pywinauto import Desktop, Application
import pygetwindow as gw
import glob
import gc

import win32api
import win32gui
import win32con

import distutils.file_util

import shutil 


pyautogui.FAILSAFE = False
 

### ---------------------------- Iniciamos el programa ------------------------

 

 

def exec_command(command=None):

        obj = Pool(2,maxtasksperchild=1000)

        obj.apply_async(os.system,(command))

        return obj



class saoVipi(object):
    
    FlagInitConfig= False
    
    
    def __init__(self,**kwargs):
        
        ##obtener_sao_explorer
        #sistema
         
        self.verbose = kwargs.get("verbose",False)
        self.ini_date = kwargs.get('ini_date',None)
        self.fin_date = kwargs.get('fin_date',None)
        
        self.path_explorer = kwargs.get("path_explorer",PATH_EXPLORER)
        
        
        self.ini_date = datetime.strptime(self.ini_date, "%Y/%m/%d")
        self.fin_date = datetime.strptime(self.fin_date, "%Y/%m/%d")
        
        self.__init_config()
        
        self.__config_download()
         

    
        
    def __config_download(self,):
        
        #/data1/ionosonde/JM91J/2009/08/*
        
        year0   = int(self.ini_date.year)
        month0  = int(self.ini_date.month)
        day0    = int(self.ini_date.day)
        
        year1  = int(self.fin_date.year)
        month1 = int(self.fin_date.month)
        day1   = int(self.fin_date.day)
        
        paths = list()
        
        temp = list()
        
        dfyear = year1-year0
        print("dfyeat",dfyear)
        if dfyear<0:
            ValueError("Verifique el rango de fechas ingresadas.")
        
        
        elif dfyear==0:
            if month0==month1:
                days = DAYS[month0-1]
                if month0 == 2 and es_bisiesto(year0): days=29
                for day in range(day0,day1+1):
                    buff='{}/{:04d}/{:02d}/{:02d}/ngi'.format(PATH_FTP,year0,month0,day)
                    paths.append(buff)
                    
                    if SAVE_SAO =='daily':temp.append(paths);paths=list();
                    
                    if self.verbose:
                        print("Agregando la direccion {} a la sección de descarga.".format(buff))
                        
                temp.append(paths);paths=list();
                
            elif  month0>month1:
                ValueError("Verifique el rango de fechas ingresadas.")
            else: 
                for m in range(month0,month1+1):
                    days = DAYS[m-1]
                    if m == 2 and es_bisiesto(year0): days=29
                    
                    for day in range(1,days+1):
                        
                        buff= '{}/{:04d}/{:02d}/{:02d}/ngi'.format(PATH_FTP,year0,m,day)
                        paths.append(buff)
                        
                        if SAVE_SAO =='daily':
                            temp.append(paths)
                            paths=list()
                        
                        if self.verbose:
                            print("Agregando la direccion {} a la sección de descarga.".format(buff))
                        
                    if SAVE_SAO =='monthly':
                        temp.append(paths)
                        paths   =list()
                    
                if SAVE_SAO =='annually':
                    temp.append(paths)
                    paths=list()
                    
        
        elif dfyear==1:
             
            for m in range(month0,13):
                days = DAYS[m-1]
                if m == 2 and es_bisiesto(year0): days=29
                
                for day in range(1,days+1):
                    buff='{}/{:04d}/{:02d}/{:02d}/ngi'.format(PATH_FTP,year0,m,day)
                    paths.append(buff)
                    if SAVE_SAO =='daily':
                        temp.append(paths)
                        paths=list()
                    
                    if self.verbose:
                        print("Agregando la direccion {} a la sección de descarga.".format(buff))
                        
                
                if SAVE_SAO =='monthly':
                    temp.append(paths)
                    paths=list()
                    
            if SAVE_SAO =='annually':
                temp.append(paths)
                paths=list()
                    
            for m in range(1,month1+1):
                days = DAYS[m-1]
                if m == 2 and es_bisiesto(year1): days=29
                
                for day in range(1,days+1):
                    buff='{}/{:04d}/{:02d}/{:02d}/ngi'.format(PATH_FTP,year1,m,day)
                    paths.append(buff)
                    if SAVE_SAO =='daily':
                        temp.append(paths)
                        paths=list()
                        
                    
                    if self.verbose:
                        print("Agregando la direccion {} a la sección de descarga.".format(buff))
                        
                if SAVE_SAO =='monthly':
                    temp.append(paths)
                    paths=list()
                
            if SAVE_SAO =='annually':
                temp.append(paths)
                paths=list()
                
        else:
          
            for m in range(month0,13):
                days = DAYS[m-1]
                if m == 2 and es_bisiesto(year0): days=29
                
                for day in range(1,days+1):
                    buff='{}/{:04d}/{:02d}/{:02d}/ngi'.format(PATH_FTP,year0,m,day)
                    paths.append(buff)
                    if SAVE_SAO =='daily':
                        temp.append(paths)
                        paths=list()
                        
                    
                    if self.verbose:
                        print("Agregando la direccion {} a la sección de descarga.".format(buff))
            
                if SAVE_SAO =='monthly':
                    temp.append(paths)
                    paths=list()
            
            if SAVE_SAO =='annually':
                temp.append(paths)
                paths=list();
            
     
                
            for year in range(year0+1,year1):
                for m in range(1,13):
                    days = DAYS[m-1]
                    if m == 2 and es_bisiesto(year): days=29
                
                    for day in range(1,days+1):
                        buff ='{}/{:04d}/{:02d}/{:02d}/ngi'.format(PATH_FTP,year,m,day)
                        paths.append(buff)
                        if SAVE_SAO =='daily':
                            temp.append(paths)
                            paths=list()
                        
                        if self.verbose:
                            print("Agregando la direccion {} a la sección de descarga.".format(buff))
                    
                    if SAVE_SAO =='monthly':
                        temp.append(paths)
                        paths=list()
                
                if SAVE_SAO =='annually':
                    temp.append(paths)
                    paths=list()
                    
  
                    
            for m in range(1,month1+1):
                days = DAYS[m-1]
                if m == 2 and es_bisiesto(year1): days=29
                
                for day in range(1,days+1):
                    buff = '{}/{:04d}/{:02d}/{:02d}/ngi'.format(PATH_FTP,year1,m,day)
                    paths.append(buff)
                    if SAVE_SAO =='daily':
                        temp.append(paths)
                        paths=list()
                    
                    if self.verbose:
                        print("Agregando la direccion {} a la sección de descarga.".format(buff))
                    
                
                if SAVE_SAO =='monthly':
                    temp.append(paths)
                    paths=list()
            
            if SAVE_SAO =='annually':
                temp.append(paths)
                paths=list()
                
        
        # temp = numpy.array(temp,dtype='object')
            
        #---------------------------------------------------------------------------
        # Ahora que ya tenemos un self.paths con los meses y dias a descargar.
        # Buscamos en el servidor si existen tales carpetas y listamos los archivos 
        # disponibles del servidor en un nuevo path
        # --------------------------------------------------------------------------
        
        self.__verify_and_download(temp)
        
        self.save_database()
        
        
    def save_database(self):
        
        file = os.path.join(".temp","db.pkl")
        self.database.to_pickle(file)            
                
        
    def __verify_and_download(self, paths):
        
        #------------------------------------------------------------------------------
        # En el servidor, los archivos están en la siguiente estructura:
        # /path/to/file/year/month/day/
        
        
        filestodownload = numpy.array(self.database['name_ngi'],dtype='object')
        
        files_saved = list()
        
        for temp in paths:
            #Temp agrupa la frecuencia con que está guardado los archivos:
            # Diaro
            # Mensual
            # Anual 
            # count para contar cuantos elementos se descargó
            
            count = 0
            for path in temp:
                
                if self.verbose:
                    print("Se conecta al servidor {}".format(SRC_FTP))
                    
                ftp = self.__ftp_connection()
                ftp.sock.settimeout(ftp_timeout)
                
                
                try:
                    # Nos movemos al directorio ftp para listar los archivos disponibles
                    # para descarga
                    ftp.cwd(path)
                    files = ftp.nlst()
                    

                                     
                except:
                   # No existe tal directorio
                   if self.verbose:
                       print("El directorio {:04d}/{:02d}/{:02d}/{} no existe en el servidor FTP".format(int(path.split('/')[-4]),
                                                                                                        int(path.split('/')[-3]),
                                                                                                        int(path.split('/')[-2]),
                                                                                                        path.split('/')[-1]))
                else:
                    
                    if len(files)>0:
                         
                        files = numpy.array(files)
                        
                        for file in files:
                            
                            if file in filestodownload:
                                #archivo descargado
                                pass
                            else:
                                #archivo por descargar
                                pout = os.path.join(SRC_TEMP,file)
                                
                                if self.__ftp_download(ftp,file,pout) == True:
                                    #archivo descargado
                                   
                                    files_saved.append(file)
                                    
                                    
                                    count+=1
                                    
                                    name_grm = '{}.GRM'.format(file.split('.')[0])
                                    path_download = os.path.join(path,file)
                                    
                                    buff = [file,float('nan'),name_grm,path_download,float('nan')]
                                    
                                    self.__add_database(buff)
                        
                        
                     
                        try:
                            ftp.quit()
                            if self.verbose:
                                print("Nos desconectamos del servidor {}.".format(SRC_FTP))
                        except:
                            RuntimeWarning("Existió problema al desconectarse del servidor FTP.")


                    else:
                        try:
                            ftp.quit()
                            if self.verbose:
                                print("Nos desconectamos del servidor {}.".format(SRC_FTP))
                        except:
                            RuntimeWarning("Existió problema al desconectarse del servidor FTP.")

            
            # Ahora convertimos a .GRM 
            # Todo el temporal
            if count>0:
                if self.verbose:
                    print("Se descargó un total de archivos {} NGI. Ahora se procede a \
                          convertir en el formato GRM.".format(count))
                
                bools = ngi2grm(SRC_TEMP)   
                
                # #actualizamos la lista 
                # lista = numpy.array(lista,dtype='object')[bools] 
                
                # lista = lista.tolist()
                
                count = count - bools
                
                if bools>0:
                    if self.verbose:
                        print("Existieron {} archivos .ngi con problema en la estructura de datos.".format(bools))
                
                if count >0:
                # Ahora ejecutamos en obtener el archivo .SAO 
                    gc.collect()
                    if self.verbose:
                        print("Empezamos con la manipulación del SaoExplorer.....")
                    if self.__release_SAOExplorer(count):
                        src_sao = os.path.join(PATH_DESKTOP,'*.SAO')
                        lista = glob.glob(src_sao)
                        
                        if len(lista)==1:
                            
                            if not os.path.isdir(PATH_SAO):
                                os.mkdir(PATH_SAO)
                                
                            for file in lista:
                                file = os.path.basename(file)
                                # Construir la ruta de destino
                                ruta_file = os.path.join(PATH_DESKTOP, file)
                                ruta_destino = os.path.join(PATH_SAO, file)

                                #Mover el archivo a la carpeta de destino
                                shutil.copy(os.path.join(PATH_DESKTOP, file),
                                            os.path.join(PATH_SAO, file))
                            
                                os.remove(ruta_file)
                                
                                if self.verbose:
                                    print("Se salvó el archivo SAO {} .".format(file))
                                    
                                # Actualizamos la base de datos
                                self.database.loc[self.database['name_ngi'].isin(files_saved), 'path_sao'] = ruta_destino
                                self.database.loc[self.database['name_ngi'].isin(files_saved), 'name_sao'] = file 

                                gc.collect()
                                files_saved = list()
                                self.save_database()

                        elif len(lista)>0:
                            raise RuntimeError("Existe diversos archivos SAO en la ruta {}, por lo que es dificil elegir.".format(PATH_DESKTOP))
                        
                        else:
                            raise RuntimeError("Los archivos SAO no se están \
                                guardando en la ruta '{}'".format(PATH_DESKTOP))
                        
                        # Eliminamos la carpeta temporal.
                        try:
                            shutil.rmtree(SRC_TEMP)
                        except:
                            print("No se pudo borrar la carpeta temporal de VIPIR.")

                else:
                    if self.verbose:
                        print("No existe archivos .GRM validos en el directorio.")
            else:
                if self.verbose:
                    print("No se descargó algún archivo. Se seguirá explorando otros directorios. ")
                     

                       
           
    def __click(self,posicion_boton,number= 1):
        
            x, y = pyautogui.center(posicion_boton)
            # Realiza el clic en el centro del botón
            pyautogui.click(x, y,clicks=number)        
            pyautogui.sleep(0.3)
    
 
            
    def __release_SAOExplorer(self,n_adjust=10):
    
        #########################################################
        # Lanzamos el explorador
        pool = self.__config_SAOExplorer()
        #########################################################
        
        pyautogui.sleep(10)
        
        posicion_boton = None
        confidence=.86
        while posicion_boton is None:
            posicion_boton = pyautogui.locateOnScreen(BUTON_ALL, confidence=confidence)
            confidence-=.05
            if confidence<0.4: LookupError("No se encontró el botón de abrir carpeta para seleccionar \
                                                        todos los archivos en SaoExplorer.")
            pyautogui.sleep(0.5)
        if self.verbose:
            print("Se hizo click en el boton para seleccionar ficheros.")    
        self.__click(posicion_boton)
        
        pyautogui.sleep(1.5)
        #########################################################
        # Confirmar si es desktop 


        #se está en otro directorio, dirigirnos a desktop
        posicion_boton = None
        confidence=.87
        while posicion_boton is None:
            posicion_boton = pyautogui.locateOnScreen(HOME, confidence=confidence)
            confidence-=.05
            if confidence<0.4: LookupError("No se encontró el botón de HOME en el SaoExplorer.")            
            pyautogui.sleep(0.5)
        
        if self.verbose:
            print("Se seleccionó el boton Home")
        self.__click(posicion_boton)
     
        pyautogui.sleep(0.9)
            
            
        #########################################################
        # Ya estamos en desktop, ahora seleccionamos la carpeta
        posicion_boton = None
        confidence=.9
        while posicion_boton is None:
            posicion_boton = pyautogui.locateOnScreen(ATEMP, confidence=confidence)
            confidence-=.05
            if confidence<0.4: LookupError("No se encontró el directorio atemp en el SaoExplorer.")  
            pyautogui.sleep(0.2)
        if self.verbose:
            print("Se seleccionó el boton Temp")      
                  
        self.__click(posicion_boton)
        #presionamos enter para entrar al directorio
        pyautogui.typewrite('\n')
        pyautogui.sleep(0.7)    
        # 
        #Seleccionamos un archivo .GRM 
        
        posicion_boton = None
        confidence=.8
        
        while posicion_boton is None:
            posicion_boton = pyautogui.locateOnScreen(GRM_FILE, confidence=confidence)
            confidence-=.05
            if confidence<0.4: LookupError("No se encontró algun archivo .GRM en el SaoExplorer.")  
        self.__click(posicion_boton)
        #presionamos enter para entrar al directorio
        pyautogui.typewrite('\n')
        #Esperamos a que cargue todos los archivos
        pyautogui.sleep(5)                                 
               
        #########################################################
        # Logramos abrir las carpetas 
        # Ahora se procede a buscar el boton ionograma 
     
        
       
        
        posicion_boton = None     
        confidence = .8
        if self.verbose:
            print("Buscando boton de Ionograma")
            
        while posicion_boton is None:
            posicion_boton = pyautogui.locateOnScreen(IONOGRAMA, confidence=confidence)
            confidence-=.05
            if confidence<0.4: LookupError("No se encontró el botón de Ionograma en el SaoExplorer.")                 
            pyautogui.sleep(0.12)
            
        if self.verbose:
            print("Se seleccionó el boton de Ionograma")
        self.__click(posicion_boton)
        ############################################################
        # Creamos una funcion pequeña para la detección de mensajes
 
 
        def detect_warning():
 
            while 1:
                bordes = None
                confidence= 0.5
                while bordes is None:
                    pyautogui.sleep(0.05)
                    bordes = pyautogui.locateOnScreen(ERROR, confidence=confidence)
                    
                    gc.collect()
                if self.verbose:
                    RuntimeWarning("Se detectó una ventana de error o emergencia. Ha sido inmediatamente cerrada.")
                pyautogui.typewrite('\n')   
                pyautogui.sleep(0.7)
                
                
        # pool_warning = Pool(1,maxtasksperchild=100)
        # pool_warning.apply_async(detect_warning,[])
        
        # pool_warning.close()
        # pool_warning.join()
        
        
        ############################################################
        ####### Ajustamos la escala DB por defecto:25
        posicion_boton = None     
        confidence = .95
        if self.verbose:
            print("Buscando boton de nivel DB Snr")
            
        while posicion_boton is None:
            posicion_boton = pyautogui.locateOnScreen(DB_SNR, confidence=confidence)
            confidence-=.05
            if confidence<0.4: LookupError("No se encontró el botón DB Snr.")                 
            pyautogui.sleep(0.02)
            
        if self.verbose:
            print("Se seleccionó el boton de Db SNR")
        
        # Doble click        
        self.__click(posicion_boton,3)        
        
        for letter in str(TH_DB):
            pyautogui.typewrite(letter)
            pyautogui.sleep(0.05)
        
        pyautogui.typewrite('\n')    
        ############################################################
        # Ahora procedemos a ajustar los archivos 
        # :-> Presionar x  -> Siguiente
        # .-> Presionar w  -> Ajustar 
        ############################################################
        
        def check_if_correct_window():
            confidence=.9
            posicion_boton  = None
            while posicion_boton is None:
                posicion_boton = pyautogui.locateOnScreen(LAYERS, confidence=confidence)
                confidence-=.07
                if confidence < 0.5: return None 
            
            return posicion_boton  
            

        
        flag_set = False
        bt = None 

        pyautogui.sleep(0.5)
        if self.verbose:
            print("Empezamos con el ajuste....")        
            
        for _ in range(n_adjust):
            
            # Ajustamos la curva
            if flag_set is False:
                bt = check_if_correct_window()
                if bt is None:
                    raise  RuntimeError("Error en la ejecución del programa SAOExplorer.")
                

            pyautogui.typewrite('\n') 
            pyautogui.sleep(0.3)  
            self.__click(bt,2)
            pyautogui.typewrite('w')
            
            # Delay por ajuste 
            pyautogui.sleep(TIME_SLEEP_BY_ADJUST)
            
            # Pasamos al siguiente ajuste
           
            pyautogui.typewrite('\n')  
            pyautogui.sleep(0.3) 
            self.__click(bt,2)

            pyautogui.typewrite('x')
            pyautogui.sleep(1.5)
            
            
        def cerrar_ventana():
            # Obtener el identificador de la ventana activa
            ventana_activa = win32gui.GetForegroundWindow()

            # Enviar el mensaje de cierre a la ventana
            win32api.PostMessage(ventana_activa, win32con.WM_CLOSE, 0, 0)
        
        cerrar_ventana()
        #########################################        
        #Finalmente cerramos la ventana
        if self.verbose:
            print("Cerramos la ventana...")
        
     
        pyautogui.sleep(5)
        #Esperamos 10 o 15 segundos para detectar algun error
    
        # pool_warning.terminate()
        
####################
        # Guardamos lo ajustado a un archivo .SAO
        # 
        # ##########################################################
        
        
        posicion_boton = None     
        confidence =.5

        if self.verbose:
            print("Buscando el boton File")
        while posicion_boton is None:
            posicion_boton = pyautogui.locateOnScreen(MENU, confidence=confidence)
            confidence = confidence-0.05 
            if confidence<0.4: LookupError("No se encontró el botón de guardado de menú en el SaoExplorer.")
            pyautogui.sleep(0.05)
            
            
        if self.verbose:
            print("Se hizo click al botón de Menú.")
            
            
        self.__click(posicion_boton)
        
        # Hacemos click en el boton de guardado
        posicion_boton = None     
        confidence =.85
        if self.verbose:
            print("Buscando el botón SaoAllRecords")
            
        while posicion_boton is None:
            posicion_boton = pyautogui.locateOnScreen(SAVE_SAO_RECORDS, confidence=confidence)
            confidence = confidence-0.05 
            if confidence<0.4: LookupError("No se encontró el botón de exportanción de archivos SAO.")
        
        self.__click(posicion_boton)
        
        
        if self.verbose:
            print("Se seleccionó el boton de guardado de .SAO")
        pyautogui.sleep(0.5)
        #presionamos enter para crear los archivos en el escritorio 
        if self.verbose:
            print("Se guardó todos los archivos .SAO en el escritorio.")
            
        #nos aseguramos estar en el escritorio
        posicion_boton = None     
        confidence =.85
        if self.verbose:
            print("Buscando el botón de Desktop")
            
        while posicion_boton is None:
            posicion_boton = pyautogui.locateOnScreen(ESCRITORIO, confidence=confidence)
            confidence = confidence-0.05 
            if confidence<0.4: LookupError("No se encontró el botón de exportanción de archivos SAO.")

        self.__click(posicion_boton)        
        
        pyautogui.typewrite('\n')
        pyautogui.sleep(0.5)
        pyautogui.typewrite('\n')
        #Esperamos 20 segundos para el guardado
        pyautogui.sleep(10)
        #Cerramos el programa
        if self.verbose:
            print("Se cierra el programa SaoExplorer.....")

        # Llamar a la función para cerrar la ventana
        cerrar_ventana()
       
        ##############################################################
        
        pool.close()
        pool.join()
        pool.terminate()
        #Terminar todos los procesos 
        pyautogui.sleep(10)
        return True 
        
        
        
        
    def __init_config(self):
        
        if self.FlagInitConfig is False:
            
            self.FlagInitConfig =True
            
            if self.ini_date is None:
                 
                ValueError("Verifique el valor proporcionado a la fecha inicial de obtención de datos.")
                    
            if self.fin_date is None:
                
                self.fin_date = self.ini_date
            
            if self.path_explorer is None:
                AttributeError("Proporcione una ruta donde esté contenido el programa SAOExplorer con el parámetro 'path_explorer'.")
            
            self.system = platform.system()
            
            if self.system in ['Windows' , 'Linux']:
                if self.verbose:
                    print("Su sistema operativo actual es {}".format(self.system))
            
            
            if self.system == 'Windows':
                
                self.bash = "win.bat"
                
            # Revisamos si la carpeta temp existe en el escritorio.
            # Si existe, se borra
            if os.path.exists(SRC_TEMP):
                if self.verbose:
                    print("Existia una carpeta temporal con datos NGI. Ha sido borrada completamente.")
                shutil.rmtree(SRC_TEMP)
            else:
                
                os.mkdir(SRC_TEMP)
                
            #revisamos si existe el archivo de tablas
                    
            file = os.path.join(".temp","db.pkl")
            
            if not os.path.isdir(os.path.dirname(file)):
                os.makedirs(os.path.dirname(file))
                
                self.database = pd.DataFrame(columns=['name_ngi',
                                                      'name_grm', 
                                                      'name_sao', 
                                                      'path_download',
                                                      'path_sao'])
            else:
                if os.path.isfile(file): 
                    self.database = pd.read_pickle(file)
                else:
                    self.database = pd.DataFrame(columns=['name_ngi',
                                                      'name_grm', 
                                                      'name_sao', 
                                                      'path_download',
                                                      'path_sao'])
    def __add_database(self,array):
        
        name_ngi,name_sao,name_grm,path_download,path_sao = array[0],array[1],array[2],array[3],array[4]
        
        
        new_data = pd.DataFrame({'name_ngi':[name_ngi],
                                 'name_grm':[name_grm],
                                 'name_sao':[name_sao],
                                 'path_download':[path_download],
                                 'path_sao':[path_sao]})
        
    
        self.database = pd.concat([self.database, new_data], ignore_index=True)           
        
         
    def __ftp_connection(self):
 
        try:
            ftp = FTP(SRC_FTP)
            ftp.login(user=USER_FTP, passwd=PWD_FTP)
        
        except:
            raise ValueError("Revisar la conexión al FTP. Posible falla: Conexión a Internet \
                       o credenciales FTP.")
        else:
            return ftp

            
    def __ftp_download(self,ftp ,pftp,pout,tar=False):
       
        '''
        Resumen
        -------------------------------------
        ftp : objeto ftp para descarga
        ptfp: path o nombre del archivo ftp 
        pout: path donde se escribirá el archivo descargado.
        ----------------------------------------------------
        
        Notas:
        El servidor tiene la estructura de:
            /data1/ionosonde/JM91J/2009/08/*
        Donde el * son carpetas organizadas por días y dentro
        de estas existe:
        - ngi
        - img
        - dat
        Procure descargar de la carpeta ngi
            
        '''
     
        if not os.path.isdir(os.path.dirname(pout)):
            os.makedirs(os.path.dirname(pout))
 
        try:
            
            with open(pout, "wb") as file:
                ftp.retrbinary('RETR {}'.format(pftp), file.write)
            
            
            
            if self.verbose:
                print("Se descargó el archivo {} del servidor FTP.".format(pftp))
            
        
        except:
            print("Existió un problema al descargar el archivo {}.".format(os.path.basename(pftp)))
            return False
        else:
            

            ##----- En caso el archivo sea un comprimido 
            
            if tar is True:
                file = tarfile.open(pout)
                file.extractall()
                file.close()
            
                os.remove(pout)
            
            return True 

                    
    def __config_SAOExplorer(self):
        
        
        command =  r'cd {} && {}'.format(self.path_explorer,self.bash)
      
 
        thread = Pool(2,maxtasksperchild=1000)
        
        thread.apply_async(os.system,[command])
        
        return thread
         
        # self.thread.close()
        # self.thread.join()
        
 
     
if __name__ =='__main__':
    ini_date="2018/05/01"
    fin_date="2018/05/20"
    obj = saoVipi(ini_date=ini_date,
                  fin_date=fin_date,
                  verbose=True)
    
 
 

