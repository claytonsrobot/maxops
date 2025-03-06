from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/hourly-form", response_class=HTMLResponse)
async def render_hourly_form(request: Request):
    return templates.TemplateResponse("hourly_form.html", {"request": request})

@router.post("/submit-hourly")
async def submit_hourly_data(
    timestamp: str = Form(...),
    flow_rate: float = Form(...),
    cod: float = Form(...),
    water_quality: str = Form(...)
):
    data = {
        "timestamp": timestamp,
        "flow_rate": flow_rate,
        "cod": cod,
        "water_quality": water_quality,
    }
    save_hourly_data_to_csv(data)
    save_hourly_data_to_json(data)
    save_hourly_data_to_toml(data)
    # Process the data (you can save it to a database or log it)
    print(f"Received hourly data: {timestamp}, {flow_rate}, {cod}, {water_quality}")
    return {"message": "Hourly data submitted successfully!"}
