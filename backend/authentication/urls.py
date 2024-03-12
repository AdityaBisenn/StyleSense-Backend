# myproject/myapp/urls.py
from django.urls import path
from .views import SignUpView, LoginView, LogoutView, protected_route, UserDetailView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('protected/', protected_route, name='protected'),
    path('userdetails/', UserDetailView.as_view(), name='user_detail'),
]
