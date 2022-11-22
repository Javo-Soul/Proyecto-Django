from django.urls import path
from core.login.views import *

urlpatterns = [
    path('', loginFormView.as_view(), name = 'login' ),
    path('logout/', LogoutView.as_view(next_page='login'), name = 'logout' ),
]