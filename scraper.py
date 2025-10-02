# scraper.py
import re, requests
from bs4 import BeautifulSoup
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}

def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()

def _session():
    s = requests.Session()
    retries = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=0.6,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET","HEAD"]
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.headers.update(HEADERS)
    return s

def scrape_job_description(url: str, timeout=(10, 40)) -> str:
    """
    Try to fetch & extract main text. If site blocks/slow, return "" (let caller fallback to jd_text).
    timeout: (connect_timeout, read_timeout)
    """
    try:
        sess = _session()
        r = sess.get(url, timeout=timeout, allow_redirects=True)
        r.raise_for_status()
    except Exception:
        return ""  

    soup = BeautifulSoup(r.text, "lxml")
    for tag in soup(["script","style","nav","footer","header","form","aside","noscript","svg"]):
        tag.decompose()

    candidates = soup.find_all(["article","section","div","main"])
    def score(node): return len(node.get_text(" ", strip=True))
    best = max(candidates, key=score) if candidates else soup

    text = " ".join(t.get_text(" ", strip=True) for t in best.find_all(["h1","h2","h3","p","li"]))
    return _clean(text)
