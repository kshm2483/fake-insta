from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('delete/<int:post_pk>', views.delete, name='delete'),
    path('update/<int:post_pk>', views.update, name='update'),
    path('create/', views.create, name='create'),
    path('', views.list, name='list'),
]