from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
import pandas as pd
from utils.geo import geocode_address
from utils.census import get_census_tract

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_filename = f"enriched_{file.filename}"  # <-- moved up here
    output_path = os.path.join(upload_dir, output_filename)

    try:
        df = pd.read_excel(file_path)

        if "Full Address" not in df.columns:
            raise ValueError("Spreadsheet must contain a 'Full Address' column.")

        if "ZIP" not in df.columns:
            raise ValueError("Spreadsheet must contain a 'ZIP' column.")

        df.to_excel(output_path, index=False)
        message = f"File '{file.filename}' uploaded successfully. Choose an operation below."

    except Exception as e:
        message = f"Error uploading file '{file.filename}': {str(e)}"

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "message": message,
        "enriched_filename": output_filename  # <-- always defined
    })



@app.post("/process/geocode")
async def process_geocode(request: Request, filename: str = Form(...)):
    return await process_enrichment(request, filename, do_geocode=True, do_census=False)


@app.post("/process/census")
async def process_census(request: Request, filename: str = Form(...)):
    return await process_enrichment(request, filename, do_geocode=False, do_census=True)


@app.post("/process/both")
async def process_both(request: Request, filename: str = Form(...)):
    return await process_enrichment(request, filename, do_geocode=True, do_census=True)


@app.post("/process/social")
async def process_social(request: Request, filename: str = Form(...)):
    return templates.TemplateResponse("upload.html", {
        "request": request,
        "message": "Social media recommendation is not implemented yet.",
        "enriched_filename": filename
    })


async def process_enrichment(request: Request, filename: str, do_geocode=False, do_census=False):
    upload_dir = "uploads"
    file_path = os.path.join(upload_dir, filename)

    try:
        df = pd.read_excel(file_path)

        if do_geocode:
            def try_geocode(row):
                result = geocode_address(row["Full Address"])
                if result is None or None in result:
                    zip_code = str(row.get("ZIP", "")).strip()
                    return geocode_address(zip_code) if zip_code else (None, None)
                return result

            df[["latitude", "longitude"]] = df.apply(try_geocode, axis=1, result_type='expand')

        if do_census:
            def enrich_with_census(row):
                if pd.notnull(row.get("latitude")) and pd.notnull(row.get("longitude")):
                    tract_data = get_census_tract(row["longitude"], row["latitude"])
                    if tract_data:
                        for key, value in tract_data.items():
                            row[key] = value
                return row

            df = df.apply(enrich_with_census, axis=1)

        output_filename = f"enriched_{filename}"
        output_path = os.path.join(upload_dir, output_filename)
        df.to_excel(output_path, index=False)

        message = "File processed successfully."
        download_link = f"/download/{output_filename}"

    except Exception as e:
        message = f"Error processing file '{filename}': {str(e)}"
        download_link = None

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "message": message,
        "enriched_filename": filename,
        "download_link": download_link
    })


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("uploads", filename)
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
