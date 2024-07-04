from main import * 
from variables import * 

from others import *

if __name__ =='__main__':
    save_grm = False
    ini_date="2020/03/24"
    fin_date="2021/12/31"
    obj = saoVipi(ini_date=ini_date,
                  fin_date=fin_date,
                  save_grm = save_grm,
                  verbose=True,
                  realtime_web = True)