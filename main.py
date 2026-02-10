#FROM imports
from fastapi import FastAPI, Query, HTTPException, status, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pathlib import Path
from typing import Annotated
from dotenv import load_dotenv
from contextlib import asynccontextmanager
#INTERNAL imports
from services.system_stats import monitor_stats, get_latest_stats
from services.network_management import get_network_info 
from services.system_management import get_system_info
from services.network_scanner import scan_network
#JUST imports :))
import bcrypt
import os
import asyncio



load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):

    asyncio.create_task(monitor_stats())
     
    print('Serwer startuje...')


    yield


    print('Serwer gasnie...')






#tworzymy zmienna app ktora jest nasza instancja klasy FastAPI
app = FastAPI(lifespan=lifespan)

#tworzymy zmienna security ktora jest nasza instancja klasy HTTPBasic, ten obiekt bedzie wyciagal login i haslo z naglowkow zapytania http
security = HTTPBasic()




#Tworzymy funkcje odpowiezialna za autoryzacje
#ta funkcja to tak zwane dependency, do uzywania przy kazdym chronionym adresie URL
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    #fastapi widzi Depends(security). Automatycznie sprawdza czy user podal username i password, jesli nie wysyla prosbe o logowanie albo wrzuci te dane do obiektu credentials

    if credentials.username != os.getenv("ADMIN_USERNAME"):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Wrong password or username",
            headers = {"WWW-Authenticate":"Basic"},

        )

    if not bcrypt.checkpw(credentials.password.encode(), os.getenv("ADMIN_PASSWORD").encode()):

        raise HTTPException(

            status_code = status.HTTP_401_UNAUTHORIZED,
            detail  = 'Wrong username or password!',
            headers = {"WWW-Authenticate": "Basic"}

        )

    

    return credentials.username



app.mount(
    "/front",
    StaticFiles(
        directory=Path(__file__).resolve().parent / "front",
        html = True
    ),
    name = "front"
)


@app.get("/api/network/")
def network_api(
    option: str = Query(..., description = "A - ipconfig, B - getmac, C - nslookup"),
    host: str | None = Query(None, description = "Needed for nslookup option!"), 
    username: str = Depends(read_current_user)):

        return get_network_info(option, host)



@app.get("/api/system/")
async def system_api(username: str = Depends(read_current_user)):
    data = await get_system_info()
    return data


@app.get('/api/scan-network')
def scan_api_network(username: str = Depends(read_current_user)):
    return scan_network()

@app.get('/api/system-stats/')
def get_stats_api(username: str = Depends(read_current_user)):
     return get_latest_stats()