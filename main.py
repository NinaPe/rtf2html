import os
import subprocess

import aiofiles as aiofiles
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI(
    title="Conversion Service",
    description="Conversion Service",
    version="0.0.1",
)


@app.post("/convert-to-html/",
          status_code=status.HTTP_200_OK,
          summary="Convert file to html file",
          operation_id="convert_to_html", )
async def convert_to_html(file: UploadFile = File(...)):
    # Save rtf file
    async with aiofiles.open(file.filename, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # convert to html
    subprocess.run(f'libreoffice --headless --convert-to html {file.filename}', shell=True)
    try:
        html_file = open(f"{file.filename.split('.')[0]}.html", 'r', encoding='utf-8')
        content = html_file.read()
        os.remove(html_file.name)
        os.remove(file.filename)

        return HTMLResponse(content=content, status_code=200)
    except Exception as e:
        os.remove(file.filename)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="File not converted")


@app.post("/convert-to-rtf/",
          status_code=status.HTTP_200_OK,
          summary="Convert file to rtf file",
          operation_id="convert_to_rtf", )
async def convert_to_rtf(file: UploadFile = File(...)):
    # Save html file
    async with aiofiles.open(file.filename, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    subprocess.run(f'libreoffice --headless --convert-to "rtf:Rich Text Format" {file.filename}', shell=True)

    try:
        rtf_file = open(f"{file.filename.split('.')[0]}.rtf", 'r', encoding='utf-8')
        content = rtf_file.read()
        os.remove(rtf_file.name)
        os.remove(file.filename)

        return HTMLResponse(content=content, status_code=200)
    except Exception as e:
        os.remove(file.filename)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="File not converted")


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, reload=True, debug=True)
