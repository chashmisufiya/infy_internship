# =====================================================
# WEB CRAWLER IMPLEMENTATION
# Tasks Covered:
# Task 1 : Basic Web Crawling using FIFO Queue
# Task 2 : Save Crawled Pages inside pages/ Folder
# Task 3 : Filter Useless Links (mailto, javascript, etc.)
# Task 4 : Crawl Same-Domain Pages Only
# Task 5 : Save Visited URLs into visited.txt
# Task 6 : Retry Logic for Failed URLs
# =====================================================

import os
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


# =====================================================
# Task 3: Filter Useless Links
# =====================================================
def is_valid_url(url):
    """
    Returns True only for valid HTTP/HTTPS URLs
    Filters out:
    - mailto:
    - javascript:
    - tel:
    - #section
    """
    if not url:
        return False

    url = url.strip().lower()
    bad_prefixes = ["mailto:", "javascript:", "tel:", "#"]

    if any(url.startswith(bad) for bad in bad_prefixes):
        return False

    parsed = urlparse(url)
    return parsed.scheme in ("http", "https")


# =====================================================
# Task 6: Retry Logic for Failed URLs
# =====================================================
def fetch_with_retry(url, retries=3, timeout=8):
    """
    Fetches a URL with retry mechanism
    Handles temporary network failures
    """
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except Exception:
            print(f"[x] Attempt {attempt} failed for {url}")
            if attempt == retries:
                return None
            time.sleep(1)


# =====================================================
# Task 1 → Task 6: Main Crawler Function
# =====================================================
def crawl(seed_url, MAX_PAGES=20):

    # -------------------------------------------------
    # Task 2: Create folder for storing pages
    # -------------------------------------------------
    os.makedirs("pages", exist_ok=True)

    # -------------------------------------------------
    # Task 1: Initialize crawler components
    # -------------------------------------------------
    queue = [seed_url]      # FIFO queue
    visited = set()         # Stores visited URLs
    duplicate_urls = 0
    page_id = 1

    # -------------------------------------------------
    # Task 4: Extract seed domain for same-domain crawl
    # -------------------------------------------------
    seed_domain = urlparse(seed_url).netloc

    start_time = time.time()
    print("\n[+] Crawling Started...\n")

    # -------------------------------------------------
    # Task 1: Main crawling loop
    # -------------------------------------------------
    while queue and len(visited) < MAX_PAGES:

        # Task 1(a): Take URL from queue
        current_url = queue.pop(0)

        # Task 1(b): Skip already visited URLs
        if current_url in visited:
            duplicate_urls += 1
            continue

        # Task 6: Fetch page with retry logic
        response = fetch_with_retry(current_url)
        if not response:
            print(f"[!] Skipping URL: {current_url}\n")
            continue

        # Task 1(d) & Task 2: Save HTML page
        file_name = f"pages/page_{page_id}.html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"[✓] Saved: {file_name}")

        # Task 1(e): Extract all links from HTML
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup.find_all("a", href=True):
            raw_link = tag['href']
            full_url = urljoin(current_url, raw_link)

            # Task 3: Filter useless links
            if not is_valid_url(full_url):
                continue

            # Task 4: Crawl same-domain URLs only
            if urlparse(full_url).netloc != seed_domain:
                continue

            # Task 1(f): Add extracted link to queue
            queue.append(full_url)

        # Task 1(g): Mark URL as visited
        visited.add(current_url)

        # Task 1(h): Increment page counter
        page_id += 1

        # Task 1(i): Sleep to avoid server overload
        time.sleep(0.5)

    # -------------------------------------------------
    # Task 5: Save visited URLs to file
    # -------------------------------------------------
    with open("visited.txt", "w") as f:
        for url in visited:
            f.write(url + "\n")

    total_time = round(time.time() - start_time, 2)

    # -------------------------------------------------
    # Final Summary Output
    # -------------------------------------------------
    print("\n----------- SUMMARY -----------")
    print(f"Total Pages Crawled : {len(visited)}")
    print(f"Unique URLs Found   : {len(visited)}")
    print(f"Duplicate URLs      : {duplicate_urls}")
    print("Visited URLs saved to visited.txt")
    print(f"Time Taken (sec)    : {total_time}")
    print("--------------------------------")


# =====================================================
# Program Execution Starts Here
# =====================================================
if __name__ == "__main__":
    seed_url = "https://books.toscrape.com"
    crawl(seed_url, MAX_PAGES=10)
