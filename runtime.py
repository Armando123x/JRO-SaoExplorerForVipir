import os 
import numpy
from multiprocessing import Pool

def read_config():


    filename = 'config.txt'
    path = os.getcwd()

    path = os.path.join(path,filename)

    file_exists = os.path.isfile(path)

    if file_exists:
        
        with open(path,'r') as file:

            buff = numpy.array(file.read().splitlines(),dtype=object)
            tmp = list()
            for line in buff:
                if line[0]!="#" and len(line)>0:
                    tmp.append(line)
            
            if len(tmp)==3:
                return numpy.array(tmp,dtype=object)
            else:
                raise FileExistsError("Revise la sintaxis del archivo {}".format(filename))

    else:

        raise FileNotFoundError("El archivo {} no existe en el directorio {}".format(filename,os.path.dirname(path)))


if __name__ == "__main__":

    ######Empezamos leyendo el archivo de configuración
    lines = read_config()
    
    initial_date = lines[0]
    final_date = lines[1]
    refresh = lines[2]
    
    refresh = int(refresh)
    
    #lugar principal 
    while (1):


        

        
