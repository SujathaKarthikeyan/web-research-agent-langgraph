import os
import urllib.robotparser
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup


def search_google_custom(
    topics: List[str], filters: Optional[Dict[str, str]] = None, num_results: int = 5
) -> List[Dict[str, str]]:
    search_results = []

    for topic in topics:
        params = {
            "key": os.environ["GCSE_API_KEY"],
            "cx": os.environ["SEARCH_ENGINE_ID"],
            "q": topic,
            "num": num_results,
        }

        if filters:
            if "language" in filters and filters["language"]:
                params["lr"] = f"lang_{filters['language'].lower()}"
            if "timeframe" in filters and filters["timeframe"]:
                params["dateRestrict"] = filters["timeframe"]
            if (
                "region" in filters
                and filters["region"]
                and filters["region"].lower() != "any"
            ):
                params["cr"] = f"country{filters['region'].upper()}"

        response = requests.get(
            "https://www.googleapis.com/customsearch/v1", params=params
        )
        response.raise_for_status()
        data = response.json()

        for item in data.get("items", []):
            search_results.append(
                {
                    "title": item.get("title"),
                    "url": item.get("link"),
                    "snippet": item.get("snippet"),
                }
            )

    return search_results


def scrape_with_robots_check(url: str, user_agent: str = "MyScraperBot"):
    try:
        # Parse robots.txt
        parsed_url = requests.utils.urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()

        if not rp.can_fetch(user_agent, url):
            print(f"Blocked by robots.txt: {url}")
            return None

        # If allowed, scrape
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract visible text
        texts = soup.stripped_strings
        content = "\n".join(texts)

        return content

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
