from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *
from django.core.mail import send_mail

class RegisterStudentView(APIView):
    def post(self, request):
        user_serializer = RegisterStudentSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            data = request.data.copy()
            data['user'] = user.id
            profile_serializer = StudentProfileSerializer(data=data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response({'message': 'Student registered successfully!'}, status=201)
            else:
                user.delete()  # rollback
                return Response(profile_serializer.errors, status=400)
        return Response(user_serializer.errors, status=400)

class CreateStudentProfileView(APIView):
    def post(self, request):
        serializer = StudentProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student profile created'})
        return Response(serializer.errors, status=400)

class RegisterAdminView(APIView):
    def post(self, request):
        user_serializer = RegisterAdminSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            data = request.data.copy()
            data['user'] = user.id
            profile_serializer = AdminProfileSerializer(data=data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response({'message': 'Admin registered successfully!'}, status=201)
            else:
                user.delete()
                return Response(profile_serializer.errors, status=400)
        return Response(user_serializer.errors, status=400)

class CreateAdminProfileView(APIView):
    def post(self, request):
        serializer = AdminProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Admin profile created'})
        return Response(serializer.errors, status=400)

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

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': f"Hello {request.user.username}, you're authenticated!",
            'user_id': request.user.id
        })
