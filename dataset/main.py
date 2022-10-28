import uvicorn
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from data_api import get_data
import io
import pandas as pd
import pickle
import simplejson

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")



def save_output(data):
    file_name = "out/output.pickle"

    with open(file_name, 'wb') as f:
        pickle.dump(data, f)



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dataset")
async def get_dataset(name: str, asset: str):
    result = get_data(name, asset)
    save_output(result)
    return result

@app.get("/download/{name}")
async def download(request: Request, name: str):
    try:
        with open('out/output.pickle', 'rb') as f:
            data = pickle.load(f)
            df = pd.DataFrame(data['data'][name])
            stream = io.StringIO()
            
            df.to_csv(stream, index=False)
            
            response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
            )
            
            response.headers["Content-Disposition"] = f"attachment; filename={name}.csv"

            return response      
    except Exception as e:
        print(e)
    
    return Response(status_code=404)

def run():
    uvicorn.run('main:app', host="0.0.0.0", port=8062)
