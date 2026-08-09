import csv
import io
from typing import List
from app.models import ScheduledLesson

class TimetableExporter:
    def __init__(self, schedule: List[ScheduledLesson], days_per_week: int = 5, periods_per_day: int = 8):
        self.schedule = schedule
        self.days = days_per_week
        self.periods = periods_per_day
        self.day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def _create_empty_grid(self) -> List[List[str]]:
        """Creates a blank 2D grid [Days][Periods]."""
        return [["" for _ in range(self.periods)] for _ in range(self.days)]

    def generate_class_grid(self, class_name: str) -> List[List[str]]:
        """Filters the schedule for a specific class and places it into a grid."""
        grid = self._create_empty_grid()
        
        for lesson in self.schedule:
            if lesson.class_group_name == class_name:
                # Format the cell as "Subject - Teacher (Room)"
                cell_text = f"{lesson.subject_name} - {lesson.teacher_name} ({lesson.room_name})"
                grid[lesson.day][lesson.period] = cell_text
                
        return grid

    def generate_teacher_grid(self, teacher_name: str) -> List[List[str]]:
        """Filters the schedule for a specific teacher and places it into a grid."""
        grid = self._create_empty_grid()
        
        for lesson in self.schedule:
            if lesson.teacher_name == teacher_name:
                # Format the cell as "Subject - Class (Room)"
                cell_text = f"{lesson.subject_name} - {lesson.class_group_name} ({lesson.room_name})"
                grid[lesson.day][lesson.period] = cell_text
                
        return grid

    def export_to_csv(self, grid: List[List[str]], title: str) -> str:
        """
        Converts a 2D grid into a CSV string format that can be downloaded 
        and opened in Microsoft Excel or Google Sheets.
        """
        # io.StringIO acts like a file, but lives purely in memory (faster for web APIs)
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write a title row and a blank spacer row
        writer.writerow([f"Timetable for: {title}"])
        writer.writerow([])
        
        # Write the Header Row (Period 1, Period 2, etc.)
        headers = ["Day / Period"] + [f"Period {p + 1}" for p in range(self.periods)]
        writer.writerow(headers)
        
        # Write the data rows
        for day_index in range(self.days):
            day_name = self.day_names[day_index]
            row_data = [day_name] + grid[day_index]
            writer.writerow(row_data)
            
        return output.getvalue()
