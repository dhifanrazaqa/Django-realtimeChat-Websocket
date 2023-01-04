from django.urls import path
from django.contrib.auth import views

from .views import home, signUpPage, roomDetail, groupDetail

urlpatterns = [
  path('', home, name="Home"),
  path('signup/', signUpPage, name="SignUp"),
  path('login/', views.LoginView.as_view(template_name='auth/loginPage.html'), name="LogIn"),
  path('logout/', views.LogoutView.as_view(), name="LogOut"),
  path('rooms/<slug:slug>', roomDetail, name="roomDetail"),
  path('groups/<slug:slug>', groupDetail, name="groupDetail")
]