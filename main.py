import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

import settings
from api.handlers import user_router
from api.login_handler import login_router
from api.service import service_router

# Sentry configuration
sentry_sdk.init(
    dsn=settings.SENTRY_URL,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

#########################
# BLOCK WITH API ROUTES #
#########################

# Create instance of the app
app = FastAPI(title="learning-platform")

# Create the instance for the routes
main_api_router = APIRouter()

# Set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(service_router, tags=["service"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # Run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
