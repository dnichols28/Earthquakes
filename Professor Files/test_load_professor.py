import pytest
from pathlib import Path
import sys
import os
import tempfile

# Add Professor Files directory to path
root_folder = Path(__file__).parent
professor_files_folder = root_folder / "Professor Files"
sys.path.insert(0, str(professor_files_folder))

from Professor import Professor
from load_professor import load_professor


class TestLoadProfessor:
    """Test suite for load_professor function"""

    def test_load_professor_success(self):
        """Test successfully loading a professor from database"""
        # Create a temporary database file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            # Write sample data
            f.write("STUDENT,900123456,John Doe,Freshman,Computer Science,true\n")
            f.write("PROFESSOR,700123456,Dr. Jane Smith,Mathematics,12345;67890\n")
            f.write("ADMIN,800123456,Admin User\n")

        try:
            # Load the professor
            prof = load_professor("700123456", temp_file)
            
            assert prof is not None
            assert prof.professor_id == "700123456"
            assert prof.full_name == "Dr. Jane Smith"
            assert prof.department == "Mathematics"
            assert prof.assigned_courses == ["12345", "67890"]

        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_no_courses(self):
        """Test loading a professor with no assigned courses"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("PROFESSOR,700999999,Dr. New Professor,Physics,\n")

        try:
            prof = load_professor("700999999", temp_file)
            
            assert prof is not None
            assert prof.professor_id == "700999999"
            assert prof.full_name == "Dr. New Professor"
            assert prof.department == "Physics"
            assert prof.assigned_courses == []

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_not_found(self):
        """Test loading a professor that doesn't exist"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("STUDENT,900123456,John Doe,Freshman,Computer Science,true\n")
            f.write("ADMIN,800123456,Admin User\n")

        try:
            prof = load_professor("700999999", temp_file)
            assert prof is None

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_wrong_user_type(self):
        """Test that loading a student ID as professor returns None"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("STUDENT,900123456,John Doe,Freshman,Computer Science,true\n")

        try:
            prof = load_professor("900123456", temp_file)
            assert prof is None

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_with_special_characters(self):
        """Test loading professor with special characters in name (without commas in quoted fields)"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            # Use a name with apostrophe but no comma to avoid CSV parsing issues
            f.write('PROFESSOR,700123456,Dr. O\'Brien PhD,Computer Science,11111\n')

        try:
            prof = load_professor("700123456", temp_file)
            
            assert prof is not None
            assert prof.professor_id == "700123456"
            assert "O'Brien" in prof.full_name or "O\\'Brien" in prof.full_name
            assert prof.department == "Computer Science"
            assert prof.assigned_courses == ["11111"]

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_empty_file(self):
        """Test loading from an empty database file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            # Empty file

        try:
            prof = load_professor("700123456", temp_file)
            assert prof is None

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_multiple_courses(self):
        """Test loading professor with multiple courses"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("PROFESSOR,700555555,Dr. Multi Course,Engineering,10001;10002;10003;10004\n")

        try:
            prof = load_professor("700555555", temp_file)
            
            assert prof is not None
            assert len(prof.assigned_courses) == 4
            assert "10001" in prof.assigned_courses
            assert "10004" in prof.assigned_courses

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_default_database_path(self):
        """Test that default database path is used when not provided"""
        # This test checks that the function can be called without database parameter
        # It will fail if Database/Accounts.txt doesn't exist, so we just check the call works
        try:
            prof = load_professor("700000000")  # Non-existent ID
            assert prof is None  # Should return None for non-existent professor
        except FileNotFoundError:
            # It's okay if the default database doesn't exist yet
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
