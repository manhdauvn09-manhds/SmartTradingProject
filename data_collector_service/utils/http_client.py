# A resilient HTTP client with retry logic
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_http_client() -> requests.Session:
    """
    Tạo một HTTP session với cơ chế retry có sẵn.
    """
    session = requests.Session()
    retry = Retry(
        total=3,
        read=3,
        connect=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504)
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
