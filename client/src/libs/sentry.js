import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";
import config from '../config';

export const configureSentry = () => {
    if (config.ENVIRONMENT !== "local"){
        Sentry.init({
            dsn: config.SENTRY_DNS,
            environment: config.ENVIRONMENT,
            integrations: [new BrowserTracing()],
            tracesSampleRate: 0.05,
        });
    }
}