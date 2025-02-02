from sentry_sdk import Client, init

from .settings import sentry_settings


def configure_sentry_monitoring() -> Client | None:
    sentry_client: Client | None = None
    if sentry_settings.sentry_dsn:  # pragma: no cover
        sentry_client = init(
            sentry_settings.sentry_dsn,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )
    return sentry_client
