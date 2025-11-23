import unittest
from Admin_files.Course import Course

class TestCourseMethods(unittest.TestCase):

    def test_dispay_crn_desc(self):
        course = Course(course_name="Test Course", time="MWF 10-11", class_list=[])
        test_csv_path = "test_courses.csv"  
        Course.save_all_courses_to_csv("test_courses.csv")
        course.display_crn_desc(test_csv_path)

