from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .serializers import *
from django.core.mail import send_mail
from .models import CustomUser, Company

class ApplyJobView(APIView):
    def post(self, request):
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Application submitted'})
        return Response(serializer.errors, status=400)

class MarkAsPlacedView(APIView):
    def post(self, request, student_id):
        try:
            student = StudentProfile.objects.get(id=student_id)
            company_name = request.data.get('company_name')

            student.is_placed = True
            student.save()

            # Send placement email
            send_mail(
                subject="🎉 Congratulations on Your Placement!",
                message=f"Hi {student.user.username},\n\nYou have been successfully placed in {company_name or 'a company'} through GBU Placements.\n\nAll the best for your journey ahead!",
                from_email="noreply@gbu.edu.in",
                recipient_list=[student.user.email],
                fail_silently=False,
            )

            return Response({'message': 'Student marked as placed and email sent.'})
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class ManageJobSelectionView(APIView):
    def post(self, request):
        serializer = CompanyJobSelectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Job selection updated successfully!'}, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, company_id):
        selections = CompanyJobSelection.objects.filter(company_id=company_id)
        serializer = CompanyJobSelectionSerializer(selections, many=True)
        return Response(serializer.data, status=200)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': f"Hello {request.user.username}, you're authenticated!",
            'user_id': request.user.id
        })
        

class ChangePasswordView(APIView):
    """
    Allows authenticated users (Admin, Student, or Company) to change their password.
    """
    def post(self, request):
        user_type = request.data.get('user_type')  # 'admin', 'student', or 'company'
        email = request.data.get('email')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        try:
            if user_type == 'admin':
                user = CustomUser.objects.get(email=email, is_admin=True)
            elif user_type == 'student':
                user = CustomUser.objects.get(email=email, is_student=True)
            elif user_type == 'company':
                user = Company.objects.get(email=email)
            else:
                return Response({'error': 'Invalid user type'}, status=400)

            # Check old password
            if user.check_password(old_password):
                user.password = make_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully!'}, status=200)
            else:
                return Response({'error': 'Old password is incorrect'}, status=400)

        except (CustomUser.DoesNotExist, Company.DoesNotExist):
            return Response({'error': 'User not found'}, status=404)


class ForgotPasswordView(APIView):
    """
    Allows users (Admin, Student, or Company) to reset their password via email.
    """
    def post(self, request):
        user_type = request.data.get('user_type')  # 'admin', 'student', or 'company'
        email = request.data.get('email')

        try:
            if user_type == 'admin':
                user = CustomUser.objects.get(email=email, is_admin=True)
            elif user_type == 'student':
                user = CustomUser.objects.get(email=email, is_student=True)
            elif user_type == 'company':
                user = Company.objects.get(email=email)
            else:
                return Response({'error': 'Invalid user type'}, status=400)

            # Generate a temporary password
            temporary_password = CustomUser.objects.make_random_password()
            user.password = make_password(temporary_password)
            user.save()

            # Send email with the temporary password
            send_mail(
                subject="Password Reset Request",
                message=f"Hi {user.username if user_type != 'company' else user.name},\n\nYour temporary password is: {temporary_password}\nPlease log in and change your password immediately.",
                from_email="noreply@gbu.edu.in",
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({'message': 'Temporary password sent to your email'}, status=200)

        except (CustomUser.DoesNotExist, Company.DoesNotExist):
            return Response({'error': 'User not found'}, status=404)
        

class SendSelectionEmailView(APIView):
    """
    Sends an email to the student once they are selected by a company.
    """
    def post(self, request):
        student_id = request.data.get('student_id')  # Fetch student_id from the request body
        company_name = request.data.get('company_name')
        domain = request.data.get('domain')

        if not student_id or not company_name or not domain:
            return Response({'error': 'Missing required fields'}, status=400)

        try:
            # Fetch the student profile
            student = StudentProfile.objects.get(id=student_id)

            # Send email
            send_mail(
                subject="🎉 Congratulations on Your Selection!",
                message=f"Hi {student.user.username},\n\n"
                        f"Congratulations! You have been selected by {company_name} for the {domain} domain.\n\n"
                        f"Best wishes for your future endeavors!\n\n"
                        f"Regards,\nGBU Placement Team",
                from_email="noreply@gbu.edu.in",
                recipient_list=[student.user.email],
                fail_silently=False,
            )

            return Response({'message': 'Selection email sent successfully!'}, status=200)

        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        
class LoginView(APIView):
    """
    Handles login for Admin, Student, and Company based on the role provided.
    """
    def post(self, request):
        role = request.data.get('role')  # Role: 'admin', 'student', or 'company'
        email = request.data.get('email')
        password = request.data.get('password')

        if not role or not email or not password:
            return Response({'error': 'Role, email, and password are required'}, status=400)

        try:
            if role == 'admin':
                user = CustomUser.objects.get(email=email, is_admin=True)
                if user.check_password(password):
                    return Response({
                        'message': 'Login successful!',
                        'user_id': user.id,
                        'role': 'admin'
                    }, status=200)
            elif role == 'student':
                user = CustomUser.objects.get(email=email, is_student=True)
                if user.check_password(password):
                    return Response({
                        'message': 'Login successful!',
                        'user_id': user.id,
                        'role': 'student'
                    }, status=200)
            elif role == 'company':
                user = Company.objects.get(email=email)
                if check_password(password, user.password):
                    return Response({
                        'message': 'Login successful!',
                        'company_id': user.id,
                        'role': 'company'
                    }, status=200)
            else:
                return Response({'error': 'Invalid role'}, status=400)

            return Response({'error': 'Invalid credentials'}, status=400)

        except (CustomUser.DoesNotExist, Company.DoesNotExist):
            return Response({'error': f'{role.capitalize()} not found'}, status=404)
        

class RegisterView(APIView):
    """
    Handles registration for Admin, Student, and Company based on the role provided.
    """
    def post(self, request):
        role = request.data.get('role')  # Role: 'admin', 'student', or 'company'
        email = request.data.get('email')
        password = request.data.get('password')

        if not role or not email or not password:
            return Response({'error': 'Role, email, and password are required'}, status=400)

        try:
            if role == 'admin':
                # Register Admin
                user = CustomUser.objects.create(
                    email=email,
                    username=request.data.get('username'),
                    is_admin=True,
                    password=make_password(password)
                )
                return Response({
                    'message': 'Admin registered successfully!',
                    'user_id': user.id,
                    'role': 'admin'
                }, status=201)

            elif role == 'student':
                # Register Student
                user = CustomUser.objects.create(
                    email=email,
                    username=request.data.get('username'),
                    is_student=True,
                    password=make_password(password)
                )
                StudentProfile.objects.create(
                    user=user,
                    branch=request.data.get('branch'),
                    skills=request.data.get('skills', ''),
                    resume=request.data.get('resume', None),
                    marksheet=request.data.get('marksheet', None)
                )
                return Response({
                    'message': 'Student registered successfully!',
                    'user_id': user.id,
                    'role': 'student'
                }, status=201)

            elif role == 'company':
                # Register Company
                company = Company.objects.create(
                    name=request.data.get('name'),
                    email=email,
                    password=make_password(password),
                    no_of_jobs=request.data.get('no_of_jobs', 0),
                    min_cgpa=request.data.get('min_cgpa', 0.0),
                    required_skills=request.data.get('required_skills', ''),
                    job_role=request.data.get('job_role', ''),
                    assessment_date=request.data.get('assessment_date', None),
                    assessment_result_date=request.data.get('assessment_result_date', None),
                    interview_date=request.data.get('interview_date', None),
                    interview_result_date=request.data.get('interview_result_date', None)
                )
                return Response({
                    'message': 'Company registered successfully!',
                    'company_id': company.id,
                    'role': 'company'
                }, status=201)

            else:
                return Response({'error': 'Invalid role'}, status=400)

        except Exception as e:
            return Response({'error': str(e)}, status=500)