from django.urls import path
from core.views import AccountCreation

urlpatterns = [
    path('account/create/', AccountCreation.as_view({'post': 'create'})),
    path('account/list/', AccountCreation.as_view({'get': 'list'}))
]
