from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Favorite
from .forms import FavoriteForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import FavoriteSerializer
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string


@login_required(login_url='login')
def favorite_list(request):
    search_query = request.GET.get('search', '')
    favorites = Favorite.objects.filter(user=request.user)
    
    if search_query:
        favorites = favorites.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(url__icontains=search_query)
        )
    
    # Pagination - 9 favoris par page
    paginator = Paginator(favorites, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'favorites/favorite_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })



def search_favorites(request):
    search_query = request.GET.get('search', '')
    favorites = Favorite.objects.filter(user=request.user)
    
    if search_query:
        favorites = favorites.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(url__icontains=search_query)
        )
    
    paginator = Paginator(favorites, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    html = render_to_string(
        'favorites/favorite_cards.html',
        {'page_obj': page_obj, 'search_query': search_query},
        request=request
    )
    
    return JsonResponse({
        'html': html,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
    })
@login_required(login_url='login')
def add_favorite(request):
    if request.method == 'POST':
        form = FavoriteForm(request.POST)
        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = request.user
            favorite.save()
            return redirect('favorite_list')
    else:
        form = FavoriteForm()
    return render(request, 'favorites/add_favorite.html', {'form': form})

@login_required(login_url='login')
def delete_favorite(request, pk):
    favorite = Favorite.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        favorite.delete()
        return redirect('favorite_list')
    return render(request, 'favorites/delete_favorite.html', {'favorite': favorite})



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès!')
            return redirect('favorite_list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def deconnection(request):
    logout(request)
    return redirect('login')




class AddFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            # Associer l'utilisateur connecté au favori
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
