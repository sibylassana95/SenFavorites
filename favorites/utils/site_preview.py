import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests.exceptions import RequestException, Timeout, SSLError

logger = logging.getLogger(__name__)

def get_site_preview(url):
    """
    Récupère le favicon d'un site avec une meilleure gestion des erreurs.
    """
    try:
        # Configuration de base
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        timeout = 3  # Timeout réduit pour PythonAnywhere
        
        # Extraction du domaine
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        try:
            # Première tentative avec vérification SSL
            response = requests.get(url, headers=headers, timeout=timeout, verify=True)
        except (SSLError, Timeout):
            logger.warning(f"Première tentative échouée pour {url}, réessai sans vérification SSL")
            # Deuxième tentative sans vérification SSL
            response = requests.get(url, headers=headers, timeout=timeout, verify=False)

        if response.status_code != 200:
            logger.warning(f"Statut HTTP non-200 pour {url}: {response.status_code}")
            return {'success': False, 'favicon_url': None}

        soup = BeautifulSoup(response.text, 'html.parser')
        favicon_url = None

        # Recherche prioritaire des favicons
        icon_rels = ['icon', 'shortcut icon', 'apple-touch-icon']
        for rel in icon_rels:
            icons = soup.find_all('link', rel=lambda r: r and rel in r.lower())
            for icon in icons:
                href = icon.get('href')
                if href:
                    potential_favicon = urljoin(domain, href)
                    try:
                        # Vérification que le favicon est accessible
                        favicon_response = requests.head(
                            potential_favicon, 
                            headers=headers, 
                            timeout=2,
                            allow_redirects=True
                        )
                        if favicon_response.status_code == 200:
                            favicon_url = potential_favicon
                            break
                    except RequestException:
                        continue

            if favicon_url:
                break

        # Fallback sur favicon.ico si rien n'a été trouvé
        if not favicon_url:
            default_favicon = f"{domain}/favicon.ico"
            try:
                favicon_response = requests.head(
                    default_favicon, 
                    headers=headers, 
                    timeout=2,
                    allow_redirects=True
                )
                if favicon_response.status_code == 200:
                    favicon_url = default_favicon
            except RequestException:
                pass

        return {
            'success': favicon_url is not None,
            'favicon_url': favicon_url
        }

    except Exception as e:
        logger.error(f"Erreur lors de la récupération du favicon pour {url}: {str(e)}")
        return {
            'success': False,
            'favicon_url': None
        }