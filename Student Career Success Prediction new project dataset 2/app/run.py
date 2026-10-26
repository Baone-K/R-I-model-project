from app.main import app  # Imports your original, untouched app
from app.routers import router

# Add the new routes to the existing app
app.include_router(router)