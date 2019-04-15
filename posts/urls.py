from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('<int:post_pk>/comment/<int:comment_pk>', views.delete_comment, name='delete_comment'),
    path('<int:post_pk>/comment/', views.create_comment, name='create_comment'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('create/', views.create, name='create'),
    path('', views.list, name='list'),
]