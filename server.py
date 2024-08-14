from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlite_helpers import *
from args import get_args
import time
import logging
from enums import Code

""" 
change all your endpoints to have try/except format and when you except, 
raise an HttpException with the status_code as the one from your enums class
"""

# backend
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

args = get_args()
FILE=args.db_name

@app.post("/create-url")
async def create_url(request : Request):
    # process request into json
    req_json = await request.json()
    # if link and alias are defined
    if "link" in req_json and "alias" in req_json:
       result = insert_url(FILE, req_json["link"])
       if result:
           raise(HTTPException(Code.OK.code, detail={"message":"inserted"}))
       else:
           raise(HTTPException(Code.CONFLICT.code, detail={"message":"URL already exists"}))
    else:
        raise(HTTPException(Code.INVALID.code, detail={"message":"invalid"}))
        

@app.get("/list-urls")
def list_url():
    # json with list of urls
    urls_json = {"urls": []}
    # for all urls in database
    for url in list_urls(FILE):
        # store json of data
        input = {"link": url[0], "alias": url[1], "timestamp": url[2], "id": url[3]}
        # add url row to json 
        urls_json["urls"].append(input)
    raise HTTPException(Code.OK.code, detail=urls_json)

@app.get("/find/{alias}")
async def find(alias):
    # locate url
    result = retrieve_url(FILE, alias)
    # if url is found
    if result:
        # redirect user to desired link
        return RedirectResponse(result[0])
    # url is not found, return error
    else:
        raise HTTPException(Code.NOT_FOUND.code, detail={"message":"url not found"})

@app.get("/delete/{alias}")
def delete(alias):
    if delete_url(FILE, alias):
        raise HTTPException(Code.OK.code, detail={"message" : f"successfully deleted link with alias {alias}"}) 
    else:
        raise HTTPException(Code.NOT_FOUND.code, detail={"message" : f"no link associated with alias {alias}"})

@app.get("/logging-levels")
def logging_levels():
    logging.error("error message")
    logging.warning("warning message")
    logging.info("info message")
    logging.debug("debug message")


logging.Formatter.converter = time.gmtime
logging.basicConfig(
    format="%(asctime)s.%(msecs)03dZ %(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level= logging.ERROR - (args.verbose*10),
)
if __name__ == "__main__":
    uvicorn.run("server:app", host=args.host, port=args.port, reload=args.reload)
    