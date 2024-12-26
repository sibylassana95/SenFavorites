import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

class FaviconHandler:
    def __init__(self, url):
        self.url = url
        self.domain = self._get_domain()
        
    def _get_domain(self):
        """Extrait le domaine de base de l'URL."""
        parsed = urlparse(self.url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def _make_request(self, url):
        """Effectue une requête HTTP sécurisée."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            return requests.get(url, headers=headers, timeout=5)
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la requête vers {url}: {str(e)}")
            return None

    def _check_favicon_exists(self, favicon_url):
        """Vérifie si le favicon existe à l'URL donnée."""
        response = self._make_request(favicon_url)
        return response and response.status_code == 200

    def get_favicon(self):
        """Récupère l'URL du favicon en utilisant plusieurs méthodes."""
        try:
            # 1. Essayer d'obtenir la page
            response = self._make_request(self.url)
            if not response:
                return None

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 2. Chercher dans les balises link
            favicon_candidates = []
            
            # Recherche des liens de favicon standards
            for link in soup.find_all('link', rel=lambda r: r and ('icon' in r.lower() or 'shortcut icon' in r.lower())):
                href = link.get('href')
                if href:
                    full_url = urljoin(self.domain, href)
                    favicon_candidates.append(full_url)

            # 3. Ajouter l'URL favicon par défaut
            default_favicon = urljoin(self.domain, '/favicon.ico')
            favicon_candidates.append(default_favicon)

            # 4. Vérifier chaque candidat
            for favicon_url in favicon_candidates:
                if self._check_favicon_exists(favicon_url):
                    logger.info(f"Favicon trouvé: {favicon_url}")
                    return favicon_url

            logger.warning(f"Aucun favicon trouvé pour {self.url}")
            return None

        except Exception as e:
            logger.error(f"Erreur lors de la récupération du favicon: {str(e)}")
            return None