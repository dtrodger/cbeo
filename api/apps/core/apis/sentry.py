"""
Sentry API
"""

import logging
import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


log = logging.getLogger(__name__)


def configure_sentry(environment, version):
    """
    Configure Sentry SDK
    """

    TRACE_RATE = 0.05
    if environment != "local":
        log.info(f"Sentry configured for environment {environment}")
        sentry_sdk.init(
            dsn=os.environ.get("SENTRY_DNS"),
            integrations=[DjangoIntegration()],
            traces_sample_rate=TRACE_RATE,
            send_default_pii=True,
            environment=environment,
            release=version,
        )
    else:
        log.info(f"Sentry not configured for environment {environment}")
