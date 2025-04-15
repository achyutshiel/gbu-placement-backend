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

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    no_of_jobs = models.IntegerField()
    min_cgpa = models.FloatField()
    required_skills = models.TextField()
    job_role = models.CharField(max_length=255)
    assessment_date = models.DateField(null=True, blank=True)
    assessment_result_date = models.DateField(null=True, blank=True)
    interview_date = models.DateField(null=True, blank=True)
    interview_result_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class CompanyJobSelection(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company.name} → {self.student.user.username}"

class JobApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default="Applied", max_length=50)

    def __str__(self):
        return f"{self.student.user.username} → {self.company_name}"