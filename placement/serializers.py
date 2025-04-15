# Serializers placeholder
from rest_framework import serializers
from .models import CustomUser, StudentProfile, AdminProfile, JobApplication, Company, CompanyJobSelection

class RegisterStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data, is_student=True)
        return user

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'

class RegisterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data, is_admin=True)
        return user

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'email', 'password', 'no_of_jobs', 'min_cgpa', 'required_skills', 'job_role', 
                  'assessment_date', 'assessment_result_date', 'interview_date', 'interview_result_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        company = Company.objects.create(**validated_data)
        return company

class CompanyJobSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyJobSelection
        fields = '__all__'