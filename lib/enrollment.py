from datetime import datetime

class Student:
    def __init__(self, name):
        self.name = name
        self._enrollments = []  # Stores Enrollment objects
        self._grades = {}  # Dictionary to store grades per enrollment

    def enroll(self, course):
        """Enrolls the student in a given course."""
        if isinstance(course, Course):
            enrollment = Enrollment(self, course)
            self._enrollments.append(enrollment)
            course.add_enrollment(enrollment)
        else:
            raise TypeError("course must be an instance of Course")

    def get_enrollments(self):
        """Returns a copy of the list of enrollments."""
        return self._enrollments.copy()

    def course_count(self):
        """Returns the number of courses the student is enrolled in."""
        return len(self._enrollments)

    def assign_grade(self, enrollment, grade):
        """Assigns a grade to an enrollment."""
        if enrollment in self._enrollments:
            self._grades[enrollment] = grade
        else:
            raise ValueError("Enrollment not found for this student.")

    def aggregate_average_grade(self):
        """Calculates and returns the student's average grade."""
        if not self._grades:
            return 0  # Avoid division by zero
        
        total_grades = sum(self._grades.values())
        num_courses = len(self._grades)
        return total_grades / num_courses


class Course:
    def __init__(self, title):
        self.title = title
        self._enrollments = []  # Stores Enrollment objects

    def add_enrollment(self, enrollment):
        """Adds an enrollment to the course."""
        if isinstance(enrollment, Enrollment):
            self._enrollments.append(enrollment)
        else:
            raise TypeError("enrollment must be an instance of Enrollment")

    def get_enrollments(self):
        """Returns a copy of the list of enrollments."""
        return self._enrollments.copy()


class Enrollment:
    all = []  # Class-level attribute to track all enrollments
    
    def __init__(self, student, course):
        """Creates an enrollment for a student in a course."""
        if isinstance(student, Student) and isinstance(course, Course):
            self.student = student
            self.course = course
            self._enrollment_date = datetime.now()
            type(self).all.append(self)  # Track all enrollments
        else:
            raise TypeError("Invalid types for student and/or course")

    def get_enrollment_date(self):
        """Returns the enrollment date."""
        return self._enrollment_date

    @classmethod
    def aggregate_enrollments_per_day(cls):
        """Returns a dictionary with enrollment counts per day."""
        enrollment_count = {}
        for enrollment in cls.all:
            date = enrollment.get_enrollment_date().date()
            enrollment_count[date] = enrollment_count.get(date, 0) + 1
        return enrollment_count


# ---- TESTING ----
if __name__ == "__main__":
    # Create students and courses
    s1 = Student("Alice")
    s2 = Student("Bob")

    c1 = Course("Math")
    c2 = Course("Science")

    # Enroll students in courses
    s1.enroll(c1)
    s1.enroll(c2)
    s2.enroll(c1)

    # Assign grades
    for enrollment in s1.get_enrollments():
        s1.assign_grade(enrollment, 90)

    for enrollment in s2.get_enrollments():
        s2.assign_grade(enrollment, 85)

    # Print results
    print(f"{s1.name} is enrolled in {s1.course_count()} courses.")  # Output: 2
    print(f"{s2.name} is enrolled in {s2.course_count()} courses.")  # Output: 1

    print("\nEnrollments per day:")
    print(Enrollment.aggregate_enrollments_per_day())

    print(f"\n{s1.name}'s average grade: {s1.aggregate_average_grade()}")  # Output: 90.0
    print(f"{s2.name}'s average grade: {s2.aggregate_average_grade()}")  # Output: 85.0
