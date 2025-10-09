import math

def grade_avg():
    try:
        num_grades = int(input("How many grades would you like to average? "))
        if num_grades <= 0:
            print("Please enter a positive integer.")
            return grade_avg()
        
        total = 0
        for i in range(num_grades):
            while True:
                try:
                    grade = float(input(f"Enter grade {i + 1}: "))
                    if 0 <= grade <= 100:
                        total += grade
                        break
                    else:
                        print("Grade must be between 0 and 100. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
        
        average = total / num_grades
        print(f"The average of the entered grades is: {round(average, 2)}")
    except ValueError:
        print("Invalid input. Please enter a positive integer.")
        return grade_avg()
    
if __name__ == "__main__":
    grade_avg()