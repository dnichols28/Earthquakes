import sys
from pathlib import Path
from Admin_files.Course import Course

root_folder = Path(__file__).parent.parent
sys.path.insert(0, str(root_folder))

from Functions import clear_screen
from Functions import admin_input_course
from Functions import create_student_schedule

def admin_driver(admin):
    all_students_schedules = []
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Create Course")
        print("2. View Student Schedule")
        print("3. View Admin Info")
        print("4. Create Student Schedule")
        print("5. Edit Student Schedule")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            clear_screen()
            print("Creating course")
            course1 = admin_input_course()
            course1.print_course_details()


        elif choice == "2":
            clear_screen()
            print("Student schedule")
            student_name = input("Enter student name: ")
            for schedule in all_students_schedules:
                if student_name in schedule:
                    print(f"Schedule for {student_name}:")
                    for course in schedule[student_name]:
                        course.print_course_details()
                    break
            else:
                print(f"No schedule found for {student_name}.")    
            

        elif choice == "3":
            clear_screen()
            admin.display_info()

        elif choice == "4":
            clear_screen()
            print("Create Student Schedule")
            student_name = input("Enter student name: ")
            new_schedule = create_student_schedule(student_name)
            all_students_schedules.append(new_schedule)
            create_new = input("Do you want to create another student schedule? (y/n): ").lower()
            
            while create_new != 'n':
                student_name = input("Enter student name: ")
                new_schedule = create_student_schedule(student_name)
                all_students_schedules.append(new_schedule)
                create_new = input("Do you want to create another student schedule? (y/n): ").lower()

        
        elif choice == "5":
            clear_screen()
            course_action = (input("Add or Remove course from schedule? (a/r): ")).lower()
            if course_action == 'a':
                
            student_name = input("Enter student name: ")
            



        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")
