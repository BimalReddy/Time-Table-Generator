from ortools.sat.python import cp_model
from app.models import TimetableRequest, TimetableResponse, ScheduledLesson
from typing import Dict, Any

class TimetableSolver:
    def __init__(self, request: TimetableRequest):
        self.request = request
        self.model = cp_model.CpModel()
        
        # Look-up dictionaries for easy access
        self.rooms = {r.id: r for r in request.rooms}
        self.teachers = {t.id: t for t in request.teachers}
        self.classes = {c.id: c for c in request.class_groups}
        
        # This will hold all our boolean variables
        self.x = {}

    def build_model(self):
        """Creates variables and applies constraints."""
        
        # --- 1. CREATE VARIABLES ---
        # We create a boolean variable (True/False) for EVERY possible combination of 
        # Lesson + Room + Day + Period. 
        for lesson in self.request.lessons:
            target_class = self.classes[lesson.class_group_id]
            
            for room in self.request.rooms:
                # OPTIMIZATION: If the room is too small, or isn't a lab when needed, 
                # we don't even create a variable for it. This makes the solver much faster.
                if room.capacity < target_class.student_count:
                    continue
                if lesson.requires_lab and not room.is_lab:
                    continue

                for day in range(self.request.days_per_week):
                    for period in range(self.request.periods_per_day):
                        var_name = f'x_L{lesson.id}_R{room.id}_D{day}_P{period}'
                        self.x[(lesson.id, room.id, day, period)] = self.model.NewBoolVar(var_name)

        # --- 2. HARD CONSTRAINTS ---

        # Constraint A: Every lesson must happen exactly `periods_per_week` times.
        for lesson in self.request.lessons:
            # Gather all variables associated with this specific lesson
            lesson_vars = [
                self.x[(l_id, r_id, d, p)] 
                for (l_id, r_id, d, p) in self.x if l_id == lesson.id
            ]
            # The sum of all these True(1) or False(0) variables must equal the required periods
            self.model.AddExactlyK(lesson_vars, lesson.periods_per_week)

        # Constraint B: No collisions! (Teachers, Classes, and Rooms can only do ONE thing at a time)
        for day in range(self.request.days_per_week):
            for period in range(self.request.periods_per_day):
                
                # 1. A Room can only host one lesson at a time
                for room in self.request.rooms:
                    room_vars = [
                        self.x[(l_id, r_id, d, p)] 
                        for (l_id, r_id, d, p) in self.x 
                        if r_id == room.id and d == day and p == period
                    ]
                    self.model.AddAtMostOne(room_vars)

                # 2. A Teacher can only teach one lesson at a time
                for teacher in self.request.teachers:
                    # Find all lessons this teacher teaches
                    teacher_lesson_ids = [l.id for l in self.request.lessons if l.teacher_id == teacher.id]
                    teacher_vars = [
                        self.x[(l_id, r_id, d, p)] 
                        for (l_id, r_id, d, p) in self.x 
                        if l_id in teacher_lesson_ids and d == day and p == period
                    ]
                    self.model.AddAtMostOne(teacher_vars)

                # 3. A Class can only attend one lesson at a time
                for class_group in self.request.class_groups:
                    class_lesson_ids = [l.id for l in self.request.lessons if l.class_group_id == class_group.id]
                    class_vars = [
                        self.x[(l_id, r_id, d, p)] 
                        for (l_id, r_id, d, p) in self.x 
                        if l_id in class_lesson_ids and d == day and p == period
                    ]
                    self.model.AddAtMostOne(class_vars)

    def solve(self) -> TimetableResponse:
        """Runs the engine and formats the output."""
        self.build_model()
        
        solver = cp_model.CpSolver()
        # Give the solver a time limit (e.g., 30 seconds) so it doesn't run forever on impossible data
        solver.parameters.max_time_in_seconds = 30.0 
        
        status = solver.Solve(self.model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            schedule = []
            lessons_dict = {l.id: l for l in self.request.lessons}
            
            # Look at every variable. If the solver set it to True (1), it goes on the schedule!
            for (l_id, r_id, d, p), variable in self.x.items():
                if solver.Value(variable) == 1:
                    lesson_req = lessons_dict[l_id]
                    
                    schedule.append(ScheduledLesson(
                        lesson_id=l_id,
                        subject_name=lesson_req.subject_name,
                        teacher_name=self.teachers[lesson_req.teacher_id].name,
                        class_group_name=self.classes[lesson_req.class_group_id].name,
                        room_name=self.rooms[r_id].name,
                        day=d,
                        period=p
                    ))
            
            return TimetableResponse(
                status="success",
                message="Timetable successfully generated!",
                schedule=schedule
            )
        else:
            # If the engine returns INFEASIBLE, the given requirements are mathematically impossible.
            return TimetableResponse(
                status="failed",
                message="Impossible to schedule with the given constraints (Check room capacities or teacher loads!).",
                schedule=[]
            )
