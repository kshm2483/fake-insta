from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('profile/update/', views.edit_profile, name='edit_profile'),
    path('password/', views.edit_password, name='edit_password'),
    path('delete/', views.del_account, name='del_account'),
    path('update/', views.edit_account, name='edit_account'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('', views.signup, name='signup'),
]