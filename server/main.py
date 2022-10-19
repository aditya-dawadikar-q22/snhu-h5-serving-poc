from requests import get
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter

from Controller import get_signed_url_for_blob

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter()

# api_app = FastAPI(title="api app")
# @api_app.get("/get-static-page")
# async def getStaticPage(request):
#     return {}

@app.get("/signed-redirect")
async def getRedirect():
    signed_url = get_signed_url_for_blob("content-serving-bucket","animals/carnivorous/img1.jpeg")
    return RedirectResponse(signed_url)

@app.get("/get-signed-url")
async def getSignedURL():
    signed_url = get_signed_url_for_blob("content-serving-bucket","NS_HUM102_C1_S2_Academic Programs of the Humanities_SCORM1.2-20221004T061848Z-001/NS_HUM102_C1_S2_Academic Programs of the Humanities_SCORM1.2/story.html")
    return {"content_url":signed_url}

@app.get("/get-html")
async def getHTML():
    return FileResponse("templates/temp/index.html",media_type="text/html")

@app.get("/get-img")
async def getFile():
    return FileResponse("templates/temp/img1.jpeg")

@app.get("/get-js")
async def getJs():
    return FileResponse("templates/temp/test-js.js",media_type="text/javascript")

@app.get("/get-css")
async def getCSS():
    return FileResponse("templates/temp/styles.css",media_type="text/css")

@general_pages_router.get("/cats")
async def getH5Content(request: Request):
    return templates.TemplateResponse("temp2/index.html",{"request":request})

@general_pages_router.get("/{filename}")
async def getH5Content(request: Request,filename: str):
    return FileResponse(f"templates/temp2/{filename}")


# app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="templates", html=True), name="ui")