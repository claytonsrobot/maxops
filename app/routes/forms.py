from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

#from app.utils.helpers import save_hourly_data_to_csv,save_hourly_data_to_json,save_hourly_data_to_toml
import app.utils.helpers as helpers

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/hourly-form", response_class=HTMLResponse)
async def render_hourly_form(request: Request):
    return templates.TemplateResponse("hourly_form.html", {"request": request})

@router.post("/submit-hourly")
async def submit_hourly_data(
    timestamp: str = Form(...),
    influent_flow_rate_MGD: float = Form(...),
    after_wet_well_flow_rate_MGD: float = Form(...),
    effluent_flow_rate_MGD: float = Form(...),
    was_flow_rate_MGD: float = Form(...),
    operator: str = Form(...)
):
    data = {
        "timestamp_entry_ISO": helpers.nowtime(),
        "timestamp_intended_ISO": helpers.sanitize_time(timestamp),
        "inluent_flow_rate_MGD": influent_flow_rate_MGD,
        "after_wet_well_flow_rate_MGD": after_wet_well_flow_rate_MGD,
        "effluent_flow_rate_MGD": effluent_flow_rate_MGD,
        "was_flow_rate_MGD": was_flow_rate_MGD,
        "operator": operator,
    }
    helpers.save_hourly_data(data)
    # Process the data (you can save it to a database or log it)
    print(f"Received hourly data: {data}")
    return {"message": "Hourly data submitted successfully!"}


@router.post("/submit-daily")
async def submit_daily_data(
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
    helpers.save_daily_data(data)
    # Process the data (you can save it to a database or log it)
    print(f"Received hourly data: {timestamp}, {flow_rate}, {cod}, {water_quality}")
    return {"message": "Hourly data submitted successfully!"}

@router.post("/submit-outfall")
async def submit_outfall_data(
    timestamp: str = Form(...),
    safe_to_make_observation: bool = Form(...),
    flotable_present: bool = Form(...),
    scum_present: bool = Form(...),
    foam_present: bool = Form(...),
    oil_present: bool = Form(...),
    operator: str = Form(...)
):
    try:
        # Convert integer flags to boolean values
        print(f"timestamp = {timestamp}")
        data = {
            "timestamp_entry_ISO": helpers.nowtime(),
            "timestamp_intended_ISO": helpers.sanitize_time(timestamp),
            "safe_to_make_observation": safe_to_make_observation,
            "flotable_present": flotable_present,
            "scum_present": scum_present,
            "foam_present": foam_present,
            "oil_present": oil_present,
            "operator": operator,
        }

        # Save the data using the appropriate helper method
        helpers.save_outfall_data(data)

        # Log for debugging
        print(f"Received outfall data: {data}")

        return {"message": "Outfall data submitted successfully!"}

    except Exception as e:
        print(f"Error processing outfall data: {e}")
        return {"error": str(e)}
