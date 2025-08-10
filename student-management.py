import json
import sys

def load_data():
    # Load data from JSON file or return empty dict
    try:
        with open("student.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

def save_data(data):
    # Save data to JSON file
    with open("student.json", "w") as file:
        json.dump(data, file, indent=4)

def input_number(prompt, min_val=None, max_val=None):
    # Get a valid number from user within optional min and max
    while True:
        try:
            num = int(input(prompt))
            if (min_val is not None and num < min_val) or (max_val is not None and num > max_val):
                print(f"Please enter a number between {min_val} and {max_val}.")
                continue
            return num
        except ValueError:
            print("Invalid input! Please enter a valid number.")

# ===== Reporting functions =====

def count_students(data):
    return len(data)

def students_by_grade(data):
    grades = {}
    for student_key, info in data.items():
        grade = info.get("Grade", "Unknown")
        grades[grade] = grades.get(grade, 0) + 1
    return grades

def average_age(data):
    total_age = 0
    count = 0
    for info in data.values():
        age = info.get("Age")
        if age is not None and age.isdigit():
            total_age += int(age)
            count += 1
    return total_age / count if count > 0 else 0

# ===== Main menu =====

def menu():
    while True:
        print("\nMenu:")
        choice = input_number("1. Log in as a parent\n2. Log in as an administrator\n3. Exit\nChoose an option: ", 1, 3)
        
        if choice == 1:
            log_parent()
        elif choice == 2:
            log_administrator()
        elif choice == 3:
            print("Good Bye")
            sys.exit()

def log_parent():
    data = load_data()
    
    while True:
        print("\nParent panel:")
        choice = input_number("1. Add student\n2. Show current info\n3. Edit information\n4. Show reports\n5. Back to main menu\n6. Exit\nChoose an option: ", 1, 6)

        if choice == 1:
            num_entries = input_number("How many entries do you want to add? ", 1)
            for i in range(num_entries):
                student_key = input(f"Enter a key name for student {i+1}: ")
                fields = ["First name", "Last name", "Age", "Grade", "School name"]
                student_info = {}
                print(f"Enter information for '{student_key}':")
                for field in fields:
                    value = input(f"{field}: ").strip()
                    student_info[field] = value
                data[student_key] = student_info
            save_data(data)

        elif choice == 2:
            print("\nCurrent students:")
            print(json.dumps(data, indent=4))
            back = input_number("1-Back to parent menu\n2-Exit\nChoose an option: ", 1, 2)
            if back == 1:
                continue
            else:
                sys.exit()

        elif choice == 3:
            student_key = input("Enter your student key: ")
            if student_key in data:
                while True:
                    print("Select field to edit:\n1-First name\n2-Last name\n3-Age\n4-Grade\n5-School name\n6-Back")
                    edit_choice = input_number("Choose an option: ", 1, 6)
                    if edit_choice == 6:
                        break
                    field_map = {1:"First name", 2:"Last name", 3:"Age", 4:"Grade", 5:"School name"}
                    if edit_choice in field_map:
                        new_value = input(f"Enter new {field_map[edit_choice]}: ").strip()
                        data[student_key][field_map[edit_choice]] = new_value
                        print("Edit successful!")
                        save_data(data)
            else:
                print("Student not found.")

        elif choice == 4:
            print("\n===== Reports =====")
            print(f"Total students: {count_students(data)}")
            print(f"Students by grade: {students_by_grade(data)}")
            print(f"Average age: {average_age(data):.2f}")

        elif choice == 5:
            menu()
        elif choice == 6:
            sys.exit()

def log_administrator():
    data = load_data()
    
    while True:
        print("\nAdministrator panel:")
        choice = input_number("1. Search\n2. Delete student\n3. Add student\n4. Show current info\n5. Show reports\n6. Back to main menu\n7. Exit\nChoose an option: ", 1, 7)

        if choice == 1:
            student_key = input("Enter student key to search: ")
            if student_key in data:
                print(f"Info for '{student_key}':")
                for k, v in data[student_key].items():
                    print(f"{k}: {v}")
            else:
                print("Student not found!")

        elif choice == 2:
            while True:
                student_key = input("Enter student key to delete: ")
                if student_key in data:
                    confirm = input("Are you sure to delete this student? (y/n): ").lower()
                    if confirm in ["y", "yes"]:
                        del data[student_key]
                        save_data(data)
                        print("Deletion successful.")
                        again = input("Delete another? (y/n): ").lower()
                        if again in ["y", "yes"]:
                            continue
                        else:
                            break
                    elif confirm in ["n", "no"]:
                        again = input("Delete another? (y/n): ").lower()
                        if again in ["y", "yes"]:
                            continue
                        else:
                            break
                    else:
                        print("Invalid input.")
                else:
                    print("Student not found!")
                    again = input("Delete another? (y/n): ").lower()
                    if again in ["y", "yes"]:
                        continue
                    else:
                        break

        elif choice == 3:
            num_entries = input_number("How many entries do you want to add? ", 1)
            for i in range(num_entries):
                student_key = input(f"Enter a key name for student {i+1}: ")
                fields = ["First name", "Last name", "Age", "Grade", "School name"]
                student_info = {}
                print(f"Enter information for '{student_key}':")
                for field in fields:
                    value = input(f"{field}: ").strip()
                    student_info[field] = value
                data[student_key] = student_info
            save_data(data)

        elif choice == 4:
            print("Current student info:")
            print(json.dumps(data, indent=4))
            back = input("Press 1 to continue: ")
            if back == "1":
                continue
            else:
                print("Invalid input.")

        elif choice == 5:
            print("\n===== Reports =====")
            print(f"Total students: {count_students(data)}")
            print(f"Students by grade: {students_by_grade(data)}")
            print(f"Average age: {average_age(data):.2f}")

        elif choice == 6:
            menu()
        elif choice == 7:
            sys.exit()

if __name__ == "__main__":
    menu()
