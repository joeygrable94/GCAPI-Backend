from app.entities.website_page.schemas import SitemapPageChangeFrequency


def test_website_sitemap_page_change_freq_enum() -> None:
    freq = SitemapPageChangeFrequency("hourly")
    assert freq.has_value("hourly")
    assert not freq.has_value("forever")
