import json
from urllib import request

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.exceptions import EntityNotFound
from app.core.config import settings
from app.core.logger import logger
from app.core.utilities import parse_id
from app.crud import (
    WebsitePageRepository,
    WebsitePageSpeedInsightsRepository,
    WebsiteRepository,
)
from app.db.session import get_db_session
from app.models import Website, WebsitePage
from app.schemas import (
    PageSpeedInsightsDevice,
    WebsitePageSpeedInsightsBase,
    WebsitePageSpeedInsightsCreate,
)


def fetch_pagespeedinsights(
    fetch_url: str, device: PageSpeedInsightsDevice
) -> WebsitePageSpeedInsightsBase | None:
    try:
        api_key: str | None = settings.cloud.googleapi
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
            score_grade=results["performance-score"]["score"],
            grade_data=json.dumps(results),
        )
        logger.info("Finished Fetching Page Speed Insights")
        return psi_base
    except Exception as e:  # pragma: no cover
        logger.info("Error Fetching Page Speed Insights: %s" % e)
        return None


async def create_website_pagespeedinsights(
    website_id: str,
    page_id: str,
    insights: WebsitePageSpeedInsightsBase,
) -> None:
    try:
        website_uuid = parse_id(website_id)
        page_uuid = parse_id(page_id)
        session: AsyncSession
        website: Website | None
        website_page: WebsitePage | None
        # check if website exists
        async with get_db_session() as session:
            websites_repo: WebsiteRepository = WebsiteRepository(session)
            website = await websites_repo.read(
                entry_id=website_uuid,
            )
        if website is None:
            raise EntityNotFound(entity_info=f"Website {website_id}")
        # check if page exists
        async with get_db_session() as session:
            pages_repo: WebsitePageRepository = WebsitePageRepository(session)
            website_page = await pages_repo.read(
                entry_id=page_uuid,
            )
        if website_page is None:
            raise EntityNotFound(entity_info=f"WebsitePage {page_id}")
        # create website page speed insights
        async with get_db_session() as session:
            psi_repo: WebsitePageSpeedInsightsRepository = (
                WebsitePageSpeedInsightsRepository(session)
            )
            website_page_psi = await psi_repo.create(
                schema=WebsitePageSpeedInsightsCreate(
                    strategy=insights.strategy,
                    score_grade=insights.score_grade,
                    grade_data=insights.grade_data,
                    page_id=website_page.id,
                    website_id=website.id,
                )
            )
            logger.info(
                f"Created Website Page Speed Insights for Website[{website_page_psi.website_id}] and Page[{website_page_psi.page_id}]"  # noqa: E501
            )  # noqa: E501
    except Exception as e:
        logger.warning("Error Creating or Updating Website Page Speed Insights: %s" % e)
    finally:
        return None
