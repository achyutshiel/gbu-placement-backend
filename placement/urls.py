from django.urls import path
from .views import (
    ApplyJobView, MarkAsPlacedView, ProtectedView,SendSelectionEmailView,LoginView,RegisterView,
    ManageJobSelectionView,ChangePasswordView, ForgotPasswordView
)

urlpatterns = [
    path('apply/', ApplyJobView.as_view()),
    path('mark-placed/<int:student_id>/', MarkAsPlacedView.as_view()),
    path('protected/', ProtectedView.as_view()),  # Login-protected route
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('send-selection-email/', SendSelectionEmailView.as_view(), name='send_selection_email'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    # Company-related routes
    path('job-selection/<int:company_id>/', ManageJobSelectionView.as_view(), name='manage_job_selection'),
]