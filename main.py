
from mongoengine import connect
from fastapi import FastAPI
import uvicorn

from AvBigBuddy.AvCounters.routes import AvCounterRoutes
from AvBigBuddy.AvServices.routes import AvServiceRoute
from AvBigBuddy.AvProducts.routes import AvProductsRoute
from AvBigBuddy.AvMembers.routes import AvMemberRoute
from AvBigBuddy.AvQueries.routes import avcontactroutes
from homeImages.routes import homeImagesRoutes
from blogs.routes import blogroutes
from homePageQuery.routes import homePageRoutes
from query.routes import contactroutes
from samplepapers.routes import sampleroutes
from sampleCategory.routes import sampleCategoryRoutes
from serive.routes import serviceroutes
from fastapi.middleware.cors import CORSMiddleware

from counters.routes import counterRoutes


from user.routes import useroutes


connect('UaaWebsitemain', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/UaaWebsitemain")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                     # Frontend origin(s)
    allow_credentials=True,                  # Allow cookies and credentials
    allow_methods=["*"],                     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                     # Allow all headers
)


app.include_router(useroutes.router, tags=["user routes"])
app.include_router(AvCounterRoutes.router, tags=['Av Counters'])
app.include_router(AvServiceRoute.router, tags=['Av Services'])
app.include_router(AvProductsRoute.router, tags=['Av Products'])
app.include_router(AvMemberRoute.router, tags=['Av Members'])
app.include_router(avcontactroutes.router, tags=["Av contact query"])
app.include_router(homeImagesRoutes.router, tags=["Home Images"])
app.include_router(serviceroutes.router, tags=['service'])
app.include_router(counterRoutes.router, tags=['counters'])
app.include_router(blogroutes.router, tags=["Blog routes"])
app.include_router(sampleroutes.router, tags=["Sample"])
app.include_router(sampleCategoryRoutes.router, tags=["Sample Category"])
app.include_router(contactroutes.router, tags=["contact query"])
app.include_router(homePageRoutes.router, tags=["Home page query"])



import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
