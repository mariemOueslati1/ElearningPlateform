import speech_recognition as sr
from elearningApp.models import UserProfile

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        try:
            audio = recognizer.listen(source, timeout=5)  # Adjust the timeout as needed
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def get_student_names():
    # Retrieve the names of users with the role "Student"
    student_profiles = UserProfile.objects.filter(roleList='Student')
    student_names = [profile.username for profile in student_profiles]
    return student_names

def initialize_attendance_status(student_names):
    # Initialize attendance status for all students as 'Absent'
    return {student: 'Absent' for student in student_names}

def process_user_response(user_response, attendance_status):
    # Define keywords for attendance status
    present_keywords = ['present']

    # Check if each student's name is mentioned in the user response
    for student in attendance_status:
        if student.lower() in user_response.lower():
            # Check for keywords to determine attendance status
            if any(keyword in user_response.lower() for keyword in present_keywords):
                attendance_status[student] = 'Present'

    return attendance_status

