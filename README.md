# PDF Writer Microservice

## Overview 

A FastAPI-based service that generates maintenance report PDFs from JSON data using ReportLab. 
This microservice:
- Accepts a folder path, a filename, and a list of maintenance records in JSON format
- Creates a landscape-oriented PDF using ReportLab showing the records in a table format
- Saves the PDF to the desired folder with desired filename
- Returns a JSON response stating the output file path (where the PDF was saved)

### Prerequisites
Before using, please make sure you have:
- Python 3.8 or later installed
- Install the following Python packages:
  ```pip install fastapi reportlab pydantic```

### How to programmatically REQUEST data
1. Send an HTTP POST to the /generate endpoint on the running service (http://localhost:8000/generate).
2. Format JSON body to match this schema:
```
{
  "folder": "./output",           // Target directory for PDF
  "filename": "report.pdf",       // Desired PDF filename
  "records": [                    // Array of maintenance records
    {
      "recordID": "1",
      "car": "2015 Subaru Outback",
      "license": "234BCD",
      "serviceDate": "04 May 2025",
      "mileage": "113450",
      "serviceType": "Seasonal tire changeover",
      "provider": "Myself",
      "notes": ""
    }
    // ...additional record objects...
  ]
}
```
    
3. Send JSON payload using POST Requests
```
import requests

payload = {
    "folder": "./output",
    "filename": "maintenance_report.pdf",
    "records": [
        {
            "recordID": "1",
            "car": "Example Car",
            "license": "ABC123",
            "serviceDate": "01 Jan 2025",
            "mileage": "10000",
            "serviceType": "Oil Change",
            "provider": "Shop",
            "notes": "Changed oil filter"
        }
    ]
}

response = requests.post(
    "http://localhost:8000/generate", json=payload
)
```

### How to programatically RECEIVE data
JSON data will be provided in the response once the microservice reads and creates the PDF file of the requested maintenance records and saves it to the requested folder. The microservice will provide a confirmation message and file path if the pdf was successfully generated. 

```
    # Check POST response status
      response = requests.post("http://127.0.0.1:8000/generate", json=payload)
      if response.status_code == 200 and response.json().get("status") == "success":
          print("PDF saved at", response.json()["path"])
      else:
          print("Error:", response.status_code, response.text)
```

