from Student import Student

def load_student(name, user_id, database="Database/Accounts.txt"):
    try:
        with open(database, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = [p.strip().strip('"') for p in line.split(",")]

                # Expected format:
                # STUDENT,900123456,John Doe,Freshman,CS,true
                if len(parts) < 6:
                    continue

                record_type = parts[0]
                student_num = parts[1]
                full_name = parts[2]

                # Name + ID must match
                if record_type == "STUDENT" and student_num == user_id and full_name.lower() == name.lower():
                    return Student(
                        student_num=parts[1],
                        full_name=parts[2],
                        classification=parts[3],
                        major=parts[4],
                        fiscal_clearance=parts[5]
                    )
    except FileNotFoundError:
        print("ERROR: Accounts.txt not found.")

    return None
