import sys 
from pathlib import Path
from Professor import Professor

professor_folder = Path(__file__).parent
sys.path.insert(0, str(professor_folder))

from pathlib import Path

def load_professor(user_id, database=None):
    if database is None:
        base_folder = Path(__file__).parent.parent
        database = base_folder / "Database" / "Accounts.txt"

    with open(database, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip().strip('"') for p in line.split(",")]

            if parts[0] == "PROFESSOR" and parts[1] == user_id:
                # Format: PROFESSOR,professor_id,full_name,department,courses
                # courses are separated by ';'
                department = parts[3] if len(parts) > 3 else ""
                assigned_courses = []
                if len(parts) > 4 and parts[4]:
                    assigned_courses = parts[4].split(';')
                
                return Professor(
                    professor_id=parts[1],
                    full_name=parts[2],
                    department=department,
                    assigned_courses=assigned_courses
                )

    return None