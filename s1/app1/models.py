from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone

# ✅ Custom User Model
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_pic = models.ImageField(upload_to='profile_pic', null=True, blank=True)

    def __str__(self):
        return self.username


# ✅ Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    teacher_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    display_id = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.display_id:
            self.display_id = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


# ✅ Section Model
class Section(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# ✅ Student Model
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    student_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    display_id = models.CharField(max_length=10, unique=True, editable=False)

    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.display_id:
            self.display_id = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    
#ATTENDANCE


class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    subject = models.CharField(max_length=100, null=True, blank=True)

    date = models.DateField(default=timezone.now)

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date', 'subject')

    def __str__(self):
        return f"{self.student.user.username} - {self.subject} - {self.date} - {self.status}"    
#ASSIGNMENT
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#SUBMISSION
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"
    

#TIMETABLE
class Timetable(models.Model):
    DAY_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
    ]

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    subject = models.CharField(max_length=100)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.section.name} - {self.subject} - {self.day}"