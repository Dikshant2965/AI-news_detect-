
"""Source signals. Recognizing a source does not prove its articles are true."""
from urllib.parse import urlparse

TRUSTED_DOMAINS = {
    # Indian official information
    "pib.gov.in": "Press Information Bureau, India",
    "rbi.org.in": "Reserve Bank of India",
    "eci.gov.in": "Election Commission of India",
    "ddnews.gov.in": "DD News",
    "newsonair.gov.in": "News on AIR",
    "ndtv.com": "NDTV",
    "ndtv.in": "NDTV India",

    # International sources
    "who.int": "World Health Organization",
    "reuters.com": "Reuters",
    "apnews.com": "Associated Press",
    "bbc.com": "BBC",

    # Hindi news publishers
    "aajtak.in": "Aaj Tak",
    "ndtv.in": "NDTV India",
    "jagran.com": "Dainik Jagran",
    "bhaskar.com": "Dainik Bhaskar",
    "amarujala.com": "Amar Ujala",
    "livehindustan.com": "Hindustan",

    # Marathi news publishers
    "loksatta.com": "Loksatta",
    "lokmat.com": "Lokmat",
    "maharashtratimes.com": "Maharashtra Times",
    "esakal.com": "Sakal",
    "pudhari.news": "Pudhari",
    "divyamarathi.bhaskar.com": "Divya Marathi",
    "bbcnewsmarathi.in": "BBC News Marathi",
}

ALLOWED_ARTICLE_DOMAINS = set(TRUSTED_DOMAINS.keys())


def is_allowed_domain(url: str) -> bool:
    try:
        parsed = urlparse(
            url if "://" in url else "https://" + url
        )
        domain = (parsed.hostname or "").lower().removeprefix("www.")
    except (ValueError, AttributeError):
        return False

    return any(
        domain == allowed or domain.endswith("." + allowed)
        for allowed in ALLOWED_ARTICLE_DOMAINS
    )


def analyze(url: str | None) -> dict:
    if not url:
        return {
            "domain": None,
            "identified": False,
            "signals": [],
            "assessment": "UNKNOWN",
        }

    try:
        parsed = urlparse(url if "://" in url else "https://" + url)
        domain = (parsed.hostname or "").lower().removeprefix("www.")
    except (ValueError, AttributeError):
        domain = ""

    if not domain:
        return {
            "domain": None,
            "identified": False,
            "signals": [],
            "assessment": "UNKNOWN",
        }

    if domain in TRUSTED_DOMAINS:
        return {
            "domain": domain,
            "identified": True,
            "signals": [f"Recognized domain: {TRUSTED_DOMAINS[domain]}"],
            "assessment": "KNOWN_SOURCE",
        }

    return {
        "domain": domain,
        "identified": True,
        "signals": ["No project-maintained source record for this domain."],
        "assessment": "UNASSESSED",
    }
