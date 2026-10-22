"""
Evidence retrieval service.

Sources:
1. Google Fact Check Tools API
2. Google News RSS for current news articles
3. Wikipedia fallback for general factual claims

Fact-check metadata and general evidence are kept separate.
"""

import os
import re
import requests

from urllib.parse import quote, urlparse
from xml.etree import ElementTree as ET


class EvidenceProvider:

    def _clean_text(self, text: str) -> str:
        """Clean extracted webpage text."""

        if not text:
            return ""

        text = re.sub(r"\s+", " ", text)
        return text.strip()
    
    def _is_relevant(self, claim: str, title: str, description: str = "") -> bool:
        """Reject news results that share too few meaningful claim words."""
        stop_words = {
            "the", "is", "a", "an", "and", "or", "of", "to", "in",
            "on", "for", "with", "by", "was", "were", "are", "be",
            "has", "have", "had", "from", "that", "this", "it",
            "as", "at", "after", "before", "about", "whether"
        }

        def words(text):
            return {
                word for word in re.findall(r"[a-zA-Z0-9]+", text.lower())
                if len(word) > 2 and word not in stop_words
            }

        claim_words = words(claim)
        result_words = words(title + " " + description)

        if not claim_words:
            return True

        overlap = claim_words & result_words

        # Require at least one meaningful shared term, and more
        # overlap for longer claims.
        required = 1 if len(claim_words) <= 3 else 2
        return len(overlap) >= required



    def search(self, claim: str) -> list[dict]:
        """
        Search external fact-check sources using Google Fact Check Tools API.
        """

        key = os.getenv("GOOGLE_FACTCHECK_API_KEY")

        if not key:
            return []

        try:
            response = requests.get(
                "https://factchecktools.googleapis.com/v1alpha1/claims:search",
                params={
                    "query": claim,
                    "key": key,
                    "languageCode": "en",
                },
                timeout=15,
            )

            response.raise_for_status()

            items = []

            for item in response.json().get("claims", []):

                for review in item.get("claimReview", []):

                    items.append({
                        "claim": item.get("text"),
                        "publisher": review.get(
                            "publisher", {}
                        ).get("name"),

                        "url": review.get("url"),

                        "rating": review.get("textualRating"),

                        "source": "Google Fact Check Tools",
                    })

            return items

        except Exception as exc:

            print("Google Fact Check error:", exc)

            return []


    
    def news_evidence(self, claim: str) -> list[dict]:
        """Retrieve relevant news results and article text when accessible."""
        try:
            query = quote(claim)
            rss_url = (
                "https://news.google.com/rss/search?"
                f"q={query}&hl=en-IN&gl=IN&ceid=IN:en"
            )

            response = requests.get(
                rss_url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 Chrome/153.0 Safari/537.36"
                    )
                },
                timeout=15,
            )
            response.raise_for_status()
            root = ET.fromstring(response.content)

            articles = []

            for item in root.findall(".//item")[:20]:
                title = self._clean_text(item.findtext("title") or "")
                link = item.findtext("link") or ""
                description = item.findtext("description") or ""
                published = item.findtext("pubDate") or ""

                description = re.sub(r"<[^>]+>", " ", description)
                description = self._clean_text(description)

                if not title or not link:
                    continue

                if not self._is_relevant(claim, title, description):
                    continue

                
                source_element = item.find("source")
                publisher = (
                    (source_element.text or "").strip()
                    if source_element is not None
                    else ""
                )
                publisher_homepage = (
                    source_element.get("url", "").strip()
                    if source_element is not None
                    else ""
                )


                article = {
                    "title": title,
                    "text": "",
                    "description": description[:1000],
                    "url": link,
                    "publisher": publisher,
                    "published": published,
                    "source": "Google News",
                    "article_text_available": False,
                    "publisher_homepage": publisher_homepage,
                }

                # Prefer the actual publisher article over its headline
                # or RSS description when assessing the claim.
                webpage = self.webpage_evidence(link)

                if webpage and webpage.get("text"):
                    article["text"] = webpage["text"][:5000]
                    article["url"] = webpage.get("url") or link
                    article["article_text_available"] = True

                    if webpage.get("title"):
                        article["article_title"] = webpage["title"]

                articles.append(article)

                if len(articles) >= 8:
                    break

            return articles

        except Exception as exc:
            print("Google News evidence error:", exc)
            return []


    def resolve_news_url(self, url: str) -> str:
            """
            Resolve a Google News RSS article URL to the original
            publisher URL.

            Google News RSS uses wrapper URLs such as:
            https://news.google.com/rss/articles/...
            """

            if "news.google.com/rss/articles/" not in url:
               return url

            try:
                response = requests.get(
                    url,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 "
                            "(Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 "
                            "Chrome/153.0 Safari/537.36"
                        )
                    },
                    timeout=15,
                    allow_redirects=True,
                )

            # Sometimes Google provides the destination
            # through a redirect.
                final_url = response.url

                if (
                    final_url
                    and "news.google.com" not in final_url
                ):
                    return final_url

            # If Google returns its shell page, don't pretend
            # that it is the publisher article.
                return url

            except Exception as exc:

                print(
                    "Google News URL resolution error:",
                    exc
                )

                return url
    def webpage_evidence(self, url: str) -> dict | None:
        """
        Attempt to extract readable text from a news webpage.

        This is used after finding an article through Google News.
        """

        try: 

            url = self.resolve_news_url(url)

            # Google News shell pages are not article pages.
            if "news.google.com/rss/articles/" in url:
                return None

            from bs4 import BeautifulSoup

            response = requests.get(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "Chrome/153.0 Safari/537.36"
                    )
                },
                timeout=15,
                allow_redirects=True,
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Remove elements that normally contain
            # navigation, scripts, advertisements, etc.
            for element in soup([
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside",
                "form",
            ]):
                element.decompose()

            paragraphs = soup.select("p")

            text_parts = []

            for paragraph in paragraphs:

                text = paragraph.get_text(
                    " ",
                    strip=True
                )

                text = self._clean_text(text)

                if len(text) >= 40:
                    text_parts.append(text)

                if len(" ".join(text_parts)) >= 5000:
                    break

            page_text = self._clean_text(
                " ".join(text_parts)
            )

            if not page_text:
                return None

            return {
                "title": soup.title.get_text(
                    " ",
                    strip=True
                ) if soup.title else "",

                "text": page_text[:5000],

                "url": response.url,

                "source": "News webpage",
            }

        except Exception as exc:

            print(
                "Webpage extraction error:",
                exc
            )

            return None

    
    def web_fact_check_search(self, claim: str) -> list[dict]:
        """Find candidate fact-check articles when the official API has no results."""
        try:
            from bs4 import BeautifulSoup

            query = quote(f'"{claim}" fact check')
            url = f"https://html.duckduckgo.com/html/?q={query}"

            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            trusted_domains = (
                "altnews.in",
                "boomlive.in",
                "factly.in",
                "afp.com",
                "snopes.com",
                "politifact.com",
                "fullfact.org",
                "reuters.com",
            )

            for item in soup.select(".result"):
                link = item.select_one(".result__a")
                snippet = item.select_one(".result__snippet")

                if not link or not link.get("href"):
                    continue

                result_url = link["href"]
                title = self._clean_text(link.get_text(" ", strip=True))
                description = self._clean_text(
                    snippet.get_text(" ", strip=True) if snippet else ""
                )

                if not any(domain in result_url.lower() for domain in trusted_domains):
                    continue

                results.append({
                    "claim": claim,
                    "publisher": "Web search candidate",
                    "url": result_url,
                    "rating": "Not independently verified",
                    "source": "Web fact-check search",
                    "title": title,
                    "description": description,
                })

                if len(results) >= 5:
                    break

            return results

        except Exception as exc:
            print("Web fact-check search error:", exc)
            return []

    def wikipedia_evidence(self, claim: str) -> list[dict]:
        """
        Retrieve general factual evidence from Wikipedia.
        """

        try:

            from bs4 import BeautifulSoup

            words = claim.strip().split()

            candidates = []

            claim_lower = claim.lower()

            if "earth" in claim_lower:
                candidates.append("Earth")

            if "moon" in claim_lower:
                candidates.append("Moon")

            if "sun" in claim_lower:
                candidates.append("Sun")

            if not candidates:

                topic = " ".join(words[:5])

                candidates.append(topic)

            evidence = []

            for title in candidates[:3]:

                url = (
                    "https://en.wikipedia.org/wiki/"
                    + quote(
                        title.replace(" ", "_")
                    )
                )

                response = requests.get(
                    url,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 "
                            "(Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 "
                            "Chrome/153.0 Safari/537.36"
                        )
                    },
                    timeout=15,
                )

                response.raise_for_status()

                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )

                paragraphs = soup.select("p")

                text_parts = []

                for paragraph in paragraphs:

                    text = paragraph.get_text(
                        " ",
                        strip=True
                    )

                    if text:
                        text_parts.append(text)

                    if len(
                        " ".join(text_parts)
                    ) > 4000:
                        break

                page_text = " ".join(
                    text_parts
                )

                if page_text:

                    evidence.append({
                        "title": title,
                        "text": page_text[:4000],
                        "url": url,
                        "source": "Wikipedia",
                    })

            return evidence

        except Exception as exc:

            print(
                "Wikipedia evidence error:",
                exc
            )

            return []