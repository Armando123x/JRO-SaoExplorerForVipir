from main import * 
from variables import * 
from datetime import datetime
from others import *

if __name__ =='__main__':

    # send_ftp()
    # send_ftp_sao()

    save_grm = False
    ini_date="2020/03/24"
    fin_date="2021/12/31"

    # obj = saoVipi(ini_date=ini_date,
    #                       fin_date=fin_date,
    #                       save_grm = save_grm,
    #                    verbose=True,
    # #                    realtime_web = True)
        
    # gen_latest()
    # send_scp()
    # send_ftp()
    # send_ftp_sao()

    time0 = 0







    while 1:
        try:
        # if (datetime.now().timestamp()-time0 >1*60*60):
            time0 = datetime.now().timestamp()
            ini_date="2020/03/24"
            fin_date="2021/12/31"
            obj = saoVipi(ini_date=ini_date,
                          fin_date=fin_date,
                          save_grm = save_grm,
                       verbose=True,
                       realtime_web = True)
             
            gen_latest()
            send_scp()
            send_ftp()
            send_ftp_sao()
        except:
            print(traceback.format_exc())
            
            gen_latest()
            send_scp()
            send_ftp()
            send_ftp_sao()
            