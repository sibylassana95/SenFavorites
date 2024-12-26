from django.contrib import admin
from .models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'user', 'description', 'created_at', 'favicon_url')
    search_fields = ('title', 'url', 'user__username')
    list_filter = ('user', 'created_at')
    readonly_fields = ('created_at',)  # Rendre 'created_at' en lecture seule

    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'user', 'favicon_url'),
        }),
        ('Details', {
            'fields': ('description', 'created_at'),  # 'created_at' sera maintenant en lecture seule
            'classes': ('collapse',),
        }),
    )

admin.site.register(Favorite, FavoriteAdmin)
