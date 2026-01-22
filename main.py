from fastapi import FastAPI, Query, HTTPException, status, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pathlib import Path
from typing import Annotated
import os
from dotenv import load_dotenv
from services.network_management import get_network_info 
import bcrypt


load_dotenv()




#tworzymy zmienna app ktora jest nasza instancja klasy FastAPI
app = FastAPI()

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

