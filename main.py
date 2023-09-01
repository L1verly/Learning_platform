from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from api.handlers import user_router

#########################
# BLOCK WITH API ROUTES #
#########################

# Create instance of the app
app = FastAPI(title="learning-platform")

# Create the instance for the routes
main_api_router = APIRouter()

# Set routes to the app instance
main_api_router.include_router(user_router, prefix='/user', tags=['user'])
app.include_router(main_api_router)

if __name__ == '__main__':
    # Run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
