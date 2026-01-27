from scapy.all import ARP, conf, Ether, srp
import os
from fastapi import HTTPException
# Wyciszamy zbędne komunikaty
conf.verb = 0

# Poprawiona struktura srp
# Pamiętaj o uruchomieniu jako SUDO!

def scan_network(range: str = "192.168.0.1/24"):
    devices_list = []

    try:
        target_ip = "192.168.0.1/24"
        # srp zwraca (answered, unanswered). Timeout musi być poza nawiasem ARP!
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip), timeout=2, inter=0.1)
    
        for snd, rcv in ans:
        # rcv.hwsrc to adres MAC nadawcy, rcv.psrc to jego IP
            devices_list.append({
                'MAC':rcv.hwsrc,
                'IP':rcv.psrc
            })

        return {
            'range': range,
            'lenght':len(devices_list),
            'ip':devices_list
        }

    except PermissionError:
        raise HTTPException(status_code = 500, detail = "Brak uprawnień Administratora")
    except Exception as e:
        raise HTTPException(status_code = 500, detail = "Błąd skanowania")