from abc import ABC, abstractmethod
import json
import os

# Base Class for Person
class Person(ABC):
    def __init__(self, user_id, name, email):
        self._user_id = user_id
        self._name = name
        self._email = email

    @abstractmethod
    def get_role(self):
        pass

    def display_info(self):
        return f"ID: {self._user_id}, Name: {self._name}, Email: {self._email}"

# Student Class
class Student(Person):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self._enrollments = []

    def get_role(self):
        return "Student"

    def enroll(self, course):
        self._enrollments.append(course)

    def view_enrollments(self):
        return self._enrollments

# Instructor Class
class Instructor(Person):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self._courses = []

    def get_role(self):
        return "Instructor"

    def add_course(self, course):
        self._courses.append(course)

    # def view_courses(self):
    #      all_courses= Course.load_courses()
    #      return [course for course in all_courses if course["instructor"] == self._user_id]
    
    def view_my_courses(self):
        all_courses = Course.load_courses()
        
        # Filter courses for this instructor
        my_courses = [course for course in all_courses if course["instructor_id"] == self._user_id]
        
        if not my_courses:
            print("No courses found.")
        else:
            print("My Courses:")
            for course in my_courses:
                print(f"ID: {course['course_id']}, Title: {course['title']}, Description: {course['description']}")


# PlatformAdmin Class
class PlatformAdmin(Person):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)

    def get_role(self):
        return "Platform Admin"

    @staticmethod
    def create_course():
        title = input("Enter course title: ")
        description = input("Enter course description: ")
        instructor_id = int(input("Enter Instructor ID: "))  # Ensure this is valid and exists
        courses = Course.load_courses("courses.json")
        course_id = len(courses) + 1

        new_course = {
            "course_id": course_id,
            "title": title,
            "description": description,
            "instructor": instructor_id  # Use 'instructor' to match view_courses filtering
        }

        courses.append(new_course)
        courses.save_json("courses.json", courses)
        print(f"Course '{title}' created successfully!")


    @staticmethod
    def delete_course(course_id):
        Course.delete_course(course_id)

# Course Class
class Course:
    courses_file = "courses.json"

    def __init__(self, course_id, title, description, instructor):
        self._course_id = course_id
        self._title = title
        self._description = description
        self._instructor = instructor

    def to_dict(self):
        return {
            "course_id": self._course_id,
            "title": self._title,
            "description": self._description,
            "instructor": self._instructor._user_id,
        }

    @classmethod
    def save_course(cls, course_data):
        courses = cls.load_courses()
        courses.append(course_data)
        with open(cls.courses_file, "w") as file:
            json.dump(courses, file, indent=4)

    @classmethod
    def load_courses(cls):
        if os.path.exists(cls.courses_file):
            with open(cls.courses_file, "r") as file:
                return json.load(file)
        return []

    @classmethod
    def delete_course(cls, course_id):
        courses = cls.load_courses()
        courses = [course for course in courses if course["course_id"] != course_id]
        with open(cls.courses_file, "w") as file:
            json.dump(courses, file, indent=4)

# Enrollment Class
class Enrollment:
    enrollments_file = "enrollments.json"

    @staticmethod
    def enroll_student(student_id, course_id):
        enrollments = Enrollment.load_enrollments()
        enrollments.append({"student_id": student_id, "course_id": course_id})
        with open(Enrollment.enrollments_file, "w") as file:
            json.dump(enrollments, file, indent=4)

    @staticmethod
    def load_enrollments():
        if os.path.exists(Enrollment.enrollments_file):
            with open(Enrollment.enrollments_file, "r") as file:
                return json.load(file)
        return []

# Assignment Class
class Assignment:
    assignments_file = "assignments.json"

    def __init__(self, assignment_id, title, course_id):
        self._assignment_id = assignment_id
        self._title = title
        self._course_id = course_id

    def to_dict(self):
        return {
            "assignment_id": self._assignment_id,
            "title": self._title,
            "course_id": self._course_id,
        }

    @classmethod
    def save_assignment(cls, assignment_data):
        assignments = cls.load_assignments()
        assignments.append(assignment_data)
        with open(cls.assignments_file, "w") as file:
            json.dump(assignments, file, indent=4)

    @classmethod
    def load_assignments(cls):
        if os.path.exists(cls.assignments_file):
            with open(cls.assignments_file, "r") as file:
                return json.load(file)
        return []

# Grade Class
class Grade:
    grades_file = "grades.json"

    @staticmethod
    def assign_grade(student_id, assignment_id, grade_value):  # Fixed variable name from 'grade' to 'grade_value'
        grades = Grade.load_grades()
        # Ensure assignment ID is passed correctly to avoid NameError.
        if 'assignment_id' not in locals():
            print("Assignment ID not defined.")
            return
        grades.append({"student_id": student_id,"assignment_id": assignment_id,"grade": grade_value})
        
        with open(Grade.grades_file,"w") as file:
            json.dump(grades,file ,indent=4)

    @staticmethod	
    def load_grades():
        if os.path.exists(Grade.grades_file): 
            with open(Grade.grades_file,"r") as file: 
                return json.load(file) 
        return []

# Schedule Class 
class Schedule:
    schedules_file ="schedules.json"
    
    @staticmethod 
    def add_schedule(course_id,timing): 
        schedules=Schedule.load_schedules() 
        schedules.append({"course_id":course_id, "timing":timing}) 
        with open(Schedule.schedules_file,"w") as file: 
            json.dump(schedules,file ,indent=4) 

    @staticmethod 
    def load_schedules(): 
        if os.path.exists(Schedule.schedules_file): 
            with open(Schedule.schedules_file,"r") as file: 
                return json.load(file) 
        return []

# Submission Class 
class Submission: 
    submissions_file ="submissions.json"
    
    def __init__( self, submission_id , assignment_id ,student_id ,content): 
        self.submission_id=submission_id 
        self.assignment_id=assignment_id 
        self.student_id=student_id 
        self.content=content
    
    def to_dict(self): 
        return { 
            "submission_id":self.submission_id,
            "assignment_id":self.assignment_id,
            "student_id":self.student_id,
            "content":self.content
    }
    
    @classmethod
    def save_submission(cls, submission_data):
        submissions = cls.load_submissions()
        submissions.append(submission_data)
        with open(cls.submissions_file, "w") as file:
            json.dump(submissions, file, indent=4)
                
    
@classmethod
def load_submissions(cls):
        if os.path.exists(cls.submissions_file):
            with open(cls.submissions_file, "r") as file:
                return json.load(file)
        return []
    

# Lesson Class  
class Lesson:  
    lessons_file = "lessons.json"
    
    def __init__(self ,lesson_id ,title ,course_id ,content):  
        self.lesson_id=lesson_id  
        self.title=title  
        self.course_id=course_id  
        self.content=content
    
    def to_dict(self):  
        return {  
            "lesson_id":self.lesson_id,
            "title":self.title,
            "course_id":self.course_id,
            "content":self.content,
        }
    
@classmethod  
def save_lesson(cls ,lesson_data):  
        lessons=cls.load_lessons()  
        lessons.append(lesson_data)  
        with open(cls.lessons_file ,"w") as file:  
            json.dump(lessons, file ,indent=4)  

@classmethod  
def load_lessons(cls):  
    if os.path.exists(cls.lessons_file):  
        with open(cls.lessons_file ,"r") as file:  
            return json.load(file)
    return[]

# Main Application class  
class MainApplication:  
    def __init__(self):
        self.admin = None
        self.instructor = None
        self.student = None
        
    def start(self):  
        while True:  
            choice=self.main_menu()  
            if choice=='1':  
                if self.admin_login():  
                    print("\nAdmin Login Successful.")  
                    self.admin_menu()  
            elif choice=='2':  
                if self.instructor_login():   
                    print("\nInstructor Login Successful.")   
                    self.instructor_menu()   
            elif choice=='3':   
                if self.student_login():   
                    print("\nStudent Login Successful.")   
                    self.student_menu()   
            elif choice=='4':   
                print("Exiting system...")   
                break   
            else:   
                print("Invalid choice ,please try again.")  

    def main_menu(self):  
        print("""   
        ------------------------------------------------------   
        |======================================================|   
        |========   Welcome To E - Learning Platform   ========|   
        |======================================================|   
        ------------------------------------------------------   
        Enter 1 : Admin Login   
        Enter 2 : Instructor Login   
        Enter 3 : Student login   
        Enter 4 : Exit """)    
        return input("Select an option: ")  

    def admin_login(self):    
        username=input("Enter Admin Username: ")    
        password=input("Enter Admin Password: ")    
        with open("users.json","r") as file:    
            users=json.load(file)    
            for user in users:    
                if user["role"]=="admin" and user["username"]==username and user["password"]==password:    
                    self.admin=PlatformAdmin(user["id"],user["name"],user["email"])    
                    return True    
            print("Invalid admin credentials.")    
            return False  

    def instructor_login(self):    
        username=input("Enter Instructor Username: ")    
        password=input("Enter Instructor Password: ")    
        with open("users.json","r") as file:    
            users=json.load(file)    
            for user in users:    
                if user["role"]=="instructor" and user["username"]==username and user["password"]==password:    
                    self.instructor=Instructor(user["id"],user["name"],user["email"])    
                    return True    
            print("Invalid instructor credentials.")    
            return False  

    def student_login(self):    
        username=input("Enter Student Username: ")    
        password=input("Enter Student Password: ")    
        with open("users.json","r") as file:    
            users=json.load(file)    
            for user in users:    
                if user["role"]=="student" and user["username"]==username and user["password"]==password:    
                    self.student=Student(user["id"],user["name"],user["email"])    
                    return True    

                print("Invalid student credentials.")    

                if input("Would you like to register as a new student? (y/n): ").lower()=='y':   
                    self.register_student(username,password)   
                    return True   

        return False  

    def register_student(self ,username,password):     
        email=input("Enter your email : ")     
        with open("users.json","r+") as file :     
            users=json.load(file)     
            new_user={     
                "id":len(users)+1 ,     
                "role":"student" ,     
                "username":username ,     
                "password":password ,     
                "name":username ,     
                "email":email     
            }     
            users.append(new_user)     
            file.seek(0)     
            json.dump(users,file ,indent=4)     
            self.student=Student(user_id=new_user["id"],name=username,email=email)     
            print("Registration successful. You are now logged in.")  

    def admin_menu(self):      
        while True :      
            print("""      
             ------------------------------------------------------      
            |======================================================|      
            |========              ADMIN MENU              ========|      
            |======================================================|      
             ------------------------------------------------------      
                    == Manage Users ==      
            1. Add User (Student/Instructor)      
            2. Remove User      
            3. View All Users      
                    == Manage Courses ==      
            4. Create Course      
            5. Edit Course      
            6. Delete Course      
            7. List All Courses      
                    == Manage Enrollments ==      
            8. View Enrollments      
            9. Enroll a Student      
            10. Remove a Student from a Course      
                    == Go Back to Main Menu ==      
            11.Logout """)
            choice=input("Select an option : ")
            if choice=='1':       
                self.add_user()       
            elif choice=='2':       
                self.remove_user()       
            elif choice=='3':       
                self.view_all_users()       
            elif choice=='4':       
                self.create_course()       
            elif choice=='5':       
                self.edit_course()       
            elif choice=='6':       
                self.delete_course()       
            elif choice=='7':       
                self.list_courses()       
            elif choice=='8':       
                self.view_enrollments()       
            elif choice=='9':       
                self.enroll_student()       
            elif choice=='10':       
                self.remove_student_from_course()       
            elif choice=='11':       
                print("Logging out...")       
                break       
            else :       
                print("Invalid choice , please try again.") 

    def add_user(self):
        role = input("Enter role (student/instructor): ").lower()
        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        users = self.load_json("users.json")
        user_id = len(users) + 1
        new_user = {"id": user_id, "role": role, "name": name, "email": email, "password": password}
        users.append(new_user)

        self.save_json("users.json", users)
        print(f"{role.capitalize()} {name} added successfully!")

    def remove_user(self):
        user_id = int(input("Enter User ID to remove: "))

        users = self.load_json("users.json")
        updated_users = [user for user in users if user["id"] != user_id]

        if len(users) == len(updated_users):
            print("User ID not found.")
        else:
            self.save_json("users.json", updated_users)
            print(f"User ID {user_id} removed successfully!")

    def view_all_users(self):
        users = self.load_json("users.json")
        if not users:
            print("No users found.")
        else:
            print("\nAll Users:")
            for user in users:
                print(f"ID: {user['id']}, Role: {user['role']}, Name: {user['name']}, Email: {user['email']}")

    def create_course(self):
        title = input("Enter course title: ")
        description = input("Enter course description: ")
        instructor_id = int(input("Enter Instructor ID: "))

        courses = self.load_json("courses.json")
        course_id = len(courses) + 1
        new_course = {"course_id": course_id, "title": title, "description": description, "instructor_id": instructor_id}
        courses.append(new_course)

        self.save_json("courses.json", courses)
        print(f"Course '{title}' created successfully!")

    def edit_course(self):
        course_id = int(input("Enter Course ID to edit: "))
        courses = self.load_json("courses.json")
        course = next((c for c in courses if c["course_id"] == course_id), None)

        if not course:
            print("Course ID not found.")
            return

        print("Leave fields blank to keep current values.")
        new_title = input(f"Enter new title ({course['title']}): ") or course['title']
        new_description = input(f"Enter new description ({course['description']}): ") or course['description']
        course["title"] = new_title
        course["description"] = new_description

        self.save_json("courses.json", courses)
        print("Course updated successfully!")

    def delete_course(self):
        course_id = int(input("Enter Course ID to delete: "))

        courses = self.load_json("courses.json")
        updated_courses = [course for course in courses if course["course_id"] != course_id]

        if len(courses) == len(updated_courses):
            print("Course ID not found.")
        else:
            self.save_json("courses.json", updated_courses)
            print(f"Course ID {course_id} deleted successfully!")

    def list_courses(self):
        courses = self.load_json("courses.json")
        if not courses:
            print("No courses found.")
        else:
            print("\nAll Courses:")
            for course in courses:
                print(f"ID: {course['course_id']}, Title: {course['title']}, Description: {course['description']}, Instructor ID: {course['instructor_id']}")

    def view_enrollments(self):
        course_id = int(input("Enter Course ID to view enrollments: "))
        enrollments = Enrollment.load_enrollments()
        users = self.load_json("users.json")

        enrolled_students = [enrollment for enrollment in enrollments if enrollment["course_id"] == course_id]
        
        if not enrolled_students:
            print("No students enrolled in this course.")
        else:
            print("Enrolled Students:")
            for enrollment in enrolled_students:
                student = next((s for s in users if s['id'] == enrollment['student_id']) , None)
                if student:
                    print(f"Student ID: {student['id']}, Name: {student['name']}, Email: {student['email']}")
                else:
                    print(f"Student ID {enrollment['student_id']} not found.")

    def enroll_student(self):
        student_id = int(input("Enter Student ID: "))
        course_id = int(input("Enter Course ID: "))

        enrollments = self.load_json("enrollments.json")
        new_enrollment = {"student_id": student_id, "course_id": course_id}
        enrollments.append(new_enrollment)

        self.save_json("enrollments.json", enrollments)
        print(f"Student ID {student_id} enrolled in Course ID {course_id} successfully!")

    def remove_student_from_course(self):
        student_id = int(input("Enter Student ID: "))
        course_id = int(input("Enter Course ID: "))

        enrollments = self.load_json("enrollments.json")
        updated_enrollments = [e for e in enrollments if not (e["student_id"] == student_id and e["course_id"] == course_id)]

        if len(enrollments) == len(updated_enrollments):
            print("Enrollment not found.")
        else:
            self.save_json("enrollments.json", updated_enrollments)
            print(f"Student ID {student_id} removed from Course ID {course_id} successfully!")

    def load_json(self, filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_json(self, filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)  


    def instructor_menu(self):     
       while True :     
           print("""     
           ------------------------------------------------------     
           |======================================================|     
           |========            INSTRUCTOR MENU           ========|     
           |======================================================|     
           ------------------------------------------------------     
           1. View My Courses     
           2. View Enrollments     
           3. Create Assignments     
           4. Grade Student     
           5. Logout """)
           choice=input("Select an option : ")         
        
           if choice=='1':         
                self.instructor.view_my_courses()         
           elif choice=='2':         
                self.view_enrollments()         
           elif choice=='3':         
                self.create_assignment()         
           elif choice=='4':         
                self.grade_student()         
           elif choice=='5':         
                print("Logging out...")         
                break         
           else :         
                print("Invalid choice , please try again.")  

    def view_enrollments(self):
        course_id = int(input("Enter Course ID to view enrollments: "))
        
        # Load enrollments and users
        enrollments = Enrollment.load_enrollments()  # Assuming this method loads enrollments
        users = self.load_json("users.json")  # Load users from the file

        # Filter enrollments for the given course_id
        enrolled_students = [enrollment for enrollment in enrollments if enrollment["course_id"] == course_id]

        if not enrolled_students:
            print("No students enrolled in this course.")
        else:
            print("\nEnrolled Students:")
            for enrollment in enrolled_students:
                # Use `users` to find the student with the matching `student_id`
                student = next((s for s in users if s['id'] == enrollment['student_id']), None)
                if student:
                    print(f"Student ID: {student['id']}, Name: {student['name']}, Email: {student['email']}")
                else:
                    print(f"Student ID {enrollment['student_id']} not found.")

    def create_assignment(self):        
       title=input("Enter Assignment Title : ")        
       course_id=input("Enter Course ID : ")  
       
       assignments = Assignment.load_assignments()
       assignment_id = len(assignments) + 1  # Generate new assignment ID
       assignment = Assignment(assignment_id, title, course_id)
       Assignment.save_assignment(assignment.to_dict())
       print(f"Assignment '{title}' created successfully!")
    
    def grade_student(self):        
       student_id=input("Enter Student ID : ")        
       assignment_id=input("Enter Assignment ID : ")        
       grade=input("Enter Grade : ")        
       Grade.assign_grade(student_id ,assignment_id ,grade )        
       print(f"Grade assigned to Student ID {student_id} for Assignment ID {assignment_id}.")  

    def student_menu(self):          
      while True :          
        print("""          
          ------------------------------------------------------          
          |======================================================|          
          |========              STUDENT MENU            ========|          
          |======================================================|          
          ------------------------------------------------------          
          1. View Enrolled Courses          
          2. Schedule          
          3. View Assignments          
          4. Submit Assignment          
          5. View Grades          
          6. Logout """)
            
        choice=input ("Select an option : ")          

        if choice =='1' :
          self.view_enrolled_courses ()          
        elif choice =='2' :
          self.view_schedule ()          
        elif choice =='3' :
          self.view_assignments ()          
        elif choice =='4' :
          self.submit_assignment ()          
        elif choice =='5' :
          self.view_grades ()          
        elif choice =='6' :
          print ("Logging out...")  
          break      
      else :
          print ("Invalid choice , please try again.")  

    def view_enrolled_courses (self ):          
      courses=self.student.view_enrollments ()          
      if not courses :
          print ("You are not enrolled in any courses.")          
      else :
          print ("Enrolled Courses :")
          for course in courses :
              print (course )   

    def view_schedule (self ):           
      schedules=Schedule.load_schedules ()           
      for schedule in schedules :
              # Display schedule details related to student's enrolled courses           
              pass   

    def view_assignments (self ):           
      assignments=Assignment.load_assignments ()           
      for assignment in assignments :
              # Display assignment details           
              pass   

    def submit_assignment(self):           
        assignment_id = input("Enter Assignment ID: ")           
        content = input("Enter your submission content: ")           
        submission_id = len(Submission.load_submissions()) + 1  # Generate a unique submission ID          
        student_id = self.student._user_id  # Use the logged-in student's ID
        
        # Create a new Submission object
        submission = Submission(submission_id, assignment_id, student_id, content)
        
        # Save the submission
        Submission.save_submission(submission.to_dict())           
        
        print(f"Submission for Assignment ID {assignment_id} successful!")  

    def view_grades (self ):           
      grades=Grade.load_grades ()           
      student_grades= [g for g in grades if g['student_id'] == self.student._user_id]           
      
      # Check for empty grades list.
      if not student_grades:
          print ("No grades found.")
          return
      
      # Display grades.
      print ("Your Grades:")
      for grade in student_grades:
          assignment_title = next((a['title'] for a in Assignment.load_assignments() if a['assignment id'] == grade['assignment id']),"Unknown")
          print(f"Assignment:{assignment_title}, Grade:{grade['grade']}")

def main():
   app = MainApplication()
   app.start()

if __name__ == "__main__":
   main()
