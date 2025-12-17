import pickle
import requests
from urlextract import URLExtract
from src.config import logger

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

def load_data_from_pickle(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        logger.info(f"Data successfully loaded from {filepath}")
        return data
    except FileNotFoundError:
        logger.error(f"File {filepath} not found.")
        return None
    except Exception as e:
        logger.error(f"Error reading pickle file: {e}")
        return None

def extract_urls(data):
    extractor = URLExtract()
    urls = []
    
    if isinstance(data, list):
        for item in data:
            found = extractor.find_urls(str(item))
            urls.extend(found)
    elif isinstance(data, str):
        urls = extractor.find_urls(data)
    
    unique_urls = list(set(urls))
    logger.info(f"Found {len(unique_urls)} unique URLs (total found: {len(urls)})")
    return unique_urls

def process_single_url(url):
    if not url.startswith(('http://', 'https://')):
        url_with_scheme = 'http://' + url
    else:
        url_with_scheme = url

    try:
        response = requests.head(
            url_with_scheme, 
            allow_redirects=True, 
            timeout=10, 
            headers=HEADERS
        )
        
        if response.status_code == 405:
            response = requests.get(
                url_with_scheme, 
                allow_redirects=True, 
                timeout=10, 
                stream=True, 
                headers=HEADERS
            )

        return (url, response.url, response.status_code)
    
    except requests.RequestException as e:
        logger.warning(f"Access error for {url}: {e}")
        return (url, None, None)