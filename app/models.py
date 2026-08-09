from pydantic import BaseModel, Field
from typing import List, Optional

# --- 1. Basic Entities ---

class Room(BaseModel):
    id: str
    name: str
    capacity: int = Field(gt=0, description="Number of students the room can hold")
    is_lab: bool = False

class Teacher(BaseModel):
    id: str
    name: str
    max_periods_per_week: int = Field(gt=0, description="Maximum workload for the teacher")

class ClassGroup(BaseModel):
    id: str
    name: str
    student_count: int = Field(gt=0, description="Total students in this class section")

# --- 2. The Core Requirement ---

class LessonRequirement(BaseModel):
    """
    This tells the solver: "Teacher X must teach Subject Y to Class Z for N periods."
    """
    id: str
    subject_name: str
    teacher_id: str
    class_group_id: str
    periods_per_week: int = Field(gt=0, description="How many times a week they meet")
    requires_lab: bool = False

# --- 3. API Request & Response Models ---

class TimetableRequest(BaseModel):
    """
    This is the exact JSON package the school website will send to our API.
    """
    rooms: List[Room]
    teachers: List[Teacher]
    class_groups: List[ClassGroup]
    lessons: List[LessonRequirement]
    days_per_week: int = 5     # Standard Monday-Friday
    periods_per_day: int = 8   # E.g., 8 periods a day

class ScheduledLesson(BaseModel):
    """
    This represents a single block on the finished timetable.
    """
    lesson_id: str
    subject_name: str
    teacher_name: str
    class_group_name: str
    room_name: str
    day: int
    period: int

class TimetableResponse(BaseModel):
    """
    This is the finished timetable we send back to the website.
    """
    status: str
    message: str
    schedule: List[ScheduledLesson] = []
