"""Input extraction for text, URL, TXT and PDF."""
import io
import ipaddress
import socket
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

class ExtractionError(Exception):
    pass

def _public_host(host: str) -> bool:
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return False
    return True

def from_url(url: str, max_chars: int = 12000) -> tuple[str, dict]:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname or not _public_host(p.hostname):
        raise ExtractionError("Only public HTTP/HTTPS URLs are allowed.")
    r = requests.get(url, timeout=15, allow_redirects=True, headers={"User-Agent":"Mozilla/5.0 NewsVerificationResearch/1.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script","style","nav","footer","header","aside","form"]): tag.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    body = " ".join(p for p in paragraphs if len(p) >= 30)
    text = (title + ". " + body).strip()
    if len(text) < 50:
        raise ExtractionError("Could not extract enough readable article text from this page.")
    return text[:max_chars], {"url": url, "title": title, "domain": p.hostname}

def from_txt(raw: bytes, max_chars: int = 12000) -> tuple[str, dict]:
    text = raw.decode("utf-8", errors="replace").strip()
    if not text: raise ExtractionError("The TXT file is empty.")
    return text[:max_chars], {"filename": "uploaded.txt"}

def from_pdf(raw: bytes, max_chars: int = 12000) -> tuple[str, dict]:
    reader = PdfReader(io.BytesIO(raw))
    text = "\n".join((page.extract_text() or "") for page in reader.pages).strip()
    if not text: raise ExtractionError("No extractable text was found in this PDF.")
    return text[:max_chars], {"filename": "uploaded.pdf", "pages": len(reader.pages)}
