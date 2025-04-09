from django.urls import path
from .views import (
    RegisterStudentView, RegisterAdminView,
    CreateStudentProfileView, CreateAdminProfileView,
    ApplyJobView, MarkAsPlacedView, ProtectedView
)

urlpatterns = [
    path('register/student/', RegisterStudentView.as_view()),
    path('register/admin/', RegisterAdminView.as_view()),
    path('profile/student/', CreateStudentProfileView.as_view()),
    path('profile/admin/', CreateAdminProfileView.as_view()),
    path('apply/', ApplyJobView.as_view()),
    path('mark-placed/<int:student_id>/', MarkAsPlacedView.as_view()),
    path('protected/', ProtectedView.as_view()),  # Login-protected route
]
