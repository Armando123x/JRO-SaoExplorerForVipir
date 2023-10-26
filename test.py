import numpy
import os
from multiprocessing import Pool
import time

def child():

    count = 0
    while(1):

        count +=1
        print("Contador hijo",count)
        if count ==30:
            TimeoutError("Eroresd")
             
        time.sleep(0.1)


if __name__ == "__main__":

    flag = False
    count =0
    time_init = time.time()
    while (1):
        

        if flag is False:
            pool = Pool(2,maxtasksperchild=1000)
            pool.apply_async(child,[])
            
            # pool.close()
            # pool.join()

            flag = True
        
        time.sleep(2)
        print("Tiempo actual de ejecución {}".format(time.time()-time_init))

        


