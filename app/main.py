from fastapi import FastAPI, Query, Path, Body, HTTPException
import psycopg2
import configparser
import logging
import time
from pydantic import BaseModel
from src.api import user_controller
from src.core import state

config = configparser.ConfigParser()
config.read("conf.ini")

conn = psycopg2.connect(
    host=config["POSTGRE"]["host"],
    user=config["POSTGRE"]["user"],
    password=config["POSTGRE"]["pwd"],
    database=config["POSTGRE"]["db_name"],
)

app = FastAPI(title="Demo FastAPI App")

log_file = "logs/fastapi_"+ time.strftime("%Y-%d-%m,%H:%M:%S") + ".log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s - [%(module)s > %(filename)s > %(funcName)s]')
logger = logging.getLogger()

@app.on_event("startup")
def startup():
    state.conn = conn
    state.cur = conn.cursor()
    state.logger = logger
    state.logger.info("Globals created")

app.include_router(user_controller.router)