import hashlib
from urllib.parse import parse_qs, urlparse

from app.core.logger import logger
from app.entities.tracking_link.schemas import TrackingLinkBaseParams


def hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def parse_url_utm_params(url: str) -> TrackingLinkBaseParams:
    try:
        utm_params = {}
        parsed_url = urlparse(url)
        parsed_params = parse_qs(parsed_url.query)
        utm_params["scheme"] = parsed_url.scheme
        utm_params["domain"] = parsed_url.netloc
        utm_params["destination"] = (
            f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        )
        utm_params["url_path"] = parsed_url.path
        if parsed_params.get("utm_campaign"):
            utm_params["utm_campaign"] = parsed_params["utm_campaign"][0]
        if parsed_params.get("utm_medium"):
            utm_params["utm_medium"] = parsed_params["utm_medium"][0]
        if parsed_params.get("utm_source"):
            utm_params["utm_source"] = parsed_params["utm_source"][0]
        if parsed_params.get("utm_content"):
            utm_params["utm_content"] = parsed_params["utm_content"][0]
        if parsed_params.get("utm_term"):
            utm_params["utm_term"] = parsed_params["utm_term"][0]
        link_utm_params = TrackingLinkBaseParams(**utm_params)
        return link_utm_params
    except Exception:
        logger.warning(f"Invalid UTM parameters in URL: {url}")
        raise Exception(message="Invalid UTM parameters in URL")
