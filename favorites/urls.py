from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('', views.favorite_list, name='favorite_list'),
    path('api/search/', views.search_favorites, name='search_favorites'),
    path('add/', views.add_favorite, name='add_favorite'),
    path('delete/<int:pk>/', views.delete_favorite, name='delete_favorite'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.deconnection, name='logout'),
    path('api/add/', views.AddFavoriteView.as_view(), name='add_favoriteapi'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]