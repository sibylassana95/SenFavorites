import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def get_site_preview(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Recherche du favicon
        favicon_url = None
        favicon_links = soup.find_all('link', rel=lambda r: r and ('icon' in r or 'shortcut icon' in r))
        
        if favicon_links:
            favicon_href = favicon_links[0].get('href', '')
            favicon_url = urljoin(url, favicon_href)
        else:
            # Essayer le favicon par défaut
            parsed_url = urlparse(url)
            default_favicon = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
            favicon_url = default_favicon
            
        return {
            'favicon_url': favicon_url,
            'success': True
        }
    except Exception as e:
        return {
            'favicon_url': None,
            'success': False,
            'error': str(e)
        }