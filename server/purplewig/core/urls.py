from django.urls import path
from core.views import AccountCreation
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

    
]
