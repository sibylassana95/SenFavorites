import logging
from django.db.models import Q
from ..models import Favorite
from ..utils.site_preview import get_site_preview

logger = logging.getLogger(__name__)

class FavoriteService:
    @staticmethod
    def get_filtered_favorites(user, search_query=''):
        """Récupère et filtre les favoris d'un utilisateur."""
        favorites = Favorite.objects.filter(user=user)
        
        if search_query:
            favorites = favorites.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(url__icontains=search_query)
            )
        
        return favorites

    @staticmethod
    def verify_and_update_favicons(favorites):
        """Vérifie et met à jour les favicons manquants."""
        updated_count = 0
        
        for favorite in favorites:
            if not favorite.favicon_url:
                preview = get_site_preview(favorite.url)
                if preview['success'] and preview['favicon_url']:
                    favorite.favicon_url = preview['favicon_url']
                    favorite.save()
                    updated_count += 1
                    logger.info(f"Favicon mis à jour pour {favorite.url}")
        
        return updated_count