import json
from urllib import request

from app.config import settings
from app.core.logger import logger
from app.entities.website_pagespeedinsight.schemas import (
    PageSpeedInsightsDevice,
    WebsitePageSpeedInsightsBase,
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
