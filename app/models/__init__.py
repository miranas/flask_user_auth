import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://6481ea9d0ea1b61ae5724ba8ca5ba630@o4504918162538496.ingest.us.sentry.io/4509668672077824",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,  # Adjust for performance monitoring; set to 0 to disable
    environment="production",  # You can use "development" or "staging" too
    send_default_pii=True     # Sends user info (if you use Flask-Login or similar)
)

