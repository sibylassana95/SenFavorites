from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.favorite_list, name='favorite_list'),
    path('add/', views.add_favorite, name='add_favorite'),
    path('delete/<int:pk>/', views.delete_favorite, name='delete_favorite'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.deconnection, name='logout'),
    
]