import unittest
from app.models import Room, Teacher, ClassGroup, LessonRequirement, TimetableRequest
from app.solver import TimetableSolver

class TestTimetableSolver(unittest.TestCase):

    def setUp(self):
        """
        This runs before every test. We set up a small, valid 'fake school' here.
        """
        self.rooms = [
            Room(id="R1", name="Math Room", capacity=30, is_lab=False),
            Room(id="R2", name="Science Lab", capacity=25, is_lab=True)
        ]
        self.teachers = [
            Teacher(id="T1", name="Mr. Smith (Math)", max_periods_per_week=10),
            Teacher(id="T2", name="Ms. Davis (Science)", max_periods_per_week=10)
        ]
        self.classes = [
            ClassGroup(id="C1", name="Grade 10A", student_count=20)
        ]
        
        # 3 Math periods, 2 Science (Lab) periods. Total = 5 lessons to schedule.
        self.lessons = [
            LessonRequirement(
                id="L1", subject_name="Math", teacher_id="T1", 
                class_group_id="C1", periods_per_week=3, requires_lab=False
            ),
            LessonRequirement(
                id="L2", subject_name="Science", teacher_id="T2", 
                class_group_id="C1", periods_per_week=2, requires_lab=True
            )
        ]

        self.valid_request = TimetableRequest(
            rooms=self.rooms,
            teachers=self.teachers,
            class_groups=self.classes,
            lessons=self.lessons,
            days_per_week=5,
            periods_per_day=4 # Small week: 20 slots total
        )

    def test_successful_schedule(self):
        """Test that a mathematically possible schedule actually succeeds."""
        solver = TimetableSolver(self.valid_request)
        response = solver.solve()
        
        self.assertEqual(response.status, "success")
        
        # We requested exactly 3 Math + 2 Science = 5 total lesson periods
        self.assertEqual(len(response.schedule), 5)

    def test_lab_constraint(self):
        """Test that Science (which requires a lab) is ONLY scheduled in R2 (the lab)."""
        solver = TimetableSolver(self.valid_request)
        response = solver.solve()
        
        for lesson in response.schedule:
            if lesson.subject_name == "Science":
                self.assertEqual(lesson.room_name, "Science Lab")

    def test_impossible_schedule_fails_gracefully(self):
        """
        Test that if we ask for the impossible, the solver catches it instead of crashing.
        We will demand 25 periods of Math, but the week only has 20 slots.
        """
        impossible_lessons = [
            LessonRequirement(
                id="L1", subject_name="Math", teacher_id="T1", 
                class_group_id="C1", periods_per_week=25, requires_lab=False
            )
        ]
        impossible_request = TimetableRequest(
            rooms=self.rooms,
            teachers=self.teachers,
            class_groups=self.classes,
            lessons=impossible_lessons,
            days_per_week=5,
            periods_per_day=4 # 5 * 4 = 20 slots available
        )
        
        solver = TimetableSolver(impossible_request)
        response = solver.solve()
        
        self.assertEqual(response.status, "failed")
        self.assertEqual(len(response.schedule), 0)

if __name__ == '__main__':
    unittest.main()
