from django.urls import path
from core.views import AccountCreation, PasswordResetViewset, CourseViewset, CourseRegistrationViewset, ServiceRegistrationViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    #Account
    path('account/create/', AccountCreation.as_view({'post': 'create'})),
    path('account/list/', AccountCreation.as_view({'get': 'list'})),
    path('account/send-confirmation-email/', AccountCreation.as_view({'post': 'send_confirmation_email'})),
    path('account/verify-email/', AccountCreation.as_view({'post': 'verify_account'})),
    path('account/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    ##password reset
    path('password-reset-request/', PasswordResetViewset.as_view({'post': 'password_reset_request'})),
    path('password-reset/confirm/', PasswordResetViewset.as_view({'post': 'password_reset_confirm'})),
    
    ##course
    path('course/create/', CourseViewset.as_view({'post': 'create'})),
    path('course/list/', CourseViewset.as_view({'get': 'list'})),
    path('course/update/<int:pk>/', CourseViewset.as_view({'put': 'update'})),
    path('course/delete/<int:pk>/', CourseViewset.as_view({'delete': 'destroy'})),
    path('course/registration/create/<int:id>/', CourseRegistrationViewset.as_view({'post': 'create'})),
    path('course/registration/list/', CourseRegistrationViewset.as_view({'get': 'list'})),
    path('course/registration/update/<int:pk>/', CourseRegistrationViewset.as_view({'put': 'update'})),
    ##service
    path('service/register/create/<int:id>/', ServiceRegistrationViewset.as_view({'post': 'create'})),
    
]
