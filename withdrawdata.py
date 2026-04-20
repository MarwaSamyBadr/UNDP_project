#!/usr/bin/env python

from stat import S_ISREG
import os
import paramiko
from datetime import datetime, timedelta
import re

############### Get data #################     

def getListOfData():  
    import paramiko
  
    HOST = "192.168.50.229"
    USERNAME = "regcm"
    PASSWORD = "regcm00"

    REMOTE_DIR = "/home/regcm/UNDP/rcm-run/Output-RF-SSP126-245-585/UNDP-Processed/" 

    # Connect
    transport = paramiko.Transport((HOST, 22))
    transport.connect(username=USERNAME, password=PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    files = sftp.listdir(REMOTE_DIR)
    sftp.close()
    transport.close()

    return (files)
#################################################################################################
def loadData(local_dir, fileList):    
    HOST = "192.168.50.229"
    USERNAME = "regcm"
    PASSWORD = "regcm00"

    REMOTE_DIR = "/home/regcm/UNDP/rcm-run/Output-RF-SSP126-245-585/UNDP-Processed/" 
    LOCAL_DIR = local_dir 

    # Connect
    transport = paramiko.Transport((HOST, 22))
    transport.connect(username=USERNAME, password=PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        for filename in fileList:
            remote_path = f"{REMOTE_DIR}/{filename}"
            attr = sftp.stat(remote_path)

            #Check if it's a file
            if not S_ISREG(attr.st_mode):
                continue
    
            # Check modification time
            print('filename', filename)
            local_path = os.path.join(LOCAL_DIR, filename)
            sftp.get(remote_path, local_path)
    finally:
        sftp.close()
        transport.close()

    return ()

