from datetime import datetime
from decimal import Decimal

import aiohttp
from lxml import etree

from app.schemas import SitemapPageChangeFrequency, WebsiteMapPage


async def fetch_url_status_code(url: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            return response.status


async def fetch_url_page_text(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_sitemap_xml(content: str) -> etree._Element:
    root: etree._Element = etree.fromstring(content.encode())
    return root


async def check_is_xml_valid_sitemap(root: etree._Element) -> bool:
    tag_set = {"urlset", "sitemapindex", "sitemap"}
    for tag in tag_set:
        if tag in root.tag:
            return True
    return False


async def check_is_sitemap_index(root: etree._Element) -> bool:
    if "sitemapindex" in root.tag:
        return True
    return False


async def check_is_sitemap_page(root: etree._Element) -> bool:
    if "sitemap" in root.tag:
        return True
    return False


async def check_is_sitemap_urlset(root: etree._Element) -> bool:
    if "urlset" in root.tag:
        return True
    return False


async def process_sitemap_index(root: etree._Element) -> list[str]:
    sitemap_urls = []
    for element in root.iter():
        if "sitemap" in element.tag:
            loc_elm = element.findtext("{*}loc")
            if loc_elm:
                sitemap_urls.append(loc_elm)
    return sitemap_urls


async def process_sitemap_page_urlset(root: etree._Element) -> list[WebsiteMapPage]:
    sitemap_pages = []
    for element in root.iter():
        if "url" in element.tag and "urlset" not in element.tag:
            sm_page = await process_sitemap_website_page(element)
            sitemap_pages.append(sm_page)
    return sitemap_pages


async def process_sitemap_website_page(root: etree._Element) -> WebsiteMapPage:
    raw_url: str = root.findtext("{*}loc") or ""
    raw_priority: str = root.findtext("{*}priority") or "0.5"
    raw_last_modified: str | None = root.findtext("{*}lastmod") or None
    raw_change_frequency: str | None = root.findtext("{*}changefreq") or None
    priority: Decimal = Decimal(raw_priority)
    last_modified: datetime | None = None
    if raw_last_modified:
        last_modified = datetime.fromisoformat(raw_last_modified)
    change_frequency: SitemapPageChangeFrequency | None = None
    if raw_change_frequency:
        change_frequency = SitemapPageChangeFrequency(raw_change_frequency)
    return WebsiteMapPage(
        url=raw_url,
        priority=priority,
        last_modified=last_modified,
        change_frequency=change_frequency,
    )
