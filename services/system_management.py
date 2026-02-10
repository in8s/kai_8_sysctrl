import socket
import platform
from fastapi import HTTPException
from getmac import get_mac_address as gma
from urllib.request import urlopen
import re as r
import psutil

#to do: 
# 1. hostname, os, c_library, Ipv4, macaddress, public ip
# 2. Oddzielna funkcja, zuzycie procesora, zucycie ramu, ile czasu trwa ekran, do tego wykresy 
#3. 



def get_system_info():

    main_sys_info = {
        'Hostname':'unknown',
        'OS Name': 'unknown',
        'IP Local':'unknown',
        'IP Public': 'unknown',
        'MAC Address': 'unknown'
    }

    try:
        main_sys_info['Hostname'] = platform.node() or 'hostname unavailable'
        main_sys_info['OS Name'] = platform.system()
        main_sys_info['IP Local'] = socket.gethostbyname(socket.gethostname())
        main_sys_info['MAC Address'] = gma()
        data = str(urlopen('http://checkip.dyndns.com/').read())
        ip = r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
        main_sys_info['IP Public'] = ip
        
    except PermissionError:
        raise HTTPException(status = 404, details = 'You dont have permissions...')
    

    return main_sys_info


def get_system_stats():
    pass

