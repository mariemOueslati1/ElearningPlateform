from django.shortcuts import render
from django.http import JsonResponse
from voice_call_service.utils import recognize_speech, process_user_response, get_student_names, initialize_attendance_status

def voice_call(request):
    if request.method == 'POST':
        user_response = recognize_speech()

        student_names = get_student_names()
        attendance_status = initialize_attendance_status(student_names)

        attendance_status = process_user_response(user_response, attendance_status)
        for student, status in attendance_status.items():
            print(student, status)

        # Update the attendance records in the database based on the result
        # for student, status in attendance_status.items():
        #     # Update the database with the attendance status for each student
        #     # You need to adjust this part based on your actual model structure
        #     # student_obj = Student.objects.get(name=student)
        #     # student_obj.attendance_status = status
        #     # student_obj.save()

        # Pass attendance_status to the template
        return render(request, 'result.html', {'attendance_status': attendance_status})
    else:
        # Render the HTML template for testing the voice call
        return render(request, 'test.html')
