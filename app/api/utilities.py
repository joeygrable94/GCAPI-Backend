import json
from typing import Optional
from urllib import request
from urllib.parse import urlparse

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logger import logger
from app.core.utilities import parse_id
from app.crud import WebsitePageRepository
from app.db.session import get_db_session
from app.models import WebsitePage
from app.schemas import (
    PageSpeedInsightsDevice,
    WebsiteMapPage,
    WebsitePageCreate,
    WebsitePageSpeedInsightsBase,
    WebsitePageUpdate,
)


async def create_or_update_website_page(
    website_id: str,
    sitemap_id: str,
    page: WebsiteMapPage,
) -> None:
    try:
        website_uuid = parse_id(website_id)
        sitemap_uuid = parse_id(sitemap_id)
        parsed_url = urlparse(page.url)
        req_status = request.urlopen(page.url)
        status_code: int = req_status.getcode() if req_status is not None else 404
        session: AsyncSession
        website_page: WebsitePage | None
        async with get_db_session() as session:
            pages_repo: WebsitePageRepository = WebsitePageRepository(session)
            website_page = await pages_repo.exists_by_two(
                field_name_a="url",
                field_value_a=parsed_url.path,
                field_name_b="website_id",
                field_value_b=website_uuid,
            )
            if website_page is not None:
                website_page = await pages_repo.update(
                    entry=website_page,
                    schema=WebsitePageUpdate(
                        url=parsed_url.path,
                        status=status_code,
                        priority=page.priority,
                        last_modified=page.last_modified,
                        change_frequency=page.change_frequency,
                    ),
                )
            else:
                website_page = await pages_repo.create(
                    schema=WebsitePageCreate(
                        url=parsed_url.path,
                        status=status_code,
                        priority=page.priority,
                        last_modified=page.last_modified,
                        change_frequency=page.change_frequency,
                        website_id=website_uuid,
                        sitemap_id=sitemap_uuid,
                    )
                )
    except Exception as e:  # pragma: no cover
        logger.warning("Error Creating or Updating Website Page: %s", e)
    finally:
        return None


def fetch_pagespeedinsights(
    fetch_url: str, device: PageSpeedInsightsDevice
) -> Optional[WebsitePageSpeedInsightsBase]:
    try:
        api_key: Optional[str] = settings.cloud.googleapi
        if api_key is None:  # pragma: no cover
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
        psi_base: WebsitePageSpeedInsightsBase = WebsitePageSpeedInsightsBase(
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
        )
        logger.info("Finished Fetching Page Speed Insights")
        return psi_base
    except Exception as e:  # pragma: no cover
        logger.info("Error Fetching Page Speed Insights: %s", e)
        return None
