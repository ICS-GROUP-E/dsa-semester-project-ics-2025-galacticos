class StudentNode:
    def __init__(self, student_id, name, course, gpa):
        self.student_id = student_id   # Unique ID (e.g., "P12345")
        self.name = name
        self.course = course
        self.gpa = gpa
        self.next = None  

class StudentLinkedList:
    def __init__(self):
        self.head = None  

    def add_student(self, student_id, name, course, gpa):
        new_student = StudentNode(student_id, name, course, gpa)
        if not self.head:
            self.head = new_student
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_student
        print(f"Student {student_id} added successfully.")

    def delete_student(self, student_id):
        current = self.head
        previous = None

        while current and current.student_id != student_id:
            previous = current
            current = current.next

        if current is None:
            print(f"Student {student_id} not found.")
            return

        if previous is None:
            self.head = current.next
        else:
            previous.next = current.next

        print(f"Student {student_id} deleted successfully.")

    def search_student(self, student_id):
        current = self.head
        while current:
            if current.student_id == student_id:
                print(f"Student found: ID={current.student_id}, Name={current.name}, Course={current.course}, GPA={current.gpa}")
                return current
            current = current.next
        print(f"Student {student_id} not found.")
        return None

    def display_all(self):
        if not self.head:
            print("No students in the list.")
            return

        current = self.head
        print("Student List:")
        while current:
            print(f"ID: {current.student_id}, Name: {current.name}, Course: {current.course}, GPA: {current.gpa}")
            current = current.next

students = StudentLinkedList()
students.add_student("P12345", "Alice", "CS", 3.8)
students.add_student("P23456", "Bob", "Math", 3.2)
students.display_all()
students.search_student("P12345")
students.delete_student("P12345")
students.display_all()