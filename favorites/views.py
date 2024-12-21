from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Favorite
from .forms import FavoriteForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


@login_required(login_url='login')
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites/favorite_list.html', {'favorites': favorites})

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

