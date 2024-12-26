import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests.exceptions import RequestException, ProxyError, SSLError

logger = logging.getLogger(__name__)

class FaviconHandler:
    """Classe pour gérer la récupération des favicons de manière orientée objet"""
    
    GOOGLE_FAVICON_URL = "https://www.google.com/s2/favicons?domain={}"
    
    def __init__(self, url):
        self.url = url
        self.domain = self._get_domain()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; FavoritesBot/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        self.timeout = 3
        
    def _get_domain(self):
        """Extrait le domaine de base de l'URL."""
        parsed = urlparse(self.url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def _make_request(self, url, method='get', **kwargs):
        """Effectue une requête HTTP sécurisée."""
        try:
            request_method = getattr(requests, method.lower())
            kwargs.setdefault('headers', self.headers)
            kwargs.setdefault('timeout', self.timeout)
            kwargs.setdefault('verify', False)
            kwargs.setdefault('allow_redirects', True)
            
            return request_method(url, **kwargs)
        except (ProxyError, SSLError) as e:
            logger.warning(f"Erreur de proxy/SSL pour {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la requête vers {url}: {str(e)}")
            return None

    def _check_favicon_exists(self, favicon_url):
        """Vérifie si le favicon existe à l'URL donnée."""
        response = self._make_request(favicon_url, method='head')
        return response and response.status_code == 200

    def _get_google_favicon(self):
        """Récupère le favicon via le service Google Favicon."""
        domain = urlparse(self.url).netloc
        return self.GOOGLE_FAVICON_URL.format(domain)

    def get_favicon(self):
        """Récupère l'URL du favicon en utilisant plusieurs méthodes."""
        try:
            # 1. Essayer d'obtenir la page
            response = self._make_request(self.url)
            if not response or response.status_code != 200:
                logger.warning(f"Impossible d'accéder à {self.url}")
                return {'success': True, 'favicon_url': self._get_google_favicon()}

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 2. Chercher dans les balises link
            icon_rels = ['icon', 'shortcut icon', 'apple-touch-icon']
            for rel in icon_rels:
                for link in soup.find_all('link', rel=lambda r: r and rel in r.lower()):
                    href = link.get('href')
                    if href:
                        favicon_url = urljoin(self.domain, href)
                        if self._check_favicon_exists(favicon_url):
                            logger.info(f"Favicon trouvé: {favicon_url}")
                            return {'success': True, 'favicon_url': favicon_url}

            # 3. Essayer favicon.ico par défaut
            default_favicon = urljoin(self.domain, '/favicon.ico')
            if self._check_favicon_exists(default_favicon):
                logger.info(f"Favicon par défaut trouvé: {default_favicon}")
                return {'success': True, 'favicon_url': default_favicon}

            # 4. Utiliser Google comme fallback
            logger.info(f"Utilisation du service Google Favicon pour {self.domain}")
            return {'success': True, 'favicon_url': self._get_google_favicon()}

        except Exception as e:
            logger.error(f"Erreur lors de la récupération du favicon: {str(e)}")
            return {'success': True, 'favicon_url': self._get_google_favicon()}

def get_site_preview(url):
    """
    Fonction wrapper qui utilise FaviconHandler pour récupérer le favicon.
    Maintenue pour la compatibilité avec le code existant.
    """
    handler = FaviconHandler(url)
    return handler.get_favicon()