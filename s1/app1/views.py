from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Section, Attendance, Assignment , Submission
from django.contrib.auth.decorators import login_required
from datetime import date
User = get_user_model()


# AUTH PAGE
def auth_page(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('student_dashboard')
        elif request.user.role == 'teacher':
            return redirect('teacher_dashboard')
        else:
            return redirect('admin_dashboard')

    return render(request, 'auth.html')


# REGISTER
def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        if role == 'student':
            Student.objects.create(user=user)
        elif role == 'teacher':
            Teacher.objects.create(user=user)

        return redirect('auth_page')


# LOGIN
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('admin_dashboard')

    return redirect('auth_page')


# DASHBOARDS
@login_required
def teacher_dashboard(request):
    return render(request, 'teacher/dashboard.html')


@login_required
def student_dashboard(request):
    return render(request, 'student/dashboard.html')


@login_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')


# TEACHER SECTIONS
@login_required
def teacher_sections(request):
    teacher = Teacher.objects.get(user=request.user)

    sections = Section.objects.filter(teacher=teacher)

    return render(request, 'teacher/sections.html', {'sections': sections})


# SECTION STUDENTS
@login_required
def section_students(request, section_id):
    teacher = Teacher.objects.get(user=request.user)

    section = Section.objects.get(id=section_id, teacher=teacher)

    students = Student.objects.filter(section=section)

    return render(request, 'teacher/students.html', {
        'section': section,
        'students': students
    })




def logout_user(request):
    if request.method == "POST":
        logout(request)
    return redirect('auth_page')


#CREATE SECTION ADMIN

@login_required
def create_section(request):
    if request.method == "POST":
        name = request.POST.get('name')
        teacher_id = request.POST.get('teacher')

        teacher = Teacher.objects.get(id=teacher_id)

        Section.objects.create(name=name, teacher=teacher)

        return redirect('create_section')

    teachers = Teacher.objects.all()
    sections = Section.objects.all()

    return render(request, 'admin/create_section.html', {
        'teachers': teachers,
        'sections': sections
    })


#SHOW STUDENT DETAILS
@login_required
def student_detail(request, student_id):
    teacher= Teacher.objects.get(User=request.user)

    student= Student.objects.get(
        user_id= student_id,
        section_teacher= teacher
    )
    return render(request, 'teacher/student_detail.html',{
        'student':student
    })



# TEACHER MARK ATTENDANCE
@login_required
def mark_attendance(request, section_id):
    teacher = Teacher.objects.get(user=request.user)

    section = Section.objects.get(id=section_id, teacher=teacher)
    students = Student.objects.filter(section=section)

    if request.method == "POST":
        for student in students:
            status = request.POST.get(str(student.user.id))

            Attendance.objects.update_or_create(
                student=student,
                section=section,
                date=date.today(),
                defaults={'status': status}
            )

        return redirect('teacher_sections')

    return render(request, 'teacher/mark_attendance.html', {
        'section': section,
        'students': students
    })


# STUDENT VIEW ATTENDANCE
@login_required
def student_attendance(request):
    student = Student.objects.get(user=request.user)

    records = Attendance.objects.filter(student=student)

    return render(request, 'student/attendance.html', {
        'records': records
    })

#TEACHER ASSIGNMENT
def create_assignment(request, section_id):
    teacher = Teacher.objects.get(user=request.user)

    section = Section.objects.get(id=section_id, teacher=teacher)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')

        Assignment.objects.create(
            title=title,
            description=description,
            section=section
        )

        return redirect('teacher_sections')

    return render(request, 'teacher/create_assignment.html', {
        'section': section
    })

#STUDENT VIEW ASSIGNMENT
@login_required
def student_assignments(request):
    student = Student.objects.get(user=request.user)

    assignments = Assignment.objects.filter(section=student.section)

    return render(request, 'student/assignments.html', {
        'assignments': assignments
    })

#STUDENT SUBMIT ASSIGNMENT
@login_required
def submit_assignment(request, assignment_id):
    student = Student.objects.get(user=request.user)

    assignment = Assignment.objects.get(id=assignment_id)

    if request.method == "POST":
        file = request.FILES.get('file')

        Submission.objects.create(
            assignment=assignment,
            student=student,
            file=file
        )

        return redirect('student_assignments')

    return render(request, 'student/submit_assignment.html', {
        'assignment': assignment
    })

#TEACHER VIEW SUBMISSIONS + GRADING 
@login_required
def view_submissions(request, assignment_id):
    teacher = Teacher.objects.get(user=request.user)

    assignment = Assignment.objects.get(id=assignment_id, section__teacher=teacher)

    submissions = Submission.objects.filter(assignment=assignment)

    return render(request, 'teacher/submissions.html', {
        'submissions': submissions
    })

@login_required
def view_submissions(request, assignment_id):
    teacher = Teacher.objects.get(user=request.user)

    assignment = Assignment.objects.get(id=assignment_id, section__teacher=teacher)

    submissions = Submission.objects.filter(assignment=assignment)

    return render(request, 'teacher/submissions.html', {
        'submissions': submissions
    })

# VIEW TEACHERS
@login_required
def view_teachers(request):
    teachers = Teacher.objects.all()

    return render(request, 'admin/teachers.html', {
        'teachers': teachers
    })

#VIEW STUDENTS

@login_required
def view_students(request):
    students = Student.objects.all()

    return render(request, 'admin/students.html', {
        'students': students
    })

#ASSSIGN SECTION

@login_required
def assign_student_section(request):
    students = Student.objects.all()
    sections = Section.objects.all()

    if request.method == "POST":
        student_id = request.POST.get('student')
        section_id = request.POST.get('section')

        student = Student.objects.get(user_id=student_id)
        section = Section.objects.get(id=section_id)

        student.section = section
        student.save()

        return redirect('assign_student_section')

    return render(request, 'admin/assign_student.html', {
        'students': students,
        'sections': sections
    })