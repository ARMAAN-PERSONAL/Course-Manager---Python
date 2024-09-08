import json

class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor

    def __str__(self):
        return f"{self.course_name} ({self.course_code}), Instructor: {self.instructor}"


class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def remove_course(self, course_code):
        self.courses = [course for course in self.courses if course.course_code != course_code]

    def update_course(self, course_code, new_instructor):
        for course in self.courses:
            if course.course_code == course_code:
                course.instructor = new_instructor
                break

    def __str__(self):
        courses_str = "\n".join([str(course) for course in self.courses])
        return f"Student ID: {self.student_id}, Name: {self.name}, Age: {self.age}\nCourses:\n{courses_str}"


class CourseManagementSystem:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def save_data(self, filename):
        data = [{"student_id": student.student_id, "name": student.name, "age": student.age, 
                 "courses": [{"course_name": c.course_name, "course_code": c.course_code, 
                              "instructor": c.instructor} for c in student.courses]} for student in self.students]
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for student_data in data:
                    student = Student(student_data["student_id"], student_data["name"], student_data["age"])
                    for course_data in student_data["courses"]:
                        course = Course(course_data["course_name"], course_data["course_code"], course_data["instructor"])
                        student.add_course(course)
                    self.add_student(student)
        except FileNotFoundError:
            print("No previous data found.")

    def display_students(self):
        for student in self.students:
            print(student)

    def main_menu(self):
        while True:
            print("\nCourse Management System Menu:")
            print("1. Add New Student")
            print("2. Add Course for a Student")
            print("3. Remove Course")
            print("4. Update Course Instructor")
            print("5. View Students")
            print("6. Save & Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_new_student()
            elif choice == "2":
                self.add_course_to_student()
            elif choice == "3":
                self.remove_course()
            elif choice == "4":
                self.update_course_instructor()
            elif choice == "5":
                self.display_students()
            elif choice == "6":
                self.save_data('student_data.json')
                print("Data saved. Exiting...")
                break
            else:
                print("Invalid choice! Please try again.")

    def add_new_student(self):
        student_id = input("Enter student ID: ")
        name = input("Enter student name: ")
        age = input("Enter student age: ")
        student = Student(student_id, name, int(age))
        self.add_student(student)
        print(f"Student {name} added.")

    def add_course_to_student(self):
        student_id = input("Enter student ID: ")
        student = self.find_student(student_id)
        if student:
            course_name = input("Enter course name: ")
            course_code = input("Enter course code: ")
            instructor = input("Enter course instructor: ")
            course = Course(course_name, course_code, instructor)
            student.add_course(course)
            print(f"Course {course_name} added to student {student.name}.")
        else:
            print("Student not found.")

    def remove_course(self):
        student_id = input("Enter student ID: ")
        student = self.find_student(student_id)
        if student:
            course_code = input("Enter course code to remove: ")
            student.remove_course(course_code)
            print(f"Course {course_code} removed from student {student.name}.")
        else:
            print("Student not found.")

    def update_course_instructor(self):
        student_id = input("Enter student ID: ")
        student = self.find_student(student_id)
        if student:
            course_code = input("Enter course code to update: ")
            new_instructor = input("Enter new instructor name: ")
            student.update_course(course_code, new_instructor)
            print(f"Instructor for course {course_code} updated to {new_instructor}.")
        else:
            print("Student not found.")


if __name__ == "__main__":
    cms = CourseManagementSystem()
    cms.load_data('student_data.json')
    cms.main_menu()
