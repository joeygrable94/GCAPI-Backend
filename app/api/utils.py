import json
from os import environ
from typing import Optional
from urllib import request

from pydantic import UUID4, AnyHttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from usp.objects.page import SitemapPage  # type: ignore
from usp.tree import AbstractSitemap  # type: ignore

from app.core.logger import logger
from app.crud import (
    WebsiteMapRepository,
    WebsitePageRepository,
    WebsitePageSpeedInsightsRepository,
)
from app.db.session import get_db_session
from app.models import WebsiteMap, WebsitePage, WebsitePageSpeedInsights
from app.schemas import (
    WebsiteMapCreate,
    WebsitePageCreate,
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsCreate,
    WebsitePageUpdate,
)
from app.schemas import PageSpeedInsightsDevice


async def create_or_update_website_page(
    website_id: UUID4, sitemap_id: UUID4, page: SitemapPage
) -> None:
    try:
        status_code = request.urlopen(page.url).getcode()
        session: AsyncSession
        async with get_db_session() as session:
            pages_repo: WebsitePageRepository = WebsitePageRepository(session)
            website_page: WebsitePage | None = await pages_repo.exists_by_two(
                field_name_a="url",
                field_value_a=page.url,
                field_name_b="website_id",
                field_value_b=website_id,
            )
            if website_page is None:
                website_page = await pages_repo.create(
                    schema=WebsitePageCreate(
                        url=page.url,
                        status=status_code,
                        priority=page.priority,
                        last_modified=page.last_modified,
                        change_frequency=page.change_frequency,
                        website_id=website_id,
                        sitemap_id=sitemap_id,
                    )
                )
            else:
                website_page = await pages_repo.update(
                    entry=website_page,
                    schema=WebsitePageUpdate(
                        status=status_code,
                        priority=page.priority,
                        last_modified=page.last_modified,
                        change_frequency=page.change_frequency,
                    ),
                )
    except Exception as e:
        logger.info("Error creating or updating website pages:", e)


async def save_sitemap_pages(website_id: UUID4, sitemap: AbstractSitemap) -> None:
    try:
        session: AsyncSession
        async with get_db_session() as session:
            sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session)
            website_map: WebsiteMap | None = await sitemap_repo.exists_by_two(
                field_name_a="url",
                field_value_a=sitemap.url,
                field_name_b="website_id",
                field_value_b=website_id,
            )
            if website_map is None:
                website_map = await sitemap_repo.create(
                    WebsiteMapCreate(url=sitemap.url, website_id=website_id)
                )
            page: SitemapPage
            for page in sitemap.all_pages():
                await create_or_update_website_page(website_id, website_map.id, page)
    except Exception as e:
        logger.info("Error saving sitemap pages:", e)


async def create_website_page_pagespeedinsights(
    website_id: UUID4, page_id: UUID4, psi: WebsitePageSpeedInsightsBase
) -> None:
    try:
        session: AsyncSession
        async with get_db_session() as session:
            site_psi_repo: WebsitePageSpeedInsightsRepository = (
                WebsitePageSpeedInsightsRepository(session)
            )
            psi_create: WebsitePageSpeedInsightsCreate = WebsitePageSpeedInsightsCreate(
                **psi.dict(),
                page_id=page_id,
                website_id=website_id,
            )
            psi_in_db: WebsitePageSpeedInsights = await site_psi_repo.create(
                schema=psi_create
            )
            logger.info(
                "Created Website Page Speed Insights:",
                psi_in_db.id,
                psi_in_db.created_on,
            )
    except Exception as e:
        logger.info("Error saving website page speed insights:", e)


async def fetch_pagespeedinsights(
    website_id: UUID4,
    page_id: UUID4,
    fetch_url: AnyHttpUrl,
    device: PageSpeedInsightsDevice,
) -> None:
    try:
        api_key: Optional[str] = environ.get("GOOGLE_CLOUD_API_KEY", None)
        if api_key is None:
            raise Exception("Google Cloud API Key not found in environment variables")
        fetch_req = "https://%s/%s/%s?url=%s&key=%s&strategy=%s" % (
            "www.googleapis.com/pagespeedonline",
            "v5",
            "runPagespeed",
            fetch_url,
            api_key,
            device.device,
        )
        results: dict = {}
        response = request.urlopen(fetch_req)
        body = response.read()
        resp_data = json.loads(body)
        if response is not None:
            response.close()
        # index the audit processes and the performance test references
        audits_index = resp_data["lighthouseResult"]["audits"]
        audits_process = resp_data["lighthouseResult"]["categories"]["performance"][
            "auditRefs"
        ]
        # set overall site performance for device
        results["performance-score"] = {}
        results["performance-score"]["weight"] = 100
        results["performance-score"]["score"] = resp_data["lighthouseResult"][
            "categories"
        ]["performance"]["score"]
        results["performance-score"]["value"] = "{:.0%}".format(
            resp_data["lighthouseResult"]["categories"]["performance"]["score"]
        )
        results["performance-score"]["unit"] = "percent"
        # loop performance audit processes
        for audit in audits_process:
            # for weighted performance audits
            if audit["weight"] > 0:
                audit_key_value = audit["id"]
                results[audit_key_value] = {}
                results[audit_key_value]["weight"] = audit["weight"]
                if audit["id"] in audits_index:
                    results[audit_key_value]["score"] = audits_index[audit["id"]][
                        "score"
                    ]
                    results[audit_key_value]["value"] = audits_index[audit["id"]][
                        "numericValue"
                    ]
                    results[audit_key_value]["unit"] = audits_index[audit["id"]][
                        "numericUnit"
                    ]
        await create_website_page_pagespeedinsights(
            website_id=website_id,
            page_id=website_id,
            psi=WebsitePageSpeedInsightsBase(
                strategy=device.device,
                ps_weight=results["performance-score"]["weight"],
                ps_grade=results["performance-score"]["score"],
                ps_value=results["performance-score"]["value"],
                ps_unit=results["performance-score"]["unit"],
                fcp_weight=results["first-contentful-paint"]["weight"],
                fcp_grade=results["first-contentful-paint"]["score"],
                fcp_value=results["first-contentful-paint"]["value"],
                fcp_unit=results["first-contentful-paint"]["unit"],
                lcp_weight=results["largest-contentful-paint"]["weight"],
                lcp_grade=results["largest-contentful-paint"]["score"],
                lcp_value=results["largest-contentful-paint"]["value"],
                lcp_unit=results["largest-contentful-paint"]["unit"],
                cls_weight=results["cumulative-layout-shift"]["weight"],
                cls_grade=results["cumulative-layout-shift"]["score"],
                cls_value=results["cumulative-layout-shift"]["value"],
                cls_unit=results["cumulative-layout-shift"]["unit"],
                si_weight=results["speed-index"]["weight"],
                si_grade=results["speed-index"]["score"],
                si_value=results["speed-index"]["value"],
                si_unit=results["speed-index"]["unit"],
                tbt_weight=results["total-blocking-time"]["weight"],
                tbt_grade=results["total-blocking-time"]["score"],
                tbt_value=results["total-blocking-time"]["value"],
                tbt_unit=results["total-blocking-time"]["unit"],
            ),
        )
    except Exception as e:
        exc_str = f"Error fetching page speed insights for Website({website_id}) on Page({page_id})"  # noqa: E501
        logger.warning(exc_str, e)
    finally:
        logger.info("Finished Fetching Page Speed Insights")