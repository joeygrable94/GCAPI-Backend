from app.entities.website_sitemap.schemas import SitemapPageChangeFrequency


def test_website_map_enum_custom() -> None:
    freq = SitemapPageChangeFrequency("hourly")
    assert freq.has_value("hourly")
    assert not freq.has_value("forever")
