from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlite_helpers import *


# backend
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)
FILE='urls.db'

@app.get("/")
def root():
    return({ "message": "hello world" })

@app.post("/create-url")
def create_url(request : Request):
    # process request into json
    req_json = request.json()
    # if link and alias are defined
    if req_json["link"] and req_json["alias"]:
        # try to insert url
        result = insert_url(FILE, req_json["link"], req_json["alias"])
        # if no duplicates
        if result:
            return({"url" : req_json["link"], "alias": req_json["alias"]})
        else:
            return ({"message" : f"A link with the alias {req_json["alias"]} already exists"})
    # if alias not defined
    else: 
        # return error message
        return({ "message": "link could not be inserted; missing link or alias" })

@app.get("/list-urls")
def list_urls():
    # json with list of urls
    urls_json = {"urls": []}
    # for all urls in database
    for url in list_urls(FILE):
        # store json of data
        input = {"link": url[0], "alias": url[1], "timestamp": url[2], "id": url[3]}
        # add url row to json 
        urls_json["urls"].append(input)
    return urls_json

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
        return {"message": "alias not found"}

@app.get("/delete/{alias}")
def delete(alias):
    if delete_url(FILE, alias):
        return {"message" : f"successfully deleted link with alias {alias}"}
    else:
        return {"message" : f"no link associated with alias {alias}"}

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)
    