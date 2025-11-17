import random 

class Course: 
    def __init__(self, course_name, time, class_list):
        crns_dict = {}
        self.course_name = course_name
        CRN = random.randint(10000, 99999)
        if CRN not in crns_dict:
            crns_dict[CRN] = Course(course_name, time, class_list)
        else:
            while CRN in crns_dict.keys():
                CRN = random.randint(10000, 99999)
            crns_dict[CRN] = Course(course_name, time, class_list)
        self.CRN = CRN
        self.time = time
        self.class_list = class_list

    def print_course_details(self):
        print(f"Course Name: {self.course_name}")
        print(f"Course ID: {self.course_id}")
        print(f"Time: {self.time}")
        print("Class List:")
        for student in self.class_list:
            print(f"- {student}")
    
    def access_course(self, CRN, crns_dict):
        if CRN in crns_dict:
            return crns_dict[CRN]
        else:
            return "Not a valid CRN."
    
    def change_time(self, new_time):
        self.time = new_time
    
    def access_crns(self):
        for crn in crns_dict.keys():
            print(crn)
    
    def change_course_name(self, old_name, new_name):
        self.course_name = new_name
    
    
