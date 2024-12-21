from django.contrib import admin
from .models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'user', 'description', 'created_at')
    search_fields = ('title', 'url', 'user__username')
    list_filter = ('user', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'user')
        }),
        ('Details', {
            'fields': ('description', 'created_at'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Favorite, FavoriteAdmin)