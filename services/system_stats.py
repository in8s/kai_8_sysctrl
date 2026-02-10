import psutil
from fastapi import HTTPException
import asyncio

latest_stats = {}

def check_system_stats():

    info = {
        'CPU Usage': 'unknown',
        'RAM Usage': 'unknown'
    }

    try:
        info['CPU Usage'] = psutil.cpu_percent(interval=None)
        info['RAM Usage'] = psutil.virtual_memory().percent
    except PermissionError:
        raise HTTPException(status_code=404, detail='You dont have permissions to do that')



    return info



async def monitor_stats(): 

    global latest_stats     

    while True: 
        try:

            latest_stats = check_system_stats()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"blad moitoringu {e}")
            await asyncio.sleep(5)