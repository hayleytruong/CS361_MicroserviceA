"""
// write_pdf_microservice.py
PDF generating microservice using FASTAPI and ReportLab to parse JSON data and
outputs maintenance record pdfs
"""

import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


class MaintenanceRecord(BaseModel):
    recordID:       str
    car:            str
    license:        str
    serviceDate:    str
    mileage:        str
    serviceType:    str
    provider:       str
    notes:          str = ""  # empty by default


class PDFRequest(BaseModel):
    folder:     str
    filename:   str
    records:    List[MaintenanceRecord]


app = FastAPI()


@app.get("/")
def read_root():
    # Default check to ensure service is running
    return {"Hello": "World"}


@app.post("/generate")
def update_item(request: PDFRequest):
    """
    Generates maintenance report PDF from JSON payload.
    Takes in folder, filename, and list of MaintenanceRecord objects (JSON), creates a formatted pdf using ReportLab, saves the PDF to the specified path and returns its location
    """

    print("[Server]: Received request payload:")
    print(request.model_dump_json())

    try:
        # Extract data from POST requset
        directory = request.folder
        file_name = request.filename
        records = request.records
        print(request)  # FOR DEBUG ONLY

        # Build full file save path
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)

        # Build PDF canvas
        page_size = landscape(A4)
        c = canvas.Canvas(file_path, pagesize=page_size)
        width, height = page_size

        # -- Header
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 50, "Maintenance Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Total records: {len(records)}")

        # -- Table headers
        y_start = height - 100
        y = y_start
        line_height = 18
        left_margin = 50

        # -- Column names and spacing
        headers = [
            ("ID",        left_margin),
            ("Car",       left_margin + 30),
            ("Lic.",      left_margin + 180),
            ("Date",      left_margin + 240),
            ("Miles",     left_margin + 320),
            ("Service",   left_margin + 370),
            ("Provider",  left_margin + 520),
            ("Notes",     left_margin + 600),
        ]
        c.setFont("Helvetica-Bold", 12)
        for text, x in headers:
            c.drawString(x, y, text)

        # -- Table rows
        c.setFont("Helvetica", 10)
        y -= line_height
        for record in records:
            if y < 50:
                c.showPage()
                y = y_start
                c.setFont("Helvetica-Bold", 10)
                for text, x in headers:
                    c.drawString(x, y, text)
                c.setFont("Helvetica", 10)
                y -= line_height

            c.drawString(headers[0][1], y, record.recordID)
            c.drawString(headers[1][1], y, record.car)
            c.drawString(headers[2][1], y, record.license)
            c.drawString(headers[3][1], y, record.serviceDate)
            c.drawString(headers[4][1], y, record.mileage)
            c.drawString(headers[5][1], y, record.serviceType)
            c.drawString(headers[6][1], y, record.provider)
            c.drawString(headers[7][1], y, record.notes or "-")
            y -= line_height

        # Save page
        c.showPage()
        c.save()

        # Return success and saved file path
        response = {"status": "success", "path": file_path}

        print("[Server]: Sending response payload:")
        print(response)

        return response

    except Exception as e:
        print("[Server]: Error while generating PDF:", e)
        raise HTTPException(status_code=500, detail=str(e))
