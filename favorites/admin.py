from django.contrib import admin
from .models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'user', 'description')
    search_fields = ('title', 'url', 'user__username')

admin.site.register(Favorite, FavoriteAdmin)