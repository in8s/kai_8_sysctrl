import subprocess
import re 
from fastapi import HTTPException, status


def get_network_info(option: str):

    try:
        if option == "A":
            result = subprocess.check_output(['ipconfig', "/all"], text = True, encoding = "cp852", errors = 'ignore')
        elif option == "B":
            result = subprocess.check_output('getmac', text = True, encoding = 'cp852', errors = 'ignore')
        else:
            raise HTTPException(status = status.HTTP_401_UNAUTHORIZED, detail = 'Not known option')

        return result
    except Exception as e:
        raise HTTPException(status_code = '500', detail = "ni dziala")
