from sentry_sdk import Client, init

from app.core.config import ApiModes, settings


def configure_monitoring() -> Client | None:
    sentry_client: Client | None = None
    if (
        settings.worker.sentry_dsn and settings.api.mode == ApiModes.production
    ):  # pragma: no cover
        sentry_client = init(
            settings.worker.sentry_dsn,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )  # type: ignore
    return sentry_client
