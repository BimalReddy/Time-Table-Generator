import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api import router as api_router 

app = FastAPI(
    title="School Timetable Generator API",
    description="Backend service for generating clash-free school timetables.",
    version="1.0.0"
)

# CORS Setup: This allows your main school website (frontend) to send 
# requests to this server without being blocked by the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your school's actual URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api")

@app.get("/")
def health_check():
    """A simple endpoint to check if the server is alive."""
    return {
        "status": "online", 
        "message": "Timetable Generator Engine is running!"
    }

if __name__ == "__main__":
    # Boots up the server on port 8000. 
    # reload=True automatically restarts the server when you save changes to files.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
