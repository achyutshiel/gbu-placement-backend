# Models placeholder
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    marksheet = models.FileField(upload_to='marksheets/')
    skills = models.TextField()
    is_placed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class JobApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default="Applied", max_length=50)

    def __str__(self):
        return f"{self.student.user.username} → {self.company_name}"
