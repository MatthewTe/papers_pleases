from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import urllib.parse
import sys
import random
import typing
from loguru import logger

class DownloadLinks(typing.TypedDict):
    title: str
    url: str

def extract_all_download_links(html_str: str) -> list[DownloadLinks]:

    extracted_links: list[DownloadLinks] = []
    try:
        soup = BeautifulSoup(html_str)

        all_download_links = soup.find_all("a", {"jsname": "UWckNb"}, href=True)
        for download_link in all_download_links:

            urls: DownloadLinks = {
                "title": download_link.text,
                "url": download_link['href']
            }
            extracted_links.append(urls)
            logger.info(f"Extracted download link {urls}")

    except Exception as e:
        logger.exception(f"Error in extracting urls. Function returned {extracted_links}")

    return extracted_links

def extract_all_download_link(download_link: str):

    download_urls: list[DownloadLinks] = []
    keep_extracting = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(download_link)

        input()

        while keep_extracting:

            full_page_content = page.content()
            new_download_urls: list[DownloadLinks] = extract_all_download_links(full_page_content)

            if len(new_download_urls) == 0:
                logger.warning(f"Found no more extracted download links from link {download_link}. Exiting.")
                keep_extracting = False

            download_urls += new_download_urls
            logger.info(f"Added {len(new_download_urls)} links to existing download links for total {download_link} links")

            time.sleep(random.randint(1, 5))
            page.click("a#pnnext")
            time.sleep(random.randint(1, 6))

        browser.close()

    return download_urls

if __name__ == "__main__":

    base_url = "https://www.google.com/search?"
    params = {"q": "site:ngc.co.tt filetype:pdf"}

    start_url = base_url+ urllib.parse.urlencode(params)

    all_download_urls: list[DownloadLinks] = extract_all_download_link(start_url)