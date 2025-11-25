import pytest
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Add necessary directories to path
root_folder = Path(__file__).parent
professor_files_folder = root_folder / "Professor Files"
admin_folder = root_folder / "Admin_files"
sys.path.insert(0, str(professor_files_folder))
sys.path.insert(0, str(admin_folder))
sys.path.insert(0, str(root_folder))

from Professor import Professor
from Course import Course
from professor_driver import professor_driver


class TestProfessorDriver:
    """Test suite for professor_driver function"""

    def setup_method(self):
        """Setup test fixtures before each test"""
        # Create a test professor
        self.professor = Professor("700123456", "Dr. Test Professor", "Computer Science", ["12345", "67890"])
        
        # Create test courses and register them
        self.course1 = Course("CPSC 101", "MWF 10-11AM", 3, ["900111111", "900222222"])
        self.course1.CRN = 12345
        Course.courses_by_crn["12345"] = self.course1
        
        self.course2 = Course("CPSC 201", "TR 2-3:30PM", 3, ["900333333"])
        self.course2.CRN = 67890
        Course.courses_by_crn["67890"] = self.course2

    def teardown_method(self):
        """Cleanup after each test"""
        # Clear the course registry
        Course.courses_by_crn.clear()
        Course.crns_list.clear()

    @patch('builtins.input', side_effect=['5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_exit_menu(self, mock_stdout, mock_input):
        """Test that choosing option 5 exits the menu"""
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "PROFESSOR MENU" in output

    @patch('builtins.input', side_effect=['1', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_assigned_courses(self, mock_stdout, mock_input):
        """Test viewing assigned courses"""
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "Dr. Test Professor's Assigned Courses" in output
        assert "CPSC 101" in output
        assert "CPSC 201" in output
        assert "12345" in output
        assert "67890" in output

    @patch('builtins.input', side_effect=['1', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_assigned_courses_empty(self, mock_stdout, mock_input):
        """Test viewing assigned courses when professor has none"""
        empty_prof = Professor("700999999", "Dr. Empty", "Mathematics")
        professor_driver(empty_prof)
        output = mock_stdout.getvalue()
        assert "No courses assigned" in output

    @patch('builtins.input', side_effect=['2', '12345', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_see_enrolled_students(self, mock_stdout, mock_input):
        """Test viewing enrolled students in a course"""
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "CPSC 101" in output
        assert "900111111" in output
        assert "900222222" in output
        assert "Enrolled Students (2)" in output

    @patch('builtins.input', side_effect=['2', '99999', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_see_students_not_assigned_course(self, mock_stdout, mock_input):
        """Test trying to view students for a course not assigned to professor"""
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "not assigned to you" in output

    @patch('builtins.input', side_effect=['2', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_see_students_no_courses(self, mock_stdout, mock_input):
        """Test viewing students when professor has no assigned courses"""
        empty_prof = Professor("700999999", "Dr. Empty", "Mathematics")
        professor_driver(empty_prof)
        output = mock_stdout.getvalue()
        assert "You have no assigned courses" in output

    @patch('builtins.input', side_effect=['3', '12345', 'MWF 1-2PM', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_change_course_time(self, mock_stdout, mock_input):
        """Test changing a course time"""
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "Current Time: MWF 10-11AM" in output
        assert "Course time updated to: MWF 1-2PM" in output
        assert self.course1.time == "MWF 1-2PM"

    @patch('builtins.input', side_effect=['3', '99999', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_change_time_not_assigned_course(self, mock_stdout, mock_input):
        """Test trying to change time for a course not assigned to professor"""
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "not assigned to you" in output

    @patch('builtins.input', side_effect=['3', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_change_time_no_courses(self, mock_stdout, mock_input):
        """Test changing time when professor has no assigned courses"""
        empty_prof = Professor("700999999", "Dr. Empty", "Mathematics")
        professor_driver(empty_prof)
        output = mock_stdout.getvalue()
        assert "You have no assigned courses" in output

    @patch('builtins.input', side_effect=['4', '12345', '900111111', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_drop_student_from_course(self, mock_stdout, mock_input):
        """Test dropping a student from a course"""
        initial_count = len(self.course1.class_list)
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "Student 900111111 dropped from CPSC 101" in output
        assert len(self.course1.class_list) == initial_count - 1
        assert "900111111" not in self.course1.class_list

    @patch('builtins.input', side_effect=['4', '12345', '900999999', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_drop_student_not_in_course(self, mock_stdout, mock_input):
        """Test trying to drop a student not enrolled in the course"""
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "Student 900999999 not found in this course" in output

    @patch('builtins.input', side_effect=['4', '99999', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_drop_student_not_assigned_course(self, mock_stdout, mock_input):
        """Test trying to drop student from course not assigned to professor"""
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "not assigned to you" in output

    @patch('builtins.input', side_effect=['4', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_drop_student_no_courses(self, mock_stdout, mock_input):
        """Test dropping student when professor has no assigned courses"""
        empty_prof = Professor("700999999", "Dr. Empty", "Mathematics")
        professor_driver(empty_prof)
        output = mock_stdout.getvalue()
        assert "You have no assigned courses" in output

    @patch('builtins.input', side_effect=['99', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_menu_choice(self, mock_stdout, mock_input):
        """Test entering an invalid menu option"""
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        assert "Invalid choice" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
