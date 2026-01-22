import subprocess
import re 
from fastapi import HTTPException, status
import socket


def get_network_info(option: str, host: str | None = None):

    try:
        if option == "A":
            result = subprocess.check_output(['ipconfig', "/all"], text = True, encoding = "cp852", errors = 'ignore')
        elif option == "B":
            result = subprocess.check_output('getmac', text = True, encoding = 'cp852', errors = 'ignore')
        elif option == "C":
            if not host:
                raise HTTPException(status_code=400, detail = "Host is required!")
            pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

            validated_host = re.match(pattern, host) is not None

            if validated_host:
                try:
                    hostname = socket.gethostbyname(host)
                    result = subprocess.check_output(['nslookup', hostname], text = True, encoding = 'utf-8', errors="ignore")
                except socket.gaierror:
                    raise HTTPException(status_code = "500", detail = 'Invalid hostname!')

        else:
            raise HTTPException(status = status.HTTP_401_UNAUTHORIZED, detail = 'Not known option')

        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code = '500', detail = "nie dziala")
