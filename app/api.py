from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from typing import List

from app.models import TimetableRequest, TimetableResponse, ScheduledLesson
from app.solver import TimetableSolver
from app.exporter import TimetableExporter

router = APIRouter()

# Create a router to organize our endpoints
router = APIRouter()

@router.post("/generate", response_model=TimetableResponse)
def generate_timetable(request: TimetableRequest):
    """
    Endpoint to generate a new timetable.
    Expects a JSON payload matching the TimetableRequest model.
    """
    try:
        # 1. Feed the validated data into our solver engine
        solver = TimetableSolver(request)
        
        # 2. Run the math to find a clash-free schedule
        response = solver.solve()
        
        # 3. Return the results (whether it succeeded or failed)
        # We don't raise an HTTP error on "failed" because an impossible schedule
        # is a valid solver outcome, not a server crash.
        return response
        
    except Exception as e:
        # If something completely unexpected breaks, we return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
@router.post("/export/class/{class_name}")
def export_class_csv(class_name: str, schedule: List[ScheduledLesson]):
    """
    Takes a generated schedule JSON and returns a downloadable CSV for a specific class.
    """
    try:
        # 1. Initialize the exporter with the schedule data sent by the website
        exporter = TimetableExporter(schedule)
        
        # 2. Generate the 2D grid for the specific class
        grid = exporter.generate_class_grid(class_name)
        
        # 3. Convert that grid into a CSV string
        csv_string = exporter.export_to_csv(grid, class_name)
        
        # 4. Return it as a downloadable file
        return PlainTextResponse(
            content=csv_string, 
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={class_name}_timetable.csv"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
