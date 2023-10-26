from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterationAPIView.as_view(), 
         name="create-user")
    
]